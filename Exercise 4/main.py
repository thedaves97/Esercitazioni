from sklearn.metrics import cohen_kappa_score
from scipy.stats import pearsonr, spearmanr

from functions import *

if __name__ == '__main__':

    print("Exercise 4")
    # Creazione risorsa Nasari
    nasari = get_nasari()
    # Viene richiamato il metodo che restituisce i dati da analizzare presi da un file "..\\dati.tsv".

    file = ["dati.tsv", "dati2.tsv"]
    #name = folder + "dati1.tsv"

    data = read_load_file(file[0])

    gold = get_italian_synset()
    # print(gold)
    my_score = []

    data2 = read_load_file(file[1])
    my_score2 = []
    for row in data2:
        my_score2.append(float(row[2]))
    #print(my_score2)

    # inter rate tra mio e gold
    base, target = [], []
    for row in data:
        base.append(row[0].lower())
        target.append(row[1].lower())
        my_score.append(float(row[2]))
    sim = []
    # print(base, "\n", target)
    gold_score = []

    for i in range(0, len(base)):
        # print(gold[base[i]])
        # print(gold[target[i]])

        (s1, s2), score = similarity_vector(gold[base[i]], gold[target[i]])
        gold_score.append(score)
        #print((s1, s2), score)

    pearson_res = []
    spearman_res = []
    gg = []
    conf = type(0.1)
    for g in gold_score:
        if type(g) is not conf:
           gg.append(float(g))

    gold_score = gg
    '''
    Check del tipo
    for g in gg:
        print(g, type(g))
    '''

    #inter rate agreement tra prima annotazione e seconda
    print("Inter-rate agreement")
    print("Spearman: ", spearmanr(my_score, my_score2)[0])
    print("Pearson: ", pearsonr(my_score, my_score2)[0])

    # confronto tra my_score e score (di gold)
    print("Evaluation between human annotation and scores retrieved")
    pearson_res.append(pearsonr(gold_score, my_score)[0])
    spearman_res.append(spearmanr(gold_score, my_score)[0])
    print("Spearman: ", spearman_res)
    print("Pearson: ", pearson_res)



    # -------------------------------------------------------------------------------------------------#

    #Task 2

    res = []
    res2 = []
    for el in my_score:
        res.append(int(el))
    for el in my_score2:
        res2.append(int(el))

    my_score = res
    my_score2 = res2

    k = cohen_kappa_score(my_score, my_score)
    print("Cohen: ", k)




        with open("Output/results.tsv", "w", encoding="utf-8") as out:
        for i in range(0, len(base)):
            (s1, s2), _ = similarity_vector(gold[base[i]], gold[target[i]])
            if s1 is not None and s2 is not None:
                out.write("{}\t{}\t{}\t{}\t".format(base[i], target[i], s1, s2))

                terms_1 = get_synset_terms(s1)
                terms_2 = get_synset_terms(s2)
                nasari_terms_1 = ""
                nasari_terms_2 = ""

                for out1 in terms_1:
                    if out1 != terms_1[len(terms_1) - 1]:
                        out.write(out1 + ",")  # if not the last term, put a ","
                        nasari_terms_1 += out1 + ","
                    else:
                        out.write(out1 + "\t")  # otherwise put a separator
                        nasari_terms_1 += out1

                for out2 in terms_2:
                    if out2 != terms_2[len(terms_2) - 1]:
                        out.write(out2 + ",")  # if not the last term, put a ","
                        nasari_terms_2 += out2 + ","
                    else:
                        out.write(out2 + "\n")  # otherwise put a separator
                        nasari_terms_2 += out2
            else:
                out.write("{}\t{}\tNone\tNone\tNone\tNone\n".format(base[i], target[i]))


