# This script takes a search string and produces a meta-recipe
# in the schema.org format, suitable for display on a sweet web frontend.
import sys
import itertools
from search import get_recipes
from datetime import date
import re
import nltk
import pattern
from collections import defaultdict
import operator
from datetime import datetime as dt
import time
import pprint

# define number regexes  
pparen = re.compile(r"\(.*\)") # gets anything in parentheses, eg "1 (11 ounce) can of beans"    
pmixed = re.compile(r"[0-9]+\s[0-9]+\/[0-9]") # gets mixed fractions, eg "1 3/4 cups of water"
pfrac = re.compile(r"[0-9]+\/[0-9]+") # gets unmixed fractions, eg "3/4 cup of water"
pdecimal = re.compile(r"[0-9]+\.[0-9]+") # gets decimal numbers, eg "11.34 ounces of butter"
pint = re.compile(r"[0-9]+\s") # gets integer numbers, eg "1 egg"

with open('standard_ingredients.txt') as f:
    standard_ingreds = f.readlines()
    standard_ingreds = set([s.rstrip() for s in standard_ingreds])
 
def compound(words):
    # takes a list of words and reduces to compounds
    # ie ['baking', 'soda', 'baking soda'] --> ['baking soda']
    singles = filter(lambda x: ' ' not in x, words)
    two_grams = [' '.join(phrase) for phrase in list(itertools.combinations(singles,2))] 
    three_grams = [' '.join(phrase) for phrase in list(itertools.combinations(singles,3))]
    removes = [] 
    for t in three_grams:
        t1, t2, t3 = t.split(' ')[:3]
        if t in words: 
            map(removes.append, [t1,t2,t3])
    for t in two_grams:
        t1, t2 = t.split(' ')
        if t in words: 
            map(removes.append, [t1,t2])
    map(words.remove, list(set(removes)))
    doubles = ' '.join(filter(lambda x: ' ' in x, words))
    map(words.remove, [s for s in singles if s in doubles and s in words])
    # remove non standard ingredients, too
    words = filter( lambda x: 
                    x in standard_ingreds or 
                    set(x.split(' ')) & standard_ingreds,
                    words ) 
    return words

def reduce_ingred(ingredient):
    # takes an ingredient string and returns a reduced tuple
    # eg, "1 (19 ounce) can black beans, drained and rinsed" 
    # returns (1, 19 ounce can, black beans) 
    ingredient = ingredient.lower()
    ingredient = ingredient.split(',')[0]
    units = [
    'ounce', 'teaspoon', 'tsp', 'tablespoon', 'tbsp', 'cup', 'pinch', 'dash', 'pound', 'handful', 'kg', 'lb', 'gallon','package', 'can'
    ]
    units += [pattern.en.pluralize(u) for u in units]
    units = set(units)
   
    # grab unit, assuming first that it is parentheses
    unit, unit1, unit2 = re.findall(pparen, ingredient), None, None
    if len(unit) > 0: # pop any unit in parens, eg '(19 ounce)'
        unit1 = unit[0]
        ingredient = ingredient.replace(unit1, '')
    
    #e = 'None' # pop the first other unit
    for e in units & set(ingredient.split(' ')):
        ingredient = ingredient.replace(e, '') 
        #break
        #unit2 = e
        #ingredient = ingredient.replace(unit2, '') 
    
    if len(unit) > 0 and unit2: # if both are there, put them together
        unit = unit1 + ' ' + unit2
    elif len(unit) > 0:
        unit = unit1
    elif unit2:
        unit = unit2
    else:
        unit = 'None'
     
    quantity = re.findall(pmixed, ingredient)
    if len(quantity) == 0:
        quantity = re.findall(pfrac, ingredient)
        if len(quantity) == 0:
            quantity = re.findall(pdecimal, ingredient)
            if len(quantity) == 0:
                quantity = re.findall(pint, ingredient)
                if len(quantity) == 0:
                    quantity = [''] 
  
    ingredient = ingredient.replace(quantity[0], '')
    quantity = quantity[0]
    if '/' in quantity:
        if ' ' in quantity:
            parts = quantity.split(' ')
            frac = map(float, parts[1].split('/'))
        else:
            frac = map(float, quantity.split('/'))
            parts = [0] 
        quantity = int(parts[0]) + frac[0] / frac[1] 
    if quantity:
        quantity = float(quantity)
    
    return ingredient # return only the reduced ingredient description 

