# makedf_zapotec.py
#
# adds density score and 2d embedding (e1, e2) to the zapotec df, which has
# ['species','length','mass','freq','folk_generic','folk_specific','clements_group','prototype']


import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.manifold import TSNE
from scipy.spatial.distance import pdist, squareform

bw = 0.2

# data from morphospace paper
ms = pd.read_csv('41559_2019_1070_MOESM3_ESM.csv')
df = pd.read_csv('df_zapotec.csv')
# make species names match
ms['Binomial'] = ms['Binomial'].str.replace('_',' ')

# pull in PC coordinates
alldf = pd.merge(df, ms, how='left', left_on='species', right_on='Binomial')

# keep only those with PC coords that are named
kddf = alldf[alldf['PC1'].notnull() & alldf['folk_generic'].notnull()]

# keep only those with PC coords that are named and have freq > 0
# kddf = alldf[(alldf['PC1'].notnull()) & (alldf['freq'] > 0) & (alldf['folk_generic'].notnull())]
# keep only those with PC coords that have freq > 0
# keep only those with PC coords that have freq > 2 or named and freq > 0
#kddf = alldf[(alldf['PC1'].notnull()) & ((alldf['freq'] > 2) | ((alldf['freq']>0) & alldf['folk_generic'].notnull()))]
# pull out PC columns

Xdf = kddf.iloc[:, 12:21]
X = Xdf.values

# use PC1 and PC2 as embedding
# X_embedded = X[:, 0:2]

# make tSNE embedding
X_embedded = TSNE(n_components=2, init="pca").fit_transform(X)

## make density using kde (currently unused)
#
#ws = kddf['freq']
#ws = np.log(ws.values)
#ws[ws==0] = 0.5 * np.log(2)
## unweighted for now
#ws[ws >0] = 1
## use kernel density estimation to compute neighborhood density
#kde = KernelDensity(kernel='exponential', bandwidth=bw).fit(X, sample_weight=ws)
#kdescores = kde.score_samples(X)

# define density as number of nearby neighbors in embedding

pwdists = squareform(pdist(X_embedded))
pwdists[pwdists==0] = 100
nndist = np.min(pwdists, axis=1)
# when included only those that are named with freq > 0
nbdist = np.sum(pwdists < 0.5 , axis=1)


kddf = kddf.assign(density = nbdist, e1=X_embedded[:,0], e2=X_embedded[:,1])
kddf = kddf[['species', 'density', 'e1', 'e2']]

finaldf = pd.merge(df, kddf, how='left', on='species')

finaldf.to_csv('df_zapotec_density.csv')

vf = finaldf.sort_values(by='folk_generic')


