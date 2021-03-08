from functions import *
from lib import *

if __name__ == '__main__':
    print("Exercise 2")

    #student: Sgaramella
    #ID: 1660 	frame: Artificiality
    #ID:  310 	frame: Dead_or_alive
    #ID:  403 	frame: Achieving_first
    #ID: 2041 	frame: Cause_emotion
	#ID:  407 	frame: Importance

    #student: sgaramella
	#ID: 2481 	frame: Erasing
	#ID: 1790 	frame: Means
	#ID: 2916 	frame: Distributed_abundance
	#ID:   37 	frame: Hearsay
	#ID: 1816 	frame: Removing_scenario

    #student: SGARAMELLA
	#ID: 1850 	frame: Carry_goods
	#ID:   26 	frame: Expectation
	#ID:  880 	frame: Being_in_operation
	#ID: 1594 	frame: Continued_state_of_affairs
	#ID:  284 	frame: Mass_motion


frame_id = [1660, 310, 403, 2041, 407]
#frame_id = [2481, 1790, 2916, 37, 1816]
#frame_id = [1850, 26, 880, 1594, 284]

ctx_f = []
ctx_w = {}
cont = 0

fn = []
fe = []
lu = []

for id in frame_id:
    '''
    if cont==1:
        break
    '''
    cont += 1

    #print("---------------------------------------------FRAME ", cont, "----------------------------------------------------\n")
    #print("---------------------------------------------FRAME NAMES--------------------------------------------------\n")
    f = get_frame(id)
    #print(preprocessing(get_main_clause(f.name), f.definition))
    syn = get_synset(get_main_clause(f.name))

    fn.append(preprocessing(get_main_clause(f.name), f.definition))

    #print("---------------------------------------------FRAME ELEMENTS----------------------------------------------\n")
    #print("Total FE: ", f.FE)
    for key in f.FE:
        definition = f.FE[key].definition
        mc = get_main_clause(key)
        #print(preprocessing(get_main_clause(key), definition))
        syn = get_synset(mc)

        fe.append(preprocessing(mc, definition))
    #print("---------------------------------------------LEXICAL UNITS------------------------------------------------\n")
    for key in f.lexUnit:
        lu_key = re.sub('\.[a-z]+', '', key)
        #print(lu_key)
        mc = get_main_clause(lu_key)
        #print(preprocessing(mc, f.lexUnit[key].definition))
        syn = get_synset(mc)
        definition = f.lexUnit[key].definition

        lu.append(preprocessing(mc, definition))

    #ctx_f, ctx_w = create_ctx(f)



#print("------------------------------------------------------------------------------------------------------------")
#print("------------------------------------------------------------------------------------------------------------")
#print("------------------------------------------------------------------------------------------------------------")

path = ['Input/FN_gold.csv', 'Input/FE_gold.csv', 'Input/LU_gold.csv']

fn_gold = read_load_csv(path[0])
fe_gold = read_load_csv(path[1])
lu_gold = read_load_csv(path[2])

ctx = []


mine = []
#print(wn.synsets(fn_gold[0][0]))
for i in range(0, len(fn_gold)):
    syn = wn.synsets(fn_gold[i][0])
    #print(fn_gold[i][0], syn)
    #print(wn.synsets(fn_gold[i][0]))
    score, s = bag_of_word(fn[i], syn)
    #print(s, fn_gold[i][1])
    mine.append(s)

for i in range(0, len(fe_gold)):
    syn = wn.synsets(fe_gold[i][0])
    #print(fn_gold[i][0], syn)
    #print(wn.synsets(fn_gold[i][0]))
    score, s = bag_of_word(fe[i], syn)
    #print(s, fe_gold[i][1])
    mine.append(s)

for i in range(0, len(lu_gold)):
    syn = wn.synsets(lu_gold[i][0])
    #print(fn_gold[i][0], syn)
    #print(wn.synsets(fn_gold[i][0]))
    score, s = bag_of_word(lu[i], syn)
    #print(s, lu_gold[i][1])
    mine.append(s)

gold = fn_gold + fe_gold + lu_gold
effective = 0
for i in range(0, len(mine)):
    #print(gold[i][1])
    stripped = remove_quotes(gold[i][1])
    synset = create_syn(stripped)
    #print(synset, mine[i])
    mine[i] = str(mine[i]).replace("Synset('", '')
    mine[i] = str(mine[i]).replace("')", '')
    #print(type(mine[i]), type(stripped))
    #print(type(mine[i]))
    if mine[i] != "None":
        effective += 1

    if mine[i] == stripped:
        cont += 1
print("cont:", cont, "effective: ", effective)
print("Res: ", (cont/effective)*100)




