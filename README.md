# MetaRecipes
Code for metarecipe app :shit:

Scrape public recipe and parses the recipe. 
Group recipes by type.
Query recipes by type.
identify base ingredients, variations, cooking method.


[schema.org recipe object](https://schema.org/Recipe)

[structured data testing tool](https://developers.google.com/structured-data/testing-tool/)

* Look at ingredients for a bunch of recipes
example: 'vegan banana bread', 'tri-tip', 'maple banana bread'

input = base dish ([signature ingredients], dish type)
eg, "banana bread"

output = a meta-recipe, which includes basic recipe + variants 
	on recipe return page, apply filters to basic recipe
		filters = (cuisine, restrictions, cooking method, ingredients) 

* Algorithm:
	1. read query string.
	2. return all matching recipes with score.
	3. construct meta recipe.
	4. Display meta recipe + variants.

ToDo:
- [x] build database
- [x] searching the database
- [ ] combine recipes into meta recipe
- [x] crawl for recipe urls
- [x] REST API in front of it.
- [ ] front end for displaying the results
- [ ] filtering the results

API Documentation
---------

All api calls should have the base url: `https://www.metarecipes.com/`

`GET https://www.metarecipes.com/recipes/`:

`GET https://www.metarecipes.com/recipes/<name>`:
    returns the named recipe 

for both of the `.../recipes/` endpoints, both base and meta recipes should be
provided for SEO so that Google can crawl the meta recipes. 

`POST data=searchstring  https://www.metarecipes.com/metasearch`:
    returns a meta recipe (base + variants based on the search string)

-------- 

#Redis
  Redis is a distributed, in-memory key-value store we use as the basic database for recipes.
  A Redis server can be instantiated on the localhost by executing `redis-server` on the command line and leaving the window open.
  On restart the server may need to be restarted.
  To install:
  `conda install redis`
  `conda install redis-py`

------------
different taxonomies:
	ingredients - meat, vegetable, flour, maple, banana, ... 
	cooking method - roast, fry, slow cooker, no cook, bake, ...
	dish type - casserole, bread, salad, meat, ...
	cuisine - thai, italian, syrian, ...
	restrictions - gluten-free, low-fat, kosher, vegan, vegetarian, ...	



example recipe JSON LD
```
<script type="application/ld+json">
{
  "@context": "http://schema.org",
  "@type": "Recipe",
  "author": "John Smith",
  "cookTime": "PT1H",
  "datePublished": "2009-05-08",
  "description": "This classic banana bread recipe comes from my mom -- the walnuts add a nice texture and flavor to the banana bread.",
  "image": "bananabread.jpg",
  "recipeIngredient": [
    "3 or 4 ripe bananas, smashed",
    "1 egg",
    "3/4 cup of sugar"
  ],
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": "http://schema.org/Comment",
    "userInteractionCount": "140"
  },
  "name": "Mom's World Famous Banana Bread",
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "240 calories",
    "fatContent": "9 grams fat"
  },
  "prepTime": "PT15M",
  "recipeInstructions": "Preheat the oven to 350 degrees. Mix in the ingredients in a bowl. Add the flour last. Pour the mixture into a loaf pan and bake for one hour.",
  "recipeYield": "1 loaf"
}
</script>
```
