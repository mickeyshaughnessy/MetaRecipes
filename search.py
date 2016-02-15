import sys 
from json import loads
import operator
import re

#import gensim

#model = gensim.models.Word2Vec()
#sentences = gensim.models.word2vec.LineSentence('/data/text8')
#print 'sentences loaded'
#model.build_vocab(sentences)
#print 'vocab built'
#model.train(sentences)
#print 'model trained'
#model.save('text8_model')

#model = gensim.models.Word2Vec.load('/data/gensim_wiki_model')

#print model.most_similar(positive=['woman', 'king'], negative=['man'])
#print model.most_similar(positive=['banana', 'bread'])

def get_recipes(search, db):
    with open(db) as f:
        recipes = []
        for line in f.readlines():
            recipe = loads(line)
            score = compute_match(search, recipe)
            if score > 0:
                recipes.append((recipe, score))
    sorted_r = sorted(recipes, key=operator.itemgetter(1))
    sorted_r.reverse()
    for r in sorted_r:
        print r[0]['name']

def compute_match(search, recipe):
    p = re.compile('('+search.lower()+')')
    result = p.findall((recipe['name'] + recipe['description']).lower()) 
    return len(result)

if __name__ == '__main__':
    # arguments are search string and db file
    get_recipes(sys.argv[1], sys.argv[2])
