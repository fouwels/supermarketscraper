import json
import urllib2
#import pprint
from bs4 import BeautifulSoup
import sys
from flask import Flask
app = Flask(__name__)

@app.route("/")
def error():
	return "no product supplied"

@app.route("/<product>")
def data(product):

	url = 'http://comparesupermarketprices.co.uk/supermarketItems.aspx?search='

	response = (urllib2.urlopen(url + product).read())
	response = response.replace("&nbsp", "NULL")

	#if isinstance(response, str):
	#	print product, " Is STR"
	#if isinstance(response, unicode):
	#	print product, " Is unicode"

	soup = BeautifulSoup(response.decode('utf-8','ignore'))
	table = (soup.html.body.find('table', attrs={'id' : 'ctl00_contentMain_gvItems'}))

	items = []

	for row in table.find_all('tr'):
		collumns = row.find_all('td')
		info = []
		try:
			info = {
				'Description' : collumns[0].string,
				'Supermarket' : collumns[1].string,
				'Offers' : collumns[2].string,
				'Price' : (collumns[3].string),
				'Section' : collumns[4].string,
				'Shelf' : collumns[5].string,	
			}
			items.append(info)
		except Exception:
			pass;
	return json.dumps(items)

if __name__ == "__main__":
    app.run()

