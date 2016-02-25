# This script starts at a root and crawls through the links.
# It collects and moves on to all links containing urls like:
# "...allrecipes.com/recipe..."

import requests
import sys
import re
from gevent import sleep
from random import shuffle, uniform

seen = []
p = re.compile('"http://allrecipes\.com/recipe.*?"')

def crawl(url):
    print url
    seen.append(url)
    r = requests.get(url)
    matches = p.findall(r.text)
    shuffle(matches) 
    for m in matches:
        m = m.replace('"','')
        if m not in seen: 
            with open('all_urls14.txt', 'a') as f:
                f.write(m+'\n')
            crawl(m)

if __name__ == "__main__":
    root = sys.argv[1]
    crawl(root)
