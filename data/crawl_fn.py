# This script starts at a root and crawls through the links.
# It collects and moves on to all links containing urls like:
# "...allrecipes.com/recipe..."

import requests
import sys
import re
from gevent import sleep
from random import shuffle, uniform

seen = []
#p = re.compile('"http://allrecipes\.com/recipe.*?"')
p = re.compile('"/recipes.*?/.*?html"')

def crawlfn_index():
    # url is like: http://www.foodnetwork.com/recipes/a-z.C.64.html
    for i in range(1,100):
        for L in 'ABCDEFGHIJKLMNOPQRSTUVW':
            url = 'http://www.foodnetwork.com/recipes/a-z.%s.%s.html' % (L, i)
            inspect(url)
        url = 'http://www.foodnetwork.com/recipes/a-z.%s.%s.html' % ('XYZ', i)
        inspect(url)
        url = 'http://www.foodnetwork.com/recipes/a-z.%s.%s.html' % ('123', i)
        inspect(url)

def inspect(url):
    print 'inspecting url %s' % url
    r = requests.get(url)
    matches = filter(lambda x: 'a-z' not in x, p.findall(r.text))
    for m in matches:
        if m not in seen:
            print m 
            seen.append(m) 
            m = m.replace('"','')
            with open('fn_urls.txt', 'a') as f:
                f.write('http://www.foodnetwork.com'+m+'\n')

if __name__ == "__main__":
    crawlfn_index()
