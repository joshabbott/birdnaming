# informativeness-zapotec_scratch.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random

def EuclideanDist(x,y):   
    return np.sqrt(np.sum((x-y)**2))


def createSimMatrix(bird_list,hummingbird_pcs,c=0.1):
	sim = {}
	for i in bird_list:
		sim[i] = {}
		for j in bird_list:
			bird_distsq = EuclideanDist(hummingbird_pcs[i],hummingbird_pcs[j])**2.0

			sim[i][j] = math.exp(-c*bird_distsq)

	return sim


def ERE(lmap,sim,need):
    """
    compute Expected Reconstruction Error for an entire categorical partitioning of the color domain.  
    we are given 
    lmap (a dict containing a label for each chip in the map), 
    sim (a dict of dicts holding a matrix of similarities between each pair of chips i and j), and 
    need (a dict containing need probabilities for each chip), 
    """
    # get your bearings - basic info.
    cnum_list = list(lmap.keys())  # list of chips
    all_cats = set(lmap.values())  # all categories in lmap
    
    # Compute listener distribution for each cat, given current lmap.
    # NB: a clean way to think of this is: for each cat, for each chip j
    # labeled by that cat, we find the sim of that chip to *each* chip i
    # in the entire grid - and we sum those sims across chips j to yield
    # a non-normalized distrib across all chips i - i.e. the sum at each
    # chip i will hold the sum across all j of sim(i,j).  we then normalize 
    # across all chips i.  then repeat for other cats.  then get E.
    ld = {}  # listener distribs, indexed by category

    for cat in all_cats:
        ld[cat] = {chip: 0.0 for chip in cnum_list}
        cat_chipnums = [i for i,x in lmap.items() if x == cat]
        for i in cnum_list:
            ld[cat][i] = np.sum([sim[i][chip_j] for chip_j in cat_chipnums])
        # normalize
        cat_sum = np.sum(list(ld[cat].values()))
        for i in cnum_list:
            # print("ld cat i: ", ld[cat][i], cat_sum)
            ld[cat][i] /= cat_sum


    # now pull this together into ERE.
    E = 0.0
    for chip_i in cnum_list:
        E += need[chip_i]*(-1.0*np.log2(ld[lmap[chip_i]][chip_i]))

    return(E)


def computeRandomShuffles(bird_list,bird_labels,simMatrix,need_probs):

	num_shuffles = 5

	lmap_rand = {}
	evalue_rand = {}
	for i in range(num_shuffles):
		# shuffle labels and recompute E
		# print(i)
		random.shuffle(bird_labels)
		# print(bird_labels)

		lmap_rand[i] = {}
		j=0
		for bird in bird_list:
			lmap_rand[i][bird] = bird_labels[j]
			j+=1
		# print(lmap_rand[i])
		evalue_rand[i] = ERE(lmap_rand[i],simMatrix,need_probs)
		# print("Uniform need probs (RAND): ", evalue_rand[i])

	return evalue_rand



def run_informativeness_on_basic_level(birds):


	bird_pcs = {}
	for bird in birds:
		bird_features = np.array(pc_data[['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','PC9']][pc_data['Binomial'] == bird.replace(' ','_')])
		if len(bird_features) > 0:
			bird_pcs[bird] = bird_features


	bird_list = list(bird_pcs.keys())

	simMatrix = createSimMatrix(bird_list,bird_pcs)

	# # need to create lmap['species']['folk_specific']
	# lmap = {}
	# for bird in bird_list:
	# 	lmap[bird] = list(df[df['species'] == bird]['folk_specific'])[0] 


	# get bird folk specific labels
	bird_labels = []
	for bird in bird_list:
		bird_labels.append(list(df[df['species'] == bird]['folk_specific'])[0])
	bird_labels_orig = bird_labels

	# make label mapping dictionary
	lmap = {}
	i=0
	for bird in bird_list:
		lmap[bird] = bird_labels_orig[i]
		i+=1


	# create need probs with uniform distribution
	uniform_need_probs = {bird: (1.0/len(bird_list)) for bird in bird_list}

	# compute ERE with uniform need probs
	evalue = ERE(lmap,simMatrix,uniform_need_probs)
	print("Uniform need probs (Zapotec birds): "+"{:.4f}".format(evalue))

	# create need probs with ebird relative freqs
	freq_need_probs = {}
	for bird in bird_list:
		freq_need_probs[bird] = float(df[df['species'] == bird]['freq'])
	freq_sum = np.sum(list(freq_need_probs.values()))

	for bird in bird_list:
		freq_need_probs[bird] = freq_need_probs[bird]/freq_sum

	# compute ERE with freq need probs
	evalue_freq = ERE(lmap,simMatrix,freq_need_probs)
	print("Freq need probs (Zapotec birds): "+"{:.4f}".format(evalue_freq))

	# RANDOM SHUFFLES WITH UNIFORM NEED
	# shuffle labels and recompute E
	evalue_rands_uniform = computeRandomShuffles(bird_list,bird_labels,simMatrix,uniform_need_probs)
	print("RAND shuffle with uniform need probs: ")
	for i in evalue_rands_uniform.keys():
		print(""+"{:.4f}".format(evalue_rands_uniform[i]))

	## RANDOM SHUFFLES WITH 
	evalue_rands_freq = computeRandomShuffles(bird_list,bird_labels,simMatrix,freq_need_probs)
	print("RAND shuffle with freq need probs: ")
	for i in evalue_rands_freq.keys():
		print(""+"{:.4f}".format(evalue_rands_freq[i]))




