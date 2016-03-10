import sys 
from json import loads
import operator
import re
#import cPickle as pickle
import redis
import sys
from os.path import abspath
up = '/'.join(abspath(".").split('/')[:-1])
sys.path.append(up)
from config import *
import pattern
from pattern.en import singularize, wordnet

redis = redis.StrictRedis(host=redis_hostname)

def get_recipes(search):
    # returns all recipes with the search string in the name or description
    results = []
    # pickling doesn't seem to be any faster than just loading from redis
    #try:
    #    recipes = pickle.load(open( "recipes.p", "rb" ))
    #except:
    #    recipes = [redis.get(k) for k in redis.keys('*recipe*')] 
    #    pickle.dump( recipes, open( "recipes.p", "wb" ) ) 
    
    recipes = [redis.get(k) for k in redis.keys('*recipe*')] 
    for r in recipes: 
        r = loads(r)
        score = compute_match(search, r)
        if score > 0:
            results.append((r, score))
    sorted_r = sorted(results, key=operator.itemgetter(1))
    sorted_r.reverse()
    i = min(len(sorted_r), 10)
    print sorted_r[:i]
    raw_input()
    return sorted_r[:i] 

def try_similarity(w1, w2):
    try:
        s = wordnet.similarity(w1,w2)
        return s
    except:
        return 0
 
def compute_match(search, recipe):
    #print search
    
    pall = re.compile('('+search.lower()+')') #pall is the regex for the whole search string
    ps = [re.compile('('+s.lower()+' )') for s in search.split(' ')] #ps is the list of regexs for each word.
    rname = recipe['name'].lower()
    #print [p.findall('chili') for p in ps] 
    
    #recipe_2grams = [' '.join(r) for r in zip(*[rname.split(' ')[i:] for i in range(2)])]  
    #recipe_2grams += ['-'.join(r) for r in zip(*[rname.split(' ')[i:] for i in range(2)])]  
    #search_2grams = [' '.join(s) for s in zip(*[search.lower().split(' ')[i:] for i in range(2)])]
    #search_2grams += ['-'.join(s) for s in zip(*[search.lower().split(' ')[i:] for i in range(2)])]
    #
    #filters = [
    #        'vegan', # no meat, cheese, egg, or animal-derived ingredients 
    #        'vegetarian', # no meat
    #        'low fat', 'low-fat', # not a lot of saturated fat
    #        'slow cooker', 'slow-cooker', # uses a slow-cooker or crockpot
    #        'gluten', 'gluten-free', 'gluten free', # no gluten
    #        'paleo', # high protein, low carb
    #        'raw', # no cooking
    #        'easy', 'quick', # low cook time, few ingredients
    #        'low-sodium' # no high salt ingredients
    #        ]
    #_filters = set(filters) & \
    #           (set([s.lower() for s in search.split(' ')]) | set(search_2grams)) & \
    #           (set(rname.split(' ')) | set(recipe_2grams))
    #if not _filters:
    #    return 0 # if the filter isn't in the name, don't return the recipe(?)

    #dashes = [' '.join(f.split('-')) for f in _filters if '-' in f]
    #if dashes: 
    #    _filters.update([' '.join(dashes)])
    #for f in _filters:
    #    rname = rname.replace(f, '')
    # scoring is this way:
        # One or more of the search terms must appear in the recipe title.
        # If both do, the score is doubled.
        # The frequency of the search terms in the description and instructions determines the score.
        # The body score is normalized by the length of the recipe body. 
    try:
        rbody = (recipe['description'] + ' ' + ' '.join(recipe['recipeInstructions'])).lower() 
    except:
        rbody = recipe['description'] 
    name_score = sum([len(p.findall(rname)) for p in ps])
    #print [p.findall(' chili') for p in ps] 
    #print name_score
    #raw_input() 
    body_score = 0
    if len(pall.findall(rname)) > 0 and len(search.split(' ')) > 1:
        name_score = name_score * 2 #double name score is the whole search string is in the name
    if name_score > 0: # only return recipe if search in name(?)
        body_score = sum([sum([try_similarity(wsearch, wbody) for wsearch in search.split(' ')]) for wbody in rbody])
        body_score = body_score / float(len(rbody))
        return name_score + 100*body_score 
    else:
        return 0

def outliers(recipes):
    new_recipes = list(recipes)
    # adjust order of recipes based on similarity of ingredient lists with recipes above
    for i in xrange(len(recipes)):
        ind = len(recipes) - i - 1
    #
    return recipes 
        
if __name__ == '__main__':
    for i, s in enumerate(get_recipes(sys.argv[1])):
        if i < 10:
            print s[0]['name'], s[1]
