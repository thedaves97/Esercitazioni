import csv
import itertools
import re
import xml.etree.ElementTree as ET
from lxml import etree as Exml
from nltk.corpus import wordnet as wn
import random




def read_load_csv():
    '''
    Questa funzione legge il file Csv.
    :return: le definizioni contenute mel file file appena letto.
    '''
    with open('Input\WordSim353.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        terms = []

        for col in csv_reader:
            terms.append(col)

    return terms


def parse_xml(path):
    """
    It parses the SemCor corpus, which has been annotated by hand on WordNet
    Sysnsets.

    In order:
    1) Load XML file
    2) Took all the tags "s"
    3) Extract the sentence
    4) Select the words to disambiguate (select only the needed ones) with
    total number of senses >= 2
    5) Extract Golden annotated sense from WSN

    :param path: the path to the XML file (Brown Corpus)
    :return: [(sentence, [(word, gold)])]
    """

    with open(path, 'r') as fileXML:
        data = fileXML.read()

        # fixing XML's bad formatting
        data = data.replace('\n', '')
        replacer = re.compile("=([\w|:|\-|$|(|)|']*)")
        data = replacer.sub(r'="\1"', data)

        result = []
        try:
            root = Exml.XML(data)
            paragraphs = root.findall("./context/p")
            sentences = []
            for p in paragraphs:
                sentences.extend(p.findall("./s"))
            for sentence in sentences:
                words = sentence.findall('wf')
                sent = ""
                tuple_list = []
                for word in words:
                    w = word.text
                    pos = word.attrib['pos']
                    sent = sent + w + ' '
                    if pos == 'NN' and '_' not in w \
                            and len(wn.synsets(w)) > 1 \
                            and 'wnsn' in word.attrib:
                        sense = word.attrib['wnsn']
                        t = (w, sense)
                        tuple_list.append(t)
                result.append((sent, tuple_list))
        except Exception as e:
            raise NameError('xml: ' + str(e))
    return result


def rand_index():
    r_ind = []
    try:
        r_ind = random.sample(range(0, 90), 50)
    except ValueError:
        print('Sample size exceeded population size.')

    return r_ind


def get_index(word, sense):
    """
    Given a ambiguous word and a sense of that word, it returns the
    corresponding index of the sense in the synsets list associated with the
    word indices starts with 1.

    :param word: ambiguous word (with more that 1 sense)
    :param sense: sense of the word
    :return: index of the sense in the synsets list of the word
    """

    senses = wn.synsets(word)
    return senses.index(sense) + 1


def write_file():
    file1 = open("result.txt", "a")  # append mode
    file1.write("")
    file1.close()