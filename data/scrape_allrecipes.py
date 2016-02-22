# This script scrapes publicly available information and attempts to extract 
# indidividual id. 

from bs4 import BeautifulSoup
from json import loads, dumps
from datetime import datetime as dt
import urllib2
import unicodedata
import operator
from lxml import etree
import redis
import sys
from os.path import abspath
up = '/'.join(abspath(".").split('/')[:-1])
sys.path.append(up)
from config import *
import hashlib

redis = redis.StrictRedis(host=redis_hostname)

def parse_url(url):
	data = {'url':url, 'ingredients':[], 'recipeInstructions':[]}
	with open('allrecipes.fields') as f:
		for line in f.readlines():
			data[line.strip()] = ''
	
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
	scraped_page = opener.open(url).read()
        soup = BeautifulSoup(scraped_page.decode('utf-8', 'ignore'), 'lxml')
	
	sections = soup.find_all("section")
	recipe = [s for s in sections if s.get('itemtype') == 'http://schema.org/Recipe'][0]
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
    if len(sys.argv) == 1:
        print 'Usage is `python scraper.py <url_file>`'
        print 'The following keys are present in the redis:' 
        print redis.keys('*recipe*') 
        
    else:
        db = []
        with open(sys.argv[1]) as f:
            for line in f.readlines():
                print line.strip()
                data = parse_url(line.strip())
                try:
                    _id = hashlib.sha224(line.strip()+data['name']).hexdigest()
                except:
                    _id = hashlib.sha224(line.strip()).hexdigest()
                with open('db.json', 'a') as f2:
                    f2.write(dumps(data)+'\n')    
                redis.set('recipe'+_id, dumps(data))
                
