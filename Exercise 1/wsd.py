import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords



def custom_lesk(word, sentence):
    """
    Lesk's algoritm implementation. Given a word and a sentence that contains the given word,
    it returns the best sense of the word.

    :param word: word to disabiguate
    :param sentence: sentence to compare
    :return: best sense for the given word
    """

    word_senses = wn.synsets(word)
    best_sense = word_senses[0]
    max_overlap = 0

    context = bag_of_word(sentence)

    for sense in word_senses:
        signature = bag_of_word(sense.definition())

        examples = sense.examples()
        for ex in examples:
            signature = signature.union(bag_of_word(ex))

        overlap = compute_overlap(signature, context)
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense


def bag_of_word(sent):
    """
    Transforms the given sentence according to the bag of words approach, apply some preprocessing too.

    :param sent: sentence
    :return: bag of words
    """

    stop_words = set(stopwords.words('english'))

    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(sent)
    tokens = list(filter(lambda x: x not in stop_words and x not in string.punctuation, tokens))
    return set(wnl.lemmatize(t) for t in tokens)


def compute_overlap(signature, context):
    """
     Computes the number of words in common between signature and context.
    :param signature: bag of words of the signature (e.g. definitions + examples)
    :param context: bag of words of the context (e.g. sentence)
    :return: number of elements in commons
    """

    return len(signature & context)


def get_sense_index(word, sense):
    """
    Given a ambiguous word and a sense of that word, it returns the
    corresponding index of the sense in the synsets list associated with the
    word indices starts with 1.

    :param word: ambiguous word (sense > 1)
    :param sense: sense of the word
    :return: index of the sense in the synsets list of the word
    """

    senses = wn.synsets(word)
    return senses.index(sense) + 1


def word_sense_disambiguation(sentences):
    res = 0
    cont = 0
    limit = 50
    tot_term_analyzed = 0
    out_list1 = []
    out_list2 = []

    for sentence in sentences:
        if cont == limit:
            break
        cont += 1
        #custom_lesk(sentence[0])
        #sentence[0] è la frase, sentence[1] è la coppia parola-numero
        #term[1] è il golden value
        if len(sentence[1]) > 0:
            #print(sentence[1][0], len(sentence[1]))
            my_sense = custom_lesk(sentence[1][0][0], sentence[0])
            #troviamo l'indice del senso appena trovato nella lista di sensi di WN
            index_val = get_sense_index(sentence[1][0][0], my_sense)

            tot_term_analyzed += 1

            #Output stuff

            annotated_index = int(sentence[1][0][1])
            out_list2.append(get_annotated_syn(sentence, annotated_index))
            out_list1.append(my_sense)
            #print(index_val, annotated_index)
            #print(annotated_index)
            #ann_syn = wn.synsets(sentence[1][0][0])[0]
            #out_list2.append(ann_syn)

            if index_val == int(sentence[1][0][1]):
                res += 1

    return res, tot_term_analyzed, res/tot_term_analyzed*100, out_list1, out_list2


def get_annotated_syn(sentence, syn_index):

    '''
    :param sentence: input sentence
    :param syn_index: annotated index
    :return: synset found at syn_index
    '''
    tot_syn = wn.synsets(sentence[1][0][0])
    annotated_syn = []
    if len(tot_syn) > 0:
        syn = tot_syn[syn_index - 1]
        #print(syn)
    else:
        syn = wn.synsets('entity')

    return syn











