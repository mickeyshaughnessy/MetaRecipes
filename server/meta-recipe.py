# This script takes a search string and produces a meta-recipe
# in the schema.org format, suitable for display on a sweet web frontend.
import sys
from search import get_recipes
from datetime import date
import re
import nltk
import pattern

def reduce_ingred(ingredient):
    ingredient = ingredient.lower()
    # takes an ingredient string and returns a reduced tuple
    
    # define unit strings
    units = [
    'ounce', 'teaspoon', 'tsp', 'tablespoon', 'tbsp', 'cup', 'pinch', 'dash', 'pound', 'handful', 'kg', 'lb',
    ]
    units += [pattern.en.pluralize(u) for u in units]
    units = set(units)
   
    # define number regexes  
    pparen = re.compile(r"\(.*\)") # gets anything in parentheses, eg "1 (11 ounce) can of beans"    
    pmixed = re.compile(r"[0-9]+\s[0-9]+\/[0-9]") # gets mixed fractions, eg "1 3/4 cups of water"
    pfrac = re.compile(r"[0-9]+\/[0-9]+") # gets unmixed fractions, eg "3/4 cup of water"
    pdecimal = re.compile(r"[0-9]+\.[0-9]+") # gets decimal numbers, eg "11.34 ounces of butter"
    pint = re.compile(r"[0-9]+\s") # gets integer numbers, eg "1 egg"

    # grab unit, assuming first that it is parentheses
    unit = re.findall(pparen, ingredient)
    e = 'None' 
    if len(unit) == 0:
        for e in units & set(ingredient.split(' ')):
            break
        unit = e
    else:
        unit = unit[0] 
    ingredient = ingredient.replace(unit, '') 
    
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
 
    print ('%s - %s - %s') % (quantity, unit, ingredient) 
    raw_input()
    return quantity, unit, ingredient 

def get_ingredients(recipes):
    ingredients = [[i for i in r[0]['ingredients']] for r in recipes]
    #print ingredients
    ingredients = [i for sublist in ingredients for i in sublist]
    #print ingredients
    ingredients = map(reduce_ingred, ingredients) 
    # assemble a list of all ingredients and amounts
    # sort list by occurences
    # return list 
    return ingredients 

def make_meta(searchs):
    recipes = get_recipes(searchs)
    print recipes[-5]
    rnames = ''
    metar = {
        '@type': 'Recipe',
        'author': 'Metarecipes',
        'datePublished': date.today().__str__()
    }
    metar['name'] = 'Meta ' + searchs

    # ingredients
    metar['recipeIngredient'] = get_ingredients(recipes)
    
    # instructions
    # description ??
    metar['description'] = 'Metarecipe constructed from: ' + ', '.join(rnames)
    return metar



if __name__ == '__main__':
    print make_meta(sys.argv[1])