zapotec_data_all = pd.read_csv('./data/df_zapotec.csv')
df = zapotec_data_all[zapotec_data_all['folk_generic'].notna()] 
# use new dataset
pc_data = pd.read_csv('./data/41559_2019_1070_MOESM3_ESM.csv') 




# just need to change this for other birds
# work on just hummingbirds for now
print("\nhummingbirds")
hummingbirds = list(df[df['folk_generic'] == 'dzǐn̲g']['species'])
# birds = list(df[df['folk_generic'] == 'dzǐn̲g']['species'])
run_informativeness_on_basic_level(hummingbirds)

print("\nsparrows")
sparrow_birds = list(df[df['folk_generic'] == 'mtsùu']['species'])
run_informativeness_on_basic_level(sparrow_birds)

print("\nhawks")
hawk_birds = list(df[df['folk_generic'] == 'msì']['species'])
run_informativeness_on_basic_level(hawk_birds)

# bird_pcs = {}
# for bird in birds:
# 	bird_features = np.array(pc_data[['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','PC9']][pc_data['Binomial'] == bird.replace(' ','_')])
# 	if len(bird_features) > 0:
# 		bird_pcs[bird] = bird_features


# bird_list = list(bird_pcs.keys())

# simMatrix = createSimMatrix(bird_list,bird_pcs)

# # # need to create lmap['species']['folk_specific']
# # lmap = {}
# # for bird in bird_list:
# # 	lmap[bird] = list(df[df['species'] == bird]['folk_specific'])[0] 


# # get bird folk specific labels
# bird_labels = []
# for bird in bird_list:
# 	bird_labels.append(list(df[df['species'] == bird]['folk_specific'])[0])
# bird_labels_orig = bird_labels

# # make label mapping dictionary
# lmap = {}
# i=0
# for bird in bird_list:
# 	lmap[bird] = bird_labels_orig[i]
# 	i+=1


# # create need probs with uniform distribution
# uniform_need_probs = {bird: (1.0/len(bird_list)) for bird in bird_list}

# # compute ERE with uniform need probs
# evalue = ERE(lmap,simMatrix,uniform_need_probs)
# print("Uniform need probs (Zapotec birds): ", evalue)

# # create need probs with ebird relative freqs
# freq_need_probs = {}
# for bird in bird_list:
# 	freq_need_probs[bird] = float(df[df['species'] == bird]['freq'])
# freq_sum = np.sum(list(freq_need_probs.values()))

# for bird in bird_list:
# 	freq_need_probs[bird] = freq_need_probs[bird]/freq_sum

# # compute ERE with freq need probs
# evalue_freq = ERE(lmap,simMatrix,freq_need_probs)
# print("Freq need probs (Zapotec birds): ", evalue_freq)

# # RANDOM SHUFFLES WITH UNIFORM NEED
# # shuffle labels and recompute E
# evalue_rands_uniform = computeRandomShuffles(bird_list,bird_labels,simMatrix,uniform_need_probs)
# print("RAND shuffle with uniform need probs: ",evalue_rands_uniform)

# ## RANDOM SHUFFLES WITH 
# evalue_rands_freq = computeRandomShuffles(bird_list,bird_labels,simMatrix,freq_need_probs)
# print("RAND shuffle with freq need probs: ",evalue_rands_freq)

