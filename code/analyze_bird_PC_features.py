# analyze_bird_PC_features.py

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from math import pi, pow, log
import pickle

import scipy.io as spio
import pandas as pd

from sklearn.metrics import pairwise_distances
from sklearn.manifold import MDS

import time
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA






zapotec_data_all = pd.read_csv('./data/df_zapotec.csv')
df = zapotec_data_all[zapotec_data_all['folk_generic'].notna()] 
# use new dataset
pc_data = pd.read_csv('./data/41559_2019_1070_MOESM3_ESM.csv') 


print("\nhummingbirds")
hummingbirds = list(df[df['folk_generic'] == 'dzǐn̲g']['species'])
# birds = list(df[df['folk_generic'] == 'dzǐn̲g']['species'])
run_informativeness_on_basic_level(hummingbirds)


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
    bird_features = np.array(pc_data[['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8','PC9']][pc_data['Binomial'] == bird.replace(' ','_')])
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












# math functions
def EuclideanDist(x,y):   
    return np.sqrt(np.sum((x-y)**2))

def norm_pdf_multivariate(x, mu, sigma):
  size = len(x)
  if size == len(mu) and (size, size) == sigma.shape:
    det = np.linalg.det(sigma)
    if det == 0:
        raise NameError("The covariance matrix can't be singular")

    norm_const = 1.0/ ( pow((2*pi),float(size)/2) * pow(det,1.0/2) )
    x_mu = np.matrix(x - mu)
    inv = sigma.I        
    result = pow(np.e, -0.5 * (x_mu * inv * x_mu.T))
    return norm_const * result
  else:
    raise NameError("The dimensions of the input don't match")



def getMDScoordinates(X,n_components=2):

  D = pairwise_distances(X)
  # D.shape
  model = MDS(n_components=n_components, dissimilarity='precomputed', random_state=1)
  out = model.fit_transform(D)
  
  plt.scatter(out[:, 0], out[:, 1])
  plt.axis('equal');


# def kde_scipy( vals1, vals2, (a,b), (c,d), N):

#   #vals1, vals2 are the values of two variables (columns)
#   #(a,b) interval for vals1; usually larger than (np.min(vals1), np.max(vals1))
#   #(c,d) -"-          vals2 

#   x=np.linspace(a,b,N)
#   y=np.linspace(c,d,N)
#   X,Y=np.meshgrid(x,y)
#   positions = np.vstack([Y.ravel(), X.ravel()])

#   values = np.vstack([vals1, vals2])
#   kernel = st.gaussian_kde(values)
#   Z = np.reshape(kernel(positions).T, X.shape)

#   return [x, y, Z]



# open bird data
# bird_data = spio.loadmat('../pairwiseSimilarities/birdsims.mat',squeeze_me=True)
bird_data = pickle.load(open("birddata.pkl","rb"))
labels = bird_data['labels']
X_sim = bird_data['sim']
typ_ratings = bird_data['typratings']



# tSNE on Leuven features for animals 

# load animal data
animal_data = spio.loadmat('kemptypeII.mat',squeeze_me=True)
# In [101]: animal_data.keys()
# Out[101]: dict_keys(['__header__', '__version__', '__globals__', 'animals', 'danimals', 
# 'data', 'freq', 'features', 'dfeatures', 'categories', 'catlabels'])
animal_names = animal_data['animals']

train_X = animal_data['data']
# ndarray  129x764: 98556 elems, type `uint8`, 98556 bytes
train_categories = animal_data['categories']
# array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#        1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
#        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4,
#        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5,
#        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], dtype=uint8)
catlabels = animal_data['catlabels']
# array(['mammals', 'birds', 'fish', 'insects', 'reptiles'], dtype=object)



# set parameters for tSNE
numdim = 2 # either 2 or 3
pcadim = 50
perplexity = 40

pca_model = PCA(n_components=pcadim)
pca_result = pca_model.fit_transform(train_X)

print('Explained variation per principal component (PCA): {}'.format(np.sum(pca_model.explained_variance_ratio_)))


time_start = time.time()
tsne = TSNE(n_components=numdim, verbose=1, perplexity=perplexity, n_iter=100000)
tsne_results = tsne.fit_transform(pca_result)
# tsne_results = tsne.fit_transform(df.loc[rndperm[:n_sne],feat_cols].values)
# ndarray        7000x784: 5488000 elems, type `float64`, 43904000 bytes (41.8701171875 Mb)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

# load as dataframe
d = {'tsne1':pd.Series(tsne_results[:,0]),'tsne2':pd.Series(tsne_results[:,1])}
df = pd.DataFrame(d)
df['labels'] = catlabels[train_categories-1]

# scatter plot
sns.lmplot(x="tsne1",y="tsne2",data=df,fit_reg=False,hue='labels',legend=False)
plt.legend()
plt.show()

# density plot
sns.jointplot(x=df["tsne1"],y=df["tsne2"],kind='kde')
plt.show()




# binarize
# train_X[train_X>1] = 1




# X_plot = np.linspace(-10, 10, 1000)[:, np.newaxis]
# X_tsne_2dim = tsne_results
# # Gaussian KDE
# kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(X_tsne_2dim)
# log_dens = kde.score_samples(X_plot)