def get_ingredients(recipes):
    # extract raw ingredient lists from recipes
    ingredients = [[i for i in r[0]['ingredients']] for r in recipes]
    # flatten into a single list of raw ingredient strings
    ingredients = [i for sublist in ingredients for i in sublist]
    # extract the core ingredient string
    ingredients = map(reduce_ingred, ingredients)
    # reduce the ingredient strings to simple words and phrases 
    #print 'pos tagging.....'
    #t_0 = time.mktime(dt.now().timetuple())
    #all_tags = map(nltk.pos_tag, [i.split() for i in ingredients]) 
    #t_1 = time.mktime(dt.now().timetuple())
    #print 'time elapsed for nltk tagger %s' % (t_1 - t_0) 
    #t_2 = time.mktime(dt.now().timetuple())
    #print [i.split() for i in ingredients]
    all_tags = map(pattern.en.tag, ingredients) 
    #t_3 = time.mktime(dt.now().timetuple())
    #print 'time elapsed for pattern tagger %s' % (t_3 - t_2)
    # an ing in all_tags looks like: [('jar', 'NN'), ('smoked', VBD), ('sour', 'JJ'), ('apples', 'NNS')]
    all_words = [' '.join([w[0] for w in ing if w[1] in ['NN', 'NNS']]) for ing in all_tags]
    all_tokes = [w for phrase in all_words for w in phrase.split(' ')] 
    all_words += all_tokes
    #print all_words
    #print all_tokes
    #raw_input()
    #print all_words
   
    # count the basic words 
    counts = defaultdict(int)
    for w in all_words:
        counts[w] += 1
    #for i in ingredients:
    #    #tags = nltk.pos_tag(nltk.Text(nltk.word_tokenize(i.lower()))) 
    #    #tags = nltk.pos_tag(nltk.word_tokenize(i.lower()))
    #    #print i.lower()
    #    #raw_input()
    #    #tags = nltk.pos_tag(i.lower().split())
    #    for t in tags:
    #        print t
    #        if t[1] == 'NN': counts[t[0]] += 1
    words_sorted = sorted(counts.items(), key=operator.itemgetter(1))
    words_sorted.reverse()
    #print words_sorted
    # assemble a list of all ingredients and amounts
    # sort list by occurences
    # return list
    #words_sorted = compound([w[0] for w in words_sorted[:30] if w[0]) 
    return(compound([w[0] for w in words_sorted[:30] if w[0]])) 

def make_meta(searchs):
    recipes = get_recipes(searchs)
    lens = [len(r[0]['ingredients']) for r in recipes]
    primary_len = int((0.75*sum(lens))/len(lens))
    #print recipes[-5]
    print recipes[-5][0]['url']
    rnames = [r[0]['name'] for r in recipes]
    metar = {
        '@type': 'Recipe',
        'author': 'Metarecipes',
        'datePublished': date.today().__str__()
    }
    metar['name'] = 'Meta ' + searchs

    # ingredients
    all_ingreds = get_ingredients(recipes)
    metar['primaryRecipeIngredient'] = all_ingreds[:primary_len] 
    metar['variantRecipeIngredient'] = all_ingreds[primary_len:] 
   
    # variants
    metar['variants'] = [r[0]['url'] for r in recipes]  
    # description 
    metar['description'] = 'Metarecipe constructed from: ' + ', '.join(rnames)
    return metar



if __name__ == '__main__':
    pprint.PrettyPrinter(indent=4).pprint(make_meta(sys.argv[1]))
