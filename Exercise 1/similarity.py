import math

from nltk.corpus import wordnet as wn

max_val = max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())

def get_synset(word):
    '''
    Return the synset for the given word
    :param word:
    :return:
    '''
    synset = wn.synsets(word)
    if not synset:
        return wn.synsets("entity")[0]
    else:
        return synset[0]


def get_depth(syn, lcs):
    '''
    It mesures the distance (depth) between the given Synset and the
    WordNet's root.
    :param syn: synset to reach from the root
    :param lcs: fisrt common sense
    :return: minimum path which contains LCS
    '''
    paths = syn.hypernym_paths()
    # all path containing LCS
    paths = list(filter(lambda x: lcs in x, paths))
    return min(len(path) for path in paths)


def lowest_common_subsumer(syn1, syn2):
    """
    It returns the lowest common ancestor for the two synset
    :param syn1: first word's synset
    :param syn2: second word's synset
    :return: common ancestor's synset
    """

    if syn1 == syn2:
        return syn1

    commons = []
    for h in syn1.hypernym_paths():
        for k in syn2.hypernym_paths():
            zipped = list(zip(h, k))  # merges 2 list in one list of tuples
            common = None
            for i in range(len(zipped)):
                if zipped[i][0] != zipped[i][1]:
                    break
                common = (zipped[i][0], i)

            if common is not None and common not in commons:
                commons.append(common)

    if len(commons) <= 0:
        return None
    #print("Commons: ", commons)
    commons.sort(key=lambda x: x[1], reverse=True)
    return commons[0][0]


def wup_sim(syn1, syn2):
    """
    Implementations of the Wu Palmer metric.
    """

    lcs = lowest_common_subsumer(syn1, syn2)
    if lcs is None:
        return 0
    sim = 2*(get_depth(lcs, lcs)/(get_depth(syn1, lcs)+get_depth(syn2, lcs)))

    return sim*10


def get_distance(syn1, syn2):
    '''
    :param syn1: 1st synset
    :param syn2: 2nd synset
    :return: distance between the given synset
    '''

    lcs = lowest_common_subsumer(syn1, syn2)
    lists_synset1 = syn1.hypernym_paths()
    lists_synset2 = syn2.hypernym_paths()

    if lcs is None:
        return None

    if syn1 == syn2:
        return 0
    # path from LCS to root
    lists_lcs = lcs.hypernym_paths()
    set_lcs = set()
    for elements in lists_lcs:
        for i in elements:
            set_lcs.add(i)

    set_lcs.remove(lcs)  # nodes from LCS (not included) to root

    # path from synset to LCS
    lists_synset1 = list(map(lambda x: [y for y in x if y not in set_lcs], lists_synset1))
    lists_synset2 = list(map(lambda x: [y for y in x if y not in set_lcs], lists_synset2))
    #print(" 1 ", lists_synset1, "\n 2 ", lists_synset2)
    # path containing LCS
    lists_synset1 = list(filter(lambda x: lcs in x, lists_synset1))
    lists_synset2 = list(filter(lambda x: lcs in x, lists_synset2))
    #print(" 1 ", lists_synset1, "\n 2 ", lists_synset2)

    return min(list(map(lambda x: len(x), lists_synset1))) + min(list(map(lambda x: len(x), lists_synset2))) - 2



def shortest_path_sim(syn1, syn2):
    """
    Implementations of the Shortest Path metric.
    """
    len = get_distance(syn1, syn2)
    if len is None:
        return 0

    if len == 0:
        sim = 2*max_val

    if len == 2*max_val:
        sim = 0

    sim = 2*max_val - len
    '''
    Normalization from [0, 2*max_val] to [0,1]
    new_val = (val - lower_bound)/(upper_bound - lower_bound)
    '''
    return (sim/40)*10

def leakcock_chodorow_sim(syn1, syn2):
    """
    Implementations of the Leakcock-Chodorow metric.
    """

    len = get_distance(syn1, syn2)
    if len is None:
        return 0

    if len == 0:
        sim = math.log10((len + 1)/(2*max_val + 1))
    else:
        sim = math.log10(len / (2 * max_val))

    sim = sim * (-1)
    return (sim / (math.log10(2 * max_val + 1))) * 10


def check(syn1, syn2):
    print("Wup", syn1.wup_similarity(syn2))
    print("Lch", syn1.lch_similarity(syn2))
    print("path", syn1.path_similarity(syn2))

