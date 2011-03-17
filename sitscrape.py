from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time
import urllib2
import unicodedata

def fetch(url):
	opener = urllib2.build_opener()
	opener.addheaders = [("User-agent", "sit-dinner-bot")]
	response = opener.open(url)
	return response.read()

def mangle(string):
	"""Strip non ascii chars
	"""
	return reduce(lambda x,y: x+y, map(unicode,string)).encode("ascii","replace").replace("??","_").replace("?","_")
	
def extract_menu(doc):
	soup = BeautifulSoup(doc)
	menu = []
	for tag in soup.findAll("table", {"id":"menytable"}):
		for table in tag.findAll("table"):
			day_menu = []
			day_prices = []
			for item in table.findAll("td", {"class":"menycelle"}):
				day_menu.append(mangle(BeautifulSoup(item.prettify().replace("\n","")).findAll("td")[0].contents))
			for item in table.findAll("td", {"class":"priscelle"}):
				day_prices.append(mangle(BeautifulSoup(item.prettify().replace("\n","")).findAll("td")[0].contents).replace(",-",""))
			menu.append(zip(day_menu,day_prices))
	return menu
	#return ["Error.. :("]*5
		
def todays_menu(urls):
	print urls
	today = datetime.now().weekday()
	if today > 4:
		return ["No dinner today, it's closed on saturday and sunday.)"]
	r = []
	for title in urls.keys():
		r.append(title)
		lines =  extract_menu(fetch(urls[title]))[today]
		
		for x in xrange(len(lines)):
			r.append(str(x+1)+". " + lines[x][0] + ", "+lines[x][1])
	return r

for l in todays_menu({ "Realfag":"http://www.sit.no/content/36447/Ukas-middagsmeny-pa-Realfag", 
					"Hangaren":"http://www.sit.no/content/36444/Ukas-middagsmeny-pa-Hangaren"}):
	print l