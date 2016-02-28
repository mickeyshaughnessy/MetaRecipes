# This script scrapes publicly available information and attempts to extract 
# indidividual id. 

#from bs4 import BeautifulSoup
from json import loads, dumps
from datetime import datetime as dt
import sys
from os.path import abspath
import urllib2
import unicodedata
import operator
#from lxml import etree
import redis
import hashlib

up = '/'.join(abspath(".").split('/')[:-1])
sys.path.append(up)
from config import *

redis = redis.StrictRedis(host=redis_hostname)

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            data = loads(line.strip())
            try:
                _id = hashlib.sha224(line.strip()+data['name']).hexdigest()
            except:
                _id = hashlib.sha224(line.strip()).hexdigest()
            redis.set('recipe'+_id, dumps(data))
                
