from functions import *
from nltk.corpus import wordnet as wn

'''
Class not used, only for test purposes 
'''

def get_ant(syn):
    ant = []
    for s in syn:
        a = s.lemmas()[0].antonyms()
        ant.append(a)
    ant = filter(None, ant)
    lem_ant = []
    for an in ant:
        ant_lemma = an[0].key().split("%")[0]
        lem_ant.append(ant_lemma)
    ant_fin = []

    for a in lem_ant:
        syn = get_synset(a)
        for s in syn:
            defintion = get_syn_definition(s)
    return lem_ant

if __name__ == '__main__':
    syn = get_synset("dead")
    #print(syn)
    a = syn[0].lemmas()[0].antonyms()
    #print(a[0].lemmas())

    dead = syn[0].lemmas()[0].antonyms()
    #print(dead)
    a = dead[0].key().split("%")[0]
    #print(a)
    ant_syn = get_synset(a)
    for s in ant_syn:
        defintion = get_syn_definition(s)
        defintion = preprocessing("", defintion)
        #print(defintion)

    #print(get_syn_definition(get_synset(a)))
    #good = wn.synset('good.a.01')
    #print(good.lemmas()[0].antonyms())
    #print(good[0].lemmas().antonyms())

    print(get_ant(syn))
    a = 0
    b = 0.0

    if a != b:
        print("Uguali")