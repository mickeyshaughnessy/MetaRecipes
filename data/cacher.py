# This script loads all the redis keys
# defines the 1000 most popular recipes
# and computes metarecipes for each.
# It then writes them into the html template
# and loads them into redis.

import sys
import redis
from json import loads, dumps
from collections import Counter
from metarecipe import make_meta

redis_hostname = 'localhost'
redis = redis.StrictRedis(host=redis_hostname)

def twograms(array):
    return map(' '.join, zip(*[array[i:] for i in range(2)]))

def threegrams(array):
    return map(' '.join, zip(*[array[i:] for i in range(3)]))

def get_names():
    return [loads(redis.get(k))['name'].lower().split(' ') for k in redis.keys('*recipe*')]

def get_tops(names):
    # get n_grams and dump them into a counter, using one-liner above
    # and list flattening syntax.
    one_grams = Counter([i for sl in names for i in sl]).most_common(500)
    two_grams = Counter([i for sl in map(twograms, names) for i in sl]).most_common(500)
    three_grams = Counter([i for sl in map(threegrams, names) for i in sl]).most_common(500)
    return one_grams, two_grams, three_grams

if __name__ == '__main__':
    if len(sys.argv) == 1:
        names = get_names()
        tops = get_tops(names)
        tops = tops[0] + tops[1] + tops[2]
        for q in tops:
            print q[0]
    else:
        with open(sys.argv[1]) as f:
            tops = [t.rstrip() for t in f.readlines()]

    with open('cached.json', 'w') as fout:
        for t in tops:
            metar = make_meta(t) 
            redis.set('cached:%s' % t, metar)
            fout.write(dumps(metar)+'\n') 

    # make metarecipes
    # make them into html
    # upload them into redis

    # apache rewrite module (turn on)
    # rewrite rules --> take string 'with lime' into appplication query.
    # on query, if query string is cached return cached html, else execute process and cache. 
