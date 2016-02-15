import sys 
import gensim

model = gensim.models.Word2Vec()
sentences = gensim.models.word2vec.LineSentence('/data/text8')
print 'sentences loaded'
model.build_vocab(sentences)
print 'vocab built'
model.train(sentences)
print 'model trained'
model.save('text8_model')

#model = gensim.models.Word2Vec.load('/data/gensim_wiki_model')

print model.most_similar(positive=['woman', 'king'], negative=['man'])
print model.most_similar(positive=['banana', 'bread'])

def get_recipes(search, db):
    pass
    # for recipe in db:
        # compute match_score(search, recipe)
    # sort scores and return

def compute_match(search, recipe):
    pass
    # compute word2vec similarity between search the top N keywords in recipe
    # return similarity score

if __name__ == '__main__':
    # arguments are search string and db file
    get_recipes(sys.argv[1], sys.argv[2])
