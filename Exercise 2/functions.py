import csv
import string

import nltk
from nltk.corpus import framenet as fn
import re
from nltk.corpus import wordnet as wn
import spacy
from nltk.corpus import stopwords


stop_words = stopwords.words('english')
numbers = [1,2,3,4,5,6,7,8,9,0]
nlp = spacy.load("en_core_web_sm")


def read_load_csv(path):
    '''
    Questa funzione legge il file Csv.
    :return: le definizioni contenute mel file file appena letto.
    '''
    cont = 0
    with open(path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        definitions = []
        for row in csv_reader:
            definitions.append(row)
    return definitions


def get_frame(frame_id):
    f = fn.frame_by_id(frame_id)

    return f


def get_main_clause(frame_name):
    """
    Get of the main clause from the frame name ("reggente").
    :param frame_name: the name of the frame
    :return: the main clause inside the frame name
    """
    mc = ""
    if '-' or '_' in frame_name:
        frame_name = frame_name.replace('_' or '-', ' ')
        frame_name = nlp(frame_name)
        for t in frame_name:
            #print(t.text, t.lemma_, t.pos_, t.tag_, t.dep_, t.shape_, t.is_alpha, t.is_stop)
            if t.tag_ == "NN" or t.tag_ == "NNS":
                mc = t.text
            else:
                if t.dep_ == 'ROOT':
                    mc = t.text
        return mc
    else:
        return frame_name


def get_synset(word):
    synset = wn.synsets(word)
    if synset == "":
        return "No synset"
    else:
        return synset


def get_syn_definition(syn):
    return syn.definition()


def preprocessing(name, sent):
    '''

    :param name: FE/LU's name
    :param sent: FE/LU's definition
    :return:
    '''
    processed = []
    other_str = ["fe", "fn", "cod", "'", "$"]
    processed.append(name.lower())
    #print(sent)
    sent = sent.lower()

    sent = nlp(sent)

    for t in sent:
        #print(t.text, t.lemma_, t.pos_, t.tag_, t.dep_, t.shape_, t.is_alpha, t.is_stop)
        if not t.is_stop:
            if t.pos_ != "PUNCT" and t.pos_ != "NUM":
                processed.append(t.lemma_)

    processed = list(filter(lambda x: x not in other_str, processed))
    #print(processed)

    #----------------------------------------------------------------------------------------------------------#

    #sent = list(filter(lambda x: x not in string.punctuation, sent))
    #sent = [''.join(c for c in s if c not in string.punctuation and not c.isdigit()) for s in sent]
    #sent = list(filter(lambda x: x not in stop_words and x not in other_str, sent))

    return processed


def bag_of_word(bag, syn):
    '''
    :param bag: program's result
    :param gold: synset annotation
    :param syn: processed synset
    :return:
    '''
    lista = []
    bag = list(filter(None, bag))
    ctx_to_use = []
    max_score = 0
    best_syn = None
    if len(syn) > 1:
        for s in syn:
            #print(s)
            ctx = get_context(s)
            ctx = list(filter(None, ctx))

            score = len(set(bag).intersection(ctx)) + 1
            best_syn = s
            if score > max_score:
                max_score = score
                best_syn = s
    else:
        #print(syn)
        ctx = get_context(syn[0])       #[0] necessario perchè altrimenti rimane in formato list e porta ad errori
        ctx = list(filter(None, ctx))
        #ctx = list(filter(" ", ctx))
        score = len(set(bag).intersection(ctx)) + 1
        max_score = score
        best_syn = syn

    return max_score, best_syn


def get_context(syn):
    '''
    Given a synset, it returns the context for the synset
    :param syn: synset processed
    :return: context for the given siynset
    '''
    syn_def = []
    examples = []
    definition = syn.definition()
    examples = get_examples(syn)
    syn_def = preprocessing("", definition)

    #aggiungere iponimi iperonimi
    limit = 0
    hyp = syn.hyponyms()
    hyp_list = []
    sub_def = []
    if hyp !=0:
        for h in hyp:
            if limit == 3:
                break
            sub_def.append(preprocessing("", h.definition()))

            hyp_list = get_examples(h)

            limit+=1
        #print(hyp_list)
            limit = 0
    hyper = syn.hypernyms()
    hyper_list = []
    if hyper != 0:
        for h in hyper:
            if limit == 3:
                break
            sub_def.append(preprocessing("", h.definition()))
            hyper_list = get_examples(h)
            limit += 1
    #print(sub_def)

    sub_def = [item for sub_list in sub_def for item in sub_list]

    return examples + syn_def + sub_def + hyp_list + hyper_list

def get_examples(syn):
    examples = []
    if syn.examples():
        for ex in syn.examples():
            examples.append(preprocessing("", ex))

    flat_list = [item for sub_list in examples for item in sub_list]

    return flat_list


def remove_quotes(stringa):
    #if they only occur at start and end...
    return stringa.strip("\'")


def create_syn(word):
    a = "Synset('"
    b = "')"
    c = a + word + b
    return c

