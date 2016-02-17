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
	
	Construct meta recipe algorithm:
	1. Get distance from query string to all base recipes.
	2. Construct meta ingredients.
	3. Construct meta directions.
	
	Construct meta ingredients:
	1. compute average ingredient list length.
	2. fill meta ingredients list with the <avg_length> most common ingredients.
	3. Use average amounts for meta ingredients amounts.
	
	Construct meta directions:
		possible steps
	* Preheat
	* Mix1
	* Mix2
	* ...
	* Cook1
	* Cook2
	* ...

	Rules: For each recipe (once) step through directions.
		For each direction, classify it as a step.
			Preheat is usually first direction.
			There can be one or more Mixes ('mix', 'combine', 'together', 'stir',...)
			Cooks usually follow Mixes ('cook', 'heat', 'bake', 'boil', 'hot', 'heat', ...)

	1. Construct meta direction template:
	2. Determine avg number and sequence of each kind of step, ie treat each recipe step sequence as a string ("PreMixMixCookMixCookServe" = "PMMCMC"), and compute the sequence that is the smallest edit distance from all the others in the cluster.
	3. Fill this each step in this sequence with the cluster average in the form:
		* Preheat: "<verb><object><how>", eg "Preheat water boiling" or "Boil water (None)"
		* Mix: "<combine><ing1><ing2>" eg "Mix eggs and vanilla" or "Rub salt and pepper and meat"
		* Cook: "<verb><object><how>" eg "Bake (None) for 1 hour at 250F" or "Boil beans 20 minutes"
	
		For each step in each recipe, project the step into the appropriate form eg - "Heat a lightly oiled griddle or frying pan over medium high heat" -- > Preheat: "<Heat><a lightly oiled griddle or frying pan><over medium high heat>". 
		Then use the most common parts to construct the meta step strings, feed these through the grammar checker and use the top ranking one that passes.
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
