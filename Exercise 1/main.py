from nltk.wsd import lesk
from prettytable import PrettyTable
from scipy.stats import pearsonr, spearmanr
import numpy as np
from CorrelationIndexes import *
from functions import *
from similarity import *
from nltk.corpus import wordnet as wn
from wsd import *

if __name__ == '__main__':
    print("Exercise 1 - Sgaramella Davide")
    print("Similarity Metrics & Correlation indexes")

input_terms = []
input_terms = read_load_csv()

#print(max(len(hyp_path) for hyp_path in wn.synset('dog.n.1').hypernym_paths()))

"Removing the first row of the list which is the title"
input_terms.pop(0)

terms = []
base = []
target = []
gold = []

for t in input_terms:
    terms = t[0].split(',')
    base.append(terms[0])
    target.append(terms[1])
    gold.append(float(terms[2]))



#print(len(base), "Baseline terms", base)
#print(len(target), "Target terms", target)

wup_val = []
lc_val = []
sp_val = []


for i in range(0, len(gold)):
    wup = wup_sim(get_synset(base[i]), get_synset(target[i]))
    #print("WUP Sim value = ", "%.2f" % wup)
    wup_val.append(wup)

    lc = leakcock_chodorow_sim(get_synset(base[i]), get_synset(target[i]))
    #print("LC value = ", "%.2f" % lc)
    lc_val.append(lc)

    sp = shortest_path_sim(get_synset(base[i]), get_synset(target[i]))
    #print("SP value = ", "%.2f" % sp)
    sp_val.append(sp)

pearson_res = []
spearman_res = []


pearson_res.append(pearson_index(gold, wup_val))
pearson_res.append(pearson_index(gold, lc_val))
pearson_res.append(pearson_index(gold, sp_val))

spearman_res.append(spearman_index(gold, wup_val))
spearman_res.append(spearman_index(gold, lc_val))
spearman_res.append(spearman_index(gold, sp_val))


#check(get_synset(base[i]), get_synset(target[i]))
table = PrettyTable(["Base", "Target", "Wup", "LC", "SP", "Gold"])
for i in range(0, len(gold)):
    #print(base[i], target[i], round(wup_val[i], 2), round(lc_val[i], 2), round(sp_val[i], 2), round(gold[i], 2))
    table.add_row([base[i], target[i], round(wup_val[i], 2), round(lc_val[i], 2), round(sp_val[i], 2), round(gold[i], 2)])


'''
Effettuiamo un check dei valori
print("Pearson mio: ", pearson_res)
print("Check")
print(pearsonr(gold, wup_val))
print(pearsonr(gold, lc_val))
print(pearsonr(gold, sp_val))
print("Spearman mio:", spearman_res)
print("Check")
print(spearmanr(gold, wup_val)[0])
print(spearmanr(gold, lc_val)[0])
print(spearmanr(gold, sp_val)[0])

'''

#print(table)
#Check con funzioni built in

path = "Result/"

'''
file1 = open(path+"sim_result.txt", "w") 
file1.write(str(table))
file1.close()


file1 = open(path+"Correlation Index.txt", "w") 
file1.write("Spearman index\n\n")
for s in spearman_res:
    file1.write("\n" + str(s))
file1.write("\n\n\nPearson index\n\n")
for p in pearson_res:
    file1.write("\n" +str(p))

file1.close()
'''


#------------------------------------------------------------------------------------------------------------------#

'''
'''
print("Word Sense Disambiguation")
my_senses = []
annotated_senses = []
parsed = parse_xml("Input/br-j15")


#Frasi per report output
#for p in parsed:
#    print(p[0])

taken, total, perc, my_senses, annotated_senses = word_sense_disambiguation(parsed)
print("Correttezza ", round(perc, 2), " %")
#print("My sense: ", my_senses, "\nAnnotated sense: ", annotated_senses)
print("Correct match: ", taken, "\nTotal: ", total)

'''
wsd_table = PrettyTable(["Result", "Annotated sense"])
for i in range(0, len(my_senses)):
    wsd_table.add_row([my_senses[i], annotated_senses[i]])

for i in range(0, len(my_senses)):
    print("My sense: ", my_senses[i], "Annotated sense: ", annotated_senses[i])

'''

#print(str(wsd_table))
'''
wsd = open(path+"wsd_result.txt", "w")
wsd.write(str(wsd_table))
wsd.close()
'''





