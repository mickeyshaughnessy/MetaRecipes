import sys 
from json import loads
import operator
import re
import redis
import sys
from os.path import abspath
up = '/'.join(abspath(".").split('/')[:-1])
sys.path.append(up)
from config import *
import gensim

print 'loading model'
#model = gensim.models.Word2Vec.load_word2vec_format('all_recipes.bin', binary=True)  # C binary format
model = gensim.models.Word2Vec.load_word2vec_format('text8.bin', binary=True)  # C binary format
#model = gensim.models.Word2Vec.load('/Users/michaelshaughnessy/Flourish/Taxonomy/data/en.model')
#model = gensim.models.Word2Vec.load_word2vec_format('/Users/michaelshaughnessy/Flourish/Taxonomy/data/GoogleNews-vectors-negative300.bin', binary=True)  # C binary format
print 'loaded model'

redis = redis.StrictRedis(host=redis_hostname)

def get_recipes(search):
    # returns all recipes with the search string in the name or description
    results = []
    for r in [redis.get(k) for k in redis.keys('*recipe*')]:
        r = loads(r)
        score = compute_match(search, r)
        if score > 0:
            results.append((r, score))
    sorted_r = sorted(results, key=operator.itemgetter(1))
    sorted_r.reverse()
    return sorted_r 
    
def compute_match(search, recipe):
    # match the number of times the search string appears in the recipe
    # name and description fields (ignoring case) and return this number: 0 - inf
    p = re.compile('('+search.lower()+')')
    rstring = (recipe['name'] + ' ' + recipe['description'] + ' ' + ' '.join(recipe['recipeInstructions'])).lower()
    hits = len(p.findall(rstring))
    
    if hits > 0:
       pass 
    return hits

def compute_score(search, recipe):
    recipe = recipe['name'].split() + recipe['description'].split() + ['recipeInstructions'].split()
    return 0


def compute_distance(search, recipe):
    # computes a distance between a recipe and a search string
    # small distances are closer together

    recipe = recipe['name'].split() + recipe['description'].split()
    search.replace(' ','_')
    search = search.lower()
    if search in model.vocab:
        targets = model.most_similar(positive=[search], negative=[])
    else:
        return 1000000 
    d = len(recipe) * len(targets) 
    for phrase in recipe:
        phrase = phrase.lower()
        for target in targets: 
            if (phrase in model.vocab):
                d -= model.similarity(target[0], phrase)
    #d = d / len(recipe)
    
    return d
    if d > 0:
        return d
    else:
        return 200000000 
    
if __name__ == '__main__':
    # argument is search string
    #for R in get_meta(sys.argv[1]):
    #sims = []
    #for R in get_meta(''):
    #    sims.append((R['name'], compute_distance(sys.argv[1], R)))
    #    sims.append((R['name'], compute_distance(sys.argv[1], R)))
    #sorted_sims = sorted(sims, key=operator.itemgetter(1))
    #for s in sorted_sims[:10]:
    #    print s[0], s[1]
    for i, s in enumerate(get_recipes(sys.argv[1])):
        if i < 10:
            print s[0]['name']
        #raw_input() 
