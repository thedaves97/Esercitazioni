import csv
import json
import re
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

diz = dict()


def get_italian_synset():
    """
    It read SemEvalIT17 file. Each italian term is associated with a list of BabelID.
    :return: a dictionary containing the italian word followed by the list of
    its BabelID. Format: {word_it: [BabelID]}
    """

    sem_dict = {}
    synsets = []
    term = "first_step"  # only for the first time
    with open("Input/SemEval17_IT_senses2synsets.txt", 'r', encoding="utf8") as file:
        for line in file.readlines():
            line = line[:-1].lower()
            if "#" in line:
                line = line[1:]
                if term != "first_step":  # only for the first time
                    sem_dict[term] = synsets
                term = line
                synsets = []
            else:
                synsets.append(line)
    return sem_dict

def get_synset_terms(sense):
    """
    It use the BabelNet HTTP API for getting the first three Lemmas of the word
    associated to the given Babel Synset ID.
    :param sense: sense's BabelID
    :return: the first three lemmas of the given sense. An error string if
    there are none
    """

    url = "https://babelnet.io/v5/getSynset"
    params = {
        "id": sense,
        "key": "30f75681-617a-45a4-b2c9-1aede0ad5640",
        "targetLang": "IT"
    }

    req = requests.get(url=url, params=params)
    data = req.json()

    synset_terms = []

    i = 0  # used to loop over the first three terms
    j = 0  # used to loop over all the senses
    while j < len(data["senses"]) and i < 3:
        term = data["senses"][j]["properties"]["fullLemma"]
        term = re.sub('\_', ' ', term).lower()

        if term not in synset_terms:
            synset_terms.append(term)
            i += 1

        j += 1

    if len(synset_terms) == 0:
        return "Empty synset terms"
    else:
        return synset_terms


def read_load_file(name):

    file = open("Input/"+name, 'r', encoding='utf-8-sig')
    read_tsv = csv.reader(file, delimiter="\t")
    list = []
    for line in read_tsv:
        list.append(line)
    file.close()
    return list


def similarity_vector(babel_id_word1, babel_id_word2):
    """
    It computes the cosine similarity between the two given NASARI vectors
    (with Embedded representation).
    :param babel_id_word1: list of BabelID of the first word
    :param babel_id_word2: list of BabelID of the second word
    :param nasari_dict: NASARI dictionary
    :return: the couple of senses (their BabelID) that maximise the score and
    the cosine similarity score.
    """

    max_value = 0
    senses = (None, None)
    for bid1 in babel_id_word1:
        for bid2 in babel_id_word2:
            if bid1 in diz.keys() and bid2 in diz.keys():
                # Storing the NASARI values of bid1 and bid2
                v1 = diz[bid1]
                v2 = diz[bid2]

                # Transforming the V1 and V2 array into a np.array (numpy array).
                # Array dimensions: 1 x len(v).
                n1 = np.array(v1).reshape(1, len(v1))
                n2 = np.array(v2).reshape(1, len(v2))

                # Computing and storing the cosine similarity.
                val = cosine_similarity(n1, n2)[0]
                if val > max_value:
                    max_value = val
                    senses = (bid1, bid2)

    return senses, max_value


def get_nasari():
    global diz
    file = open("Input/mini_NASARI.tsv", 'r', encoding= 'utf8')
    read_tsv = csv.reader(file, delimiter="\t")
    for line in read_tsv:
        diz[line[0].split('_')[0]] = line[1:]
    file.close()
    #print(diz)


