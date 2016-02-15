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

sample_urls = ["http://allrecipes.com/recipe/242314/browned-butter-banana-bread/", "http://allrecipes.com/recipes/360/bread/quick-bread/"]
    
#response = urllib2.urlopen(sample_urls[0])
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
scraped_page = opener.open(sample_urls[0]).read()
soup = BeautifulSoup(scraped_page.decode('utf-8', 'ignore'))

#print soup.descendants

sections = soup.find_all("section")
#sections = soup.find_all("attributes")
#print sections

data = {'ingredients':[], 'recipeInstructions':[]}
with open('allrecipes.fields') as f:
	for line in f.readlines():
		data[line.strip()] = ''

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
				data[prop] = i.string	
			elif prop == 'recipeInstructions':
				data[prop] = [step.string for step in i.contents if step.name == 'li']
			elif prop == 'recipeYield':
				data[prop] = i.get('content')
	except:
		pass

print dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
#print recipe
#for i in recipe:
#	print i.name or i.string

#parser = etree.XMLParser()
#parser = etree.XMLParser(recover=True)
#tree = etree.fromstring(html, parser=parser)
#root = etree.Element("root")

#print root.tag



#opener = urllib2.build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
#scraped_page = opener.open(sample_urls[0]).read()
#
#
#
#
visible_text = soup.getText()
#visible_text = unicodedata.normalize('NFKD', visible_text).encode('ascii','ignore')
#print len(visible_text)
#all_text = ''.join(visible_text)
##print visible_text
##raw_input()
#
#
##[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
#sep_chars1 = ['\n', '.', ',', '"', ';', '?', '!', '[', ']', '{', '}', "'", '-',
#                           '+', '^', '(', ')', ':', '_', '=']
#sep_chars2 = ['\n', '.', ',', '"', ';', '?', '!', '[', ']', '{', '}',
#                           '+', '^', '(', ')', ':', '_', '=', '/']
#for c in sep_chars2:
#    all_text = all_text.replace(c,' ')
#print all_text
#raw_input()
#all_text = ' '.join(all_text.split())
#all_text = all_text.lower()
#all_text = all_text.split()
#
#N = 3
#Ngrams = {}
#for i in xrange(len(all_text) - (N+1)):
#    gram = ' '.join([all_text[i+x] for x in xrange(N)])
#    if Ngrams.get(gram):
#        Ngrams[gram] += 1
#    else:
#        Ngrams[gram] = 1
#
#sorted_N = sorted(Ngrams.items(), key=operator.itemgetter(1))
#print 'Top 10 N grams are:'
#for i in range(1,11):
#    print '"%s", count: %s' % (sorted_N[-i][0], sorted_N[-i][1])
