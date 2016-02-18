import sys 
from json import loads
import operator
import re
import redis
from config import *

redis = redis.StrictRedis(host=redis_hostname)

def get_recipes(search):
    results = []
    for r in [redis.get(k) for k in redis.keys('*recipe#*')]:
        score = compute_match(search, r)
        if score > 0:
            results.append((r, score))
    sorted_r = sorted(results, key=operator.itemgetter(1))
    sorted_r.reverse()
    for r in sorted_r:
        print r[0]['name']

def compute_match(search, recipe):
    # match the number of times the search string appears in the recipe
    # name and description fields (ignoring case) and return this number: 0 - inf
    p = re.compile('('+search.lower()+')')
    result = p.findall((recipe['name'] + recipe['description']).lower()) 
    return len(result)

    # alternate algorithm - compute similarity score between 
    # 1. break seach string into words.
    # 2. for each word in the string, compute


if __name__ == '__main__':
    # argument is search string
    get_recipes(sys.argv[1])