# Uniform need probs (Zapotec hummingbirds):  3.64181785636
# Freq need probs (Zapotec hummingbirds):  3.63785269426
# {'Amazilia beryllina': 'dzǐn̲g-gué', 'Archilochus colubris': 'dzǐn̲g', 'Colibri thalassinus': 'dzǐn̲g', 'Lampornis amethystinus': 'dzǐn̲g-yǎ-guì', 'Calothorax pulcher': 'dzǐn̲g', 'Cynanthus sordidus': 'dzǐn̲g', 'Selasphorus rufus': 'dzǐn̲g-yǎ-guì', 'Lampornis clemenciae': 'dzǐn̲g', 'Eugenes fulgens': 'dzǐn̲g', 'Lamprolaima rhami': 'dzǐn̲g', 'Amazilia viridifrons': 'dzǐn̲g-dán-yǎ-guì', 'Atthis heloisa': 'dzǐn̲g', 'Hylocharis leucotis': 'dzǐn̲g'}
# Uniform need probs (RAND):  3.68415097201
# {'Amazilia beryllina': 'dzǐn̲g', 'Archilochus colubris': 'dzǐn̲g', 'Colibri thalassinus': 'dzǐn̲g', 'Lampornis amethystinus': 'dzǐn̲g', 'Calothorax pulcher': 'dzǐn̲g', 'Cynanthus sordidus': 'dzǐn̲g', 'Selasphorus rufus': 'dzǐn̲g', 'Lampornis clemenciae': 'dzǐn̲g', 'Eugenes fulgens': 'dzǐn̲g-yǎ-guì', 'Lamprolaima rhami': 'dzǐn̲g-yǎ-guì', 'Amazilia viridifrons': 'dzǐn̲g', 'Atthis heloisa': 'dzǐn̲g-gué', 'Hylocharis leucotis': 'dzǐn̲g-dán-yǎ-guì'}
# Uniform need probs (RAND):  3.62016805549
# {'Amazilia beryllina': 'dzǐn̲g-yǎ-guì', 'Archilochus colubris': 'dzǐn̲g', 'Colibri thalassinus': 'dzǐn̲g', 'Lampornis amethystinus': 'dzǐn̲g', 'Calothorax pulcher': 'dzǐn̲g', 'Cynanthus sordidus': 'dzǐn̲g', 'Selasphorus rufus': 'dzǐn̲g-gué', 'Lampornis clemenciae': 'dzǐn̲g-dán-yǎ-guì', 'Eugenes fulgens': 'dzǐn̲g', 'Lamprolaima rhami': 'dzǐn̲g', 'Amazilia viridifrons': 'dzǐn̲g', 'Atthis heloisa': 'dzǐn̲g-yǎ-guì', 'Hylocharis leucotis': 'dzǐn̲g'}
# Uniform need probs (RAND):  3.65236516766
# {'Amazilia beryllina': 'dzǐn̲g', 'Archilochus colubris': 'dzǐn̲g', 'Colibri thalassinus': 'dzǐn̲g', 'Lampornis amethystinus': 'dzǐn̲g', 'Calothorax pulcher': 'dzǐn̲g-gué', 'Cynanthus sordidus': 'dzǐn̲g-dán-yǎ-guì', 'Selasphorus rufus': 'dzǐn̲g', 'Lampornis clemenciae': 'dzǐn̲g', 'Eugenes fulgens': 'dzǐn̲g', 'Lamprolaima rhami': 'dzǐn̲g-yǎ-guì', 'Amazilia viridifrons': 'dzǐn̲g', 'Atthis heloisa': 'dzǐn̲g-yǎ-guì', 'Hylocharis leucotis': 'dzǐn̲g'}
# Uniform need probs (RAND):  3.66301207578
# {'Amazilia beryllina': 'dzǐn̲g', 'Archilochus colubris': 'dzǐn̲g-dán-yǎ-guì', 'Colibri thalassinus': 'dzǐn̲g', 'Lampornis amethystinus': 'dzǐn̲g', 'Calothorax pulcher': 'dzǐn̲g', 'Cynanthus sordidus': 'dzǐn̲g', 'Selasphorus rufus': 'dzǐn̲g-gué', 'Lampornis clemenciae': 'dzǐn̲g', 'Eugenes fulgens': 'dzǐn̲g', 'Lamprolaima rhami': 'dzǐn̲g-yǎ-guì', 'Amazilia viridifrons': 'dzǐn̲g', 'Atthis heloisa': 'dzǐn̲g-yǎ-guì', 'Hylocharis leucotis': 'dzǐn̲g'}
# Uniform need probs (RAND):  3.655989981








