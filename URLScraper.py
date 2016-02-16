# This script scrapes publicly available information and attempts to extract 
# indidividual id. 

from bs4 import BeautifulSoup
from json import loads, dumps
from datetime import datetime as dt
import sys
import urllib2
import unicodedata
import operator
#import xml.etree.ElementTree as ET
from lxml import etree

def parse_url(url):
    data = {'ingredients':[], 'recipeInstructions':[]}
    with open('allrecipes.fields') as f:
        for line in f.readlines():
            data[line.strip()] = ''
	
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
    scraped_page = opener.open(url).read()
    soup = BeautifulSoup(scraped_page.decode('utf-8', 'ignore'), 'lxml')	
    #print soup
    #### this works for allrecipes.com recipes ####
    #sections = soup.find_all("section")
    sections = soup.find_all("div")
    
    #### this works for norecipes.com recipes ####
    #sections = soup.findall("section","div")

    recipe = [s for s in sections if s.get('itemtype') == 'http://schema.org/Recipe'][0]	
    #recipe = soup.children.findall(itemtype='http://schema.org/Recipe')
    for i in recipe.descendants:
		try:
			prop = i.get('itemprop')
			if prop in data.keys():
				if prop == 'ingredients': 
					data[prop].append(i.string)
				elif prop == 'image':
					data[prop] = i.get('src')
				elif prop in ['prepTime', 'cookTime', 'totalTime']:
					data[prop] = i.get('datetime')
				elif prop in ['description', 'name']:
					data[prop] = i.string.strip()	
				elif prop == 'recipeInstructions':
					data[prop] = [step.string for step in i.contents if step.name == 'li']
				elif prop == 'recipeYield':
					data[prop] = i.get('content')
		except:
			pass
	
	#print dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    return data

if __name__ == '__main__':
    db = []
    if len(sys.argv) > 1:
        print parse_url(sys.argv[1])
    else: 
        with open('urls.text') as f:
            for line in f.readlines():
                print line
                db.append(parse_url(line.strip()))
            with open('db.json', 'w') as f:
                for r in db:
                    f.write(dumps(r)+'\n')
                
