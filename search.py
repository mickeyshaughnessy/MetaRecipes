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
import pattern
from pattern.en import singularize, wordnet


#print 'loading model'
#model = gensim.models.Word2Vec.load_word2vec_format('all_recipes.bin', binary=True)  # C binary format
#model = gensim.models.Word2Vec.load_word2vec_format('text8.bin', binary=True)  # C binary format
#model = gensim.models.Word2Vec.load('/Users/michaelshaughnessy/Flourish/Taxonomy/data/en.model')
#model = gensim.models.Word2Vec.load_word2vec_format('/Users/michaelshaughnessy/Flourish/Taxonomy/data/GoogleNews-vectors-negative300.bin', binary=True)  # C binary format
#print 'loaded model'

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
    print sorted_r
    i = min(len(sorted_r), 10)
    return sorted_r[:i] 

def try_similarity(w1, w2):
    try:
        s = wordnet.similarity(w1,w2)
        return s
    except:
        return 0
 
def compute_match(search, recipe):
    
    # scoring is this way:
        # One or more of the search terms must appear in the recipe title.
        # If both do, the score is doubled.
        # The frequency of the search terms in the description and instructions determines the score.
        # The body score is normalized by the length of the recipe body. 
    pall = re.compile('('+search.lower()+')')
    ps = [re.compile('('+s.lower()+')') for s in search.split(' ')]
    #### This section to handle pluralization isn't quite working
    #if s.lower()[-1] == 's':
    #    ps2 = [re.compile('('+pattern.en.singularize(s.lower())+')') for s in search.split(' ')]
    #else:
    #    ps2 = [re.compile('('+pattern.en.pluralize(s.lower())+')') for s in search.split(' ')]
    #ps = ps1 + ps2
    rname = recipe['name'].lower()
    rbody = (recipe['description'] + ' ' + ' '.join(recipe['recipeInstructions'])).lower() 
     
    name_score = sum([len(p.findall(rname)) for p in ps])
    body_score = 0
    #body_score = sum([model.similarity(, phrase)
    #body_score = sum([len(p.findall(rbody)) for p in ps])
    if len(pall.findall(rname)) > 0 and len(search.split(' ')) > 1:
        name_score = name_score * 2
    if name_score > 0:
        body_score = sum([sum([try_similarity(wsearch, wbody) for wsearch in search.split(' ')]) for wbody in rbody])
        body_score = body_score / float(len(rbody))
        #print recipe['name'], name_score, body_score 
        return name_score + 100*body_score 
    else:
        return 0
    
if __name__ == '__main__':
    for i, s in enumerate(get_recipes(sys.argv[1])):
        if i < 10:
            print s[0]['name'], s[1]
