# MetaRecipes
code for metarecipe app

[schema.org recipe object](https://schema.org/Recipe)

[structured data testing tool](https://developers.google.com/structured-data/testing-tool/)

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
