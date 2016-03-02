# This script scrapes publicly available information and attempts to extract 
# indidividual id. 

from bs4 import BeautifulSoup
from json import loads, dumps
from datetime import datetime as dt
import urllib2
import random
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
agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:2.0b4) Gecko/20100818',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-au; rv:1.9.0.1) Gecko/2008070206',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36']

def parse_url(url):
    data = {'url':url, 'ingredients':[], 'recipeInstructions':[]}
    #with open('foodnetwork.fields') as f:
	#    for line in f.readlines():
	#    data[line.strip()] = ''
	
    opener = urllib2.build_opener()
    #opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
    agent = random.choice(agents)
    opener.addheaders = [('User-agent', agent)]
    try:
        scraped_page = opener.open(url).read()
    except:
        return 0
    soup = BeautifulSoup(scraped_page.decode('utf-8', 'ignore'), 'lxml')
	
    #articles = soup.find_all("article")
    #recipe = [a for a in articles if a.get('itemtype') == 'http://schema.org/Recipe']
    try:
        sections = soup.find_all('section')
        sections = filter(lambda x: x.get('class'), sections)
        name_sec = [s for s in sections if ('title' in s.get('class'))][0]
    except:
        return None 
    for k in name_sec.descendants:
        try:
            prop = k.get('itemprop')
            if prop == 'name':
                data['name'] = k.string 
            if prop == 'description':
                data['description'] = k['content']
        except:
            pass
    try:
        recipe = [s for s in sections if ('ingredients-instructions' in s.get('class'))][0]
    except:
        return None
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
            url_count = 0
            for line in f.readlines():
                url_count += 1
                print line.strip(), url_count
                data = parse_url(line.strip())
                try:
                    _id = hashlib.sha224(line.strip()+data['name']).hexdigest()
                except:
                    _id = hashlib.sha224(line.strip()).hexdigest()
                if data:
                    with open('db_foodnetwork.json', 'a') as f2:
                        f2.write(dumps(data)+'\n')    
                redis.set('recipe'+_id, dumps(data))
                
