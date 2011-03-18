# -*- coding: utf-8 -*-
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
import sys
import newsscrape

class NewsBot(irc.IRCClient):
	def _get_nickname(self):
		return self.factory.nickname
	nickname = property(_get_nickname)
	
	def signedOn(self):
		self.join(self.factory.channel)
		print "Signed on as %s." % (self.nickname,)
	
	def joined(self, channel):
		print "Joined %s." % (channel,)
	
	def privmsg(self, user, channel, msg):
		if not user:
			return
		if "!nyheter" in msg:
			site = "http://www.vg.no/rss/create.php"
			#TODO rate limit this, and cache...
			news_lines = newsscrape.get_news(site)
			self.msg(self.factory.channel, "*** Nyheter fra VG RSS ***")
			for line in news_lines:
				self.msg(self.factory.channel, line)

class NewsBotFactory(protocol.ClientFactory):
    protocol = NewsBot
    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname
        
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
        
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
	try:
		nick = sys.argv[1]
		chan = sys.argv[2]
		server = sys.argv[3]
		reactor.connectTCP(server, 6667, NewsBotFactory("#"+chan, nick))
		reactor.run()
	except:
		print "Usage:"
		print "python news-bot.py nick channel server"
		print ""
		print "Omit # for channel"
