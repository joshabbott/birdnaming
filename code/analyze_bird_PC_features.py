# analyze_bird_PC_features.py

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from math import pi, pow, log
import math
import pickle

import scipy.io as spio
import pandas as pd

from sklearn.metrics import pairwise_distances
from sklearn.manifold import MDS

import time
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA








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

def run_informativeness_on_basic_level(birds):

  bird_pcs = {}
  for bird in birds:
    # bird_features = np.array(pc_data[['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','PC9']][pc_data['Binomial'] == bird.replace(' ','_')])
    bird_features = np.array(pc_data[['PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','PC9']][pc_data['Binomial'] == bird.replace(' ','_')])
    if len(bird_features) > 0:
      bird_pcs[bird] = bird_features


  bird_list = list(bird_pcs.keys())

  simMatrix = createSimMatrix(bird_list,bird_pcs)

  # # need to create lmap['species']['folk_specific']
  # lmap = {}
  # for bird in bird_list:
  #   lmap[bird] = list(df[df['species'] == bird]['folk_specific'])[0] 


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

    return simMatrix, lmap


zapotec_data_all = pd.read_csv('./data/df_zapotec.csv')
df = zapotec_data_all[zapotec_data_all['folk_generic'].notna()] 
# use new dataset
pc_data = pd.read_csv('./data/41559_2019_1070_MOESM3_ESM.csv') 


print("\nhummingbirds")
hummingbirds = list(df[df['folk_generic'] == 'dzǐn̲g']['species'])
# birds = list(df[df['folk_generic'] == 'dzǐn̲g']['species'])
simMatrix, lmap = run_informativeness_on_basic_level(hummingbirds)

# analyze simMatrix

simlabels = list(simMatrix.keys())
simlabels_dict = {}
for i in simlabels:
  curvec = []
  for j in simlabels:
    curvec.append(simMatrix[i][j])

  simlabels_dict[i] = curvec

simlabels_mat = np.array([simlabels_dict[i] for i in simlabels])
sns.heatmap(simlabels_mat.T,cmap="Blues",xticklabels=simlabels,yticklabels=simlabels) 





# 
# TSNE on feature space — are there natural clusters which group the folk specific labels?
# 
# data from morphospace paper
ms = pd.read_csv('./data/41559_2019_1070_MOESM3_ESM.csv')
df = pd.read_csv('./data/df_zapotec.csv')
# make species names match
ms['Binomial'] = ms['Binomial'].str.replace('_',' ')

# pull in PC coordinates
alldf = pd.merge(df, ms, how='left', left_on='species', right_on='Binomial')

# keep only those with PC coords that are named
kddf = alldf[alldf['PC1'].notnull() & alldf['folk_generic'].notnull()]
catlabels = list(kddf['folk_generic'])     


# pull out PC columns
# Xdf = kddf.iloc[:, 12:21]
# dont use PC1 (bird size)
Xdf = kddf.iloc[:, 13:21]

X = Xdf.values

# make tSNE embedding
tsne_results = TSNE(n_components=2, init="pca").fit_transform(X)

# load as dataframe
d = {'tsne1':pd.Series(tsne_results[:,0]),'tsne2':pd.Series(tsne_results[:,1])}
df = pd.DataFrame(d)
df['labels'] = catlabels

# scatter plot
sns.lmplot(x="tsne1",y="tsne2",data=df,fit_reg=False,hue='labels',legend=False)
plt.legend()
plt.show()

# density plot
sns.jointplot(x=df["tsne1"],y=df["tsne2"],kind='kde')
plt.show()



# # tSNE on Leuven features for animals 

# # load animal data
# animal_data = spio.loadmat('kemptypeII.mat',squeeze_me=True)
# # In [101]: animal_data.keys()
# # Out[101]: dict_keys(['__header__', '__version__', '__globals__', 'animals', 'danimals', 
# # 'data', 'freq', 'features', 'dfeatures', 'categories', 'catlabels'])
# animal_names = animal_data['animals']

# train_X = animal_data['data']
# # ndarray  129x764: 98556 elems, type `uint8`, 98556 bytes
# train_categories = animal_data['categories']
# # array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
# #        1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
# #        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
# #        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4,
# #        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5,
# #        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], dtype=uint8)
# catlabels = animal_data['catlabels']
# # array(['mammals', 'birds', 'fish', 'insects', 'reptiles'], dtype=object)



# # set parameters for tSNE
# numdim = 2 # either 2 or 3
# pcadim = 50
# perplexity = 40

# pca_model = PCA(n_components=pcadim)
# pca_result = pca_model.fit_transform(train_X)

# print('Explained variation per principal component (PCA): {}'.format(np.sum(pca_model.explained_variance_ratio_)))


# time_start = time.time()
# tsne = TSNE(n_components=numdim, verbose=1, perplexity=perplexity, n_iter=100000)
# tsne_results = tsne.fit_transform(pca_result)
# # tsne_results = tsne.fit_transform(df.loc[rndperm[:n_sne],feat_cols].values)
# # ndarray        7000x784: 5488000 elems, type `float64`, 43904000 bytes (41.8701171875 Mb)
# print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

# # load as dataframe
# d = {'tsne1':pd.Series(tsne_results[:,0]),'tsne2':pd.Series(tsne_results[:,1])}
# df = pd.DataFrame(d)
# df['labels'] = catlabels[train_categories-1]

# # scatter plot
# sns.lmplot(x="tsne1",y="tsne2",data=df,fit_reg=False,hue='labels',legend=False)
# plt.legend()
# plt.show()

# # density plot
# sns.jointplot(x=df["tsne1"],y=df["tsne2"],kind='kde')
# plt.show()




# # binarize
# # train_X[train_X>1] = 1




# # X_plot = np.linspace(-10, 10, 1000)[:, np.newaxis]
# # X_tsne_2dim = tsne_results
# # # Gaussian KDE
# # kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(X_tsne_2dim)
# # log_dens = kde.score_samples(X_plot)



