# MetaRecipes
Code for metarecipe app :shit:

[schema.org recipe object](https://schema.org/Recipe)

[structured data testing tool](https://developers.google.com/structured-data/testing-tool/)


ToDo:
- [x] build database
- [x] searching the database
- [x] combine recipes into meta recipe
- [x] make ingredients list of length = avg length of ingredients returned
- [x] crawl for recipe urls
- [x] REST API in front of it.
- [ ] front end for displaying the results
- [ ] filtering the results on adjectives ('vegan', 'slow-cooker', etc)
- [ ] images (collect and serve)
- [ ] ingredient ratios
- [ ] remove outliers from search results, based on ingredient commonality.
- [ ] scrape http://cookieandkate.com/
- [ ] make metadirections  
- [ ] scrape epicurious.
- [ ] domain name registration.
- [ ] standup full API server.
- [ ] complete frontend design, including extensive flat url structure with cached metarecipes. 
- [ ] initial SEO to establish domain authority
- [ ] add support for other languages

#Meta Recipe Algorithm:

    The idea of the meta recipe is to return a set of meta-ingredients and a set of meta instructions for preparing a dish given a search string.

    Input = search string

    Output = list of ingredients and instructions.

    0. Transform search string to extract filter terms.
    1. For each recipe in the db, score it against the search string. The score is used to construct a exponentially weighted db average (see example).
    2. Compute average ingredient list length, L_avg_.
    3. Fill a ingredient list of length, L_avg_, with the most common ingredients, using serving number weighted avg amounts. 
    4. Construct meta directions and return.
    5. Establish new url endpoint with metarecipe corresponding to search string. 

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

  A running Redis is required for the recipe server to connect to. 

  On laptop restart the server may need to be restarted.
  
  To install:
  `conda install redis`
  `conda install redis-py`

------------

#Notes
different taxonomies:
	ingredients - meat, vegetable, flour, maple, banana, ... 
	cooking method - roast, fry, slow cooker, no cook, bake, ...
	dish type - casserole, bread, salad, meat, ...
	cuisine - thai, italian, syrian, ...
	restrictions - gluten-free, low-fat, kosher, vegan, vegetarian, ...	

Scrape public recipe and parses the recipe. 
Group recipes by type.
Query recipes by type.
identify base ingredients, variations, cooking method.


* Look at ingredients for a bunch of recipes
example: 'vegan banana bread', 'tri-tip', 'maple banana bread'

input = base dish ([signature ingredients], dish type)
eg, "banana bread"

output = a meta-recipe, which includes basic recipe + variants 
	on recipe return page, apply filters to basic recipe
		filters = (cuisine, restrictions, cooking method, ingredients) 

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


# Setup
There are several components to set up.
* screen: `screen -d -m -S shared`, `screen -x shared`
* Install git: sudo `apt-get update`, `sudo apt-get install git`
* 
* make .github credentials and .vimrc right:  

1. Python / Anaconda. Use ` wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh` to conda from the command line. You need to restart your terminal session (ssh out, or open a new window) after installing conda.

2. Redis. You need to install both Redis and the redis-python interface - `conda install redis-py` and `conda install redis`

3. The NLP library we are currently using is pattern, its not available in anaconda so you need to `pip install pattern`

4. You need to start redis in a new screen (eventually we can move it to a dedicated server or cluster): `screen -d -m -S shared`, `screen -x shared`, `<ctrl + a>, c` and `redis-server`. Then a final `<ctrl + a>, n` to get back to a fresh screen.

5. Change the redis settings so it doesn't try to write to disk (only on AWS EC2 server, should be fixed soon). `redis-cli` then `config set stop-writes-on-bgsave-error no`.  

6. The redis needs to be filled - from the `/data/` directory, execute: `python upload_redis.py db_all.json`.

7. To run the webserver, install apache: `sudo apt-get install apache2 apache2-base apache2-mpm-prefork apache2-utils libexpat1 ssl-cert` The `amazonaws.com.conf` file needs to be put in `/etc/apache2/sites-available` and enabled, `sudo a2ensite amazonaws.com` and you should disable the default site `sudo a2dissite 000-default`. Then reload `sudo apachectl restart`.  
