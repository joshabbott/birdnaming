# makedf_zapotec.py
#
# creates pandas df with columns:
# ['species','length','mass','freq','folk_generic','folk_specific','clements_group','prototype']


import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity

bw = 0.2

# data from morphospace paper
ms = pd.read_csv('41559_2019_1070_MOESM3_ESM.csv')
df = pd.read_csv('df_zapotec.csv')
# make species names match
ms['Binomial'] = ms['Binomial'].str.replace('_',' ')

# pull in PC coordinates
alldf = pd.merge(df, ms, how='left', left_on='species', right_on='Binomial')
# keep only those with PC coords that are named and have freq > 0
#kddf = alldf[(alldf['PC1'].notnull()) & (alldf['freq'] > 0) & (alldf['folk_generic'].notnull())]
# keep only those with PC coords that have freq > 0
kddf = alldf[(alldf['PC1'].notnull()) & (alldf['freq'] > 0)]
# pull out PC columns
Xdf = kddf.iloc[:, 12:21]
X = Xdf.values
ws = kddf['freq']
ws = np.log(ws.values)
ws[ws==0] = 0.5 * np.log(2)
# effectively unweighted for now
ws[ws >0] = 1
# use kernel density estimation to compute neighborhood density
kde = KernelDensity(kernel='exponential', bandwidth=bw).fit(X, sample_weight=ws)
kdescores = kde.score_samples(X)

kddf = kddf.assign(density = kdescores)
kddf = kddf[['species', 'density']]

finaldf = pd.merge(df, kddf, how='left', on='species')

finaldf.to_csv('df_zapotec_density.csv')



