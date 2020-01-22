import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# some useful functions
def get_birdcounts(ebd_data):
	# read ebird count and name data
	bird_counts = {}

	science_name = list(ebd_data['SCIENTIFIC NAME'])

	i=0
	for bird_name in science_name:
		if bird_name in bird_counts.keys():
			bird_counts[bird_name] +=1
		else:
			bird_counts[bird_name] = 1

		i+=1

	return bird_counts




# read zapotec data
df = pd.read_csv('./data/df_zapotec.csv')

# load ebird data
ebd_data = pd.read_csv('./data/ebird_MX-OAX_relJul-2019_clean.csv')
# get bird counts, index by species name
bird_counts = get_birdcounts(ebd_data)



#
# ANALYSES
#


# what categories are given a name?

# violin plot (with log frequency of occurrence)

bird_list = list(df['species']) 
freqs = list(df['freq'])

data_zapotec = [np.log(i) for i in freqs if i >0]
data_all = [np.log(i) for i in bird_counts.values()]

missing_data = []
for birdcount in bird_counts.keys():
	if birdcount not in bird_list:
		missing_data.append(np.log(bird_counts[birdcount]))

pos = [1,2,3]
plotnames = ('Zapotec','Missing','All OAX')
plt.figure()
plt.violinplot([data_zapotec,missing_data,data_all],pos) 
plt.title('Frequency densities of Zapotec')
plt.xticks(pos,plotnames)
plt.ylabel('Log frequency of occurence')

plt.show()
















names = list(df['folk_specific'])
freqs = list(df['freq'])
             
xs = [len(i) for i in names]
ys = freqs
plt.figure()
plt.scatter(xs,ys)
plt.ylabel('Frequency counts')
plt.xlabel('Zapotec name length')
plt.show()

# In[170]:


slope, intercept, r_value, p_value, std_err = linregress(xs, ys)
print("slope: %f    intercept: %f" % (slope, intercept))
print("R-squared: %f" % r_value**2)


# ## relationship between length and mass

# In[171]:


# check relationship between length and mass
xs = list(df['length'])
ys = list(df['mass'])
plt.figure()
plt.scatter(xs,ys)
plt.ylabel('Body Masses')
plt.xlabel('Body Length')
plt.show()


slope, intercept, r_value, p_value, std_err = linregress(xs, ys)
print("slope: %f    intercept: %f" % (slope, intercept))
print("R-squared: %f" % r_value**2)


# ## Monomial label frequencies vs. Compound label frequencies

# In[192]:


monomials = []
compounds = []
for i in range(len(names)):
    if len(names[i].split('-')) > 1:
        if freqs[i] > 0:
            compounds.append(freqs[i])
    else:
        if freqs[i] > 0:
            monomials.append(freqs[i])


# In[193]:


np.mean(np.log(compounds))


# In[194]:


np.mean(np.log(monomials))


# In[195]:


# violin plot 
data_compounds = [np.log(i) for i in compounds]
data_monomials = [np.log(i) for i in monomials]

pos = [1,2]
plotnames = ('Compounds','Monomials')
plt.figure()
plt.violinplot([data_compounds,data_monomials],pos)
plt.title('Frequency densities of Zapotec name forms')
plt.xticks(pos,plotnames)
plt.ylabel('Log frequency of occurence')
plt.show()

# ## monomial vs. compound analysis with mass

# In[196]:


# do the same with mass
mass = list(df['mass'])

monomials = []
compounds = []
for i in range(len(names)):
    if len(names[i].split('-')) > 1:
        compounds.append(mass[i])
    else:
        monomials.append(mass[i])


# In[197]:


np.mean(np.log(compounds))


# In[199]:


np.mean(np.log(monomials))


# In[200]:


# violin plot 
data_compounds = [np.log(i) for i in compounds]
data_monomials = [np.log(i) for i in monomials]

pos = [1,2]
plotnames = ('Compounds','Monomials')
plt.figure()
plt.violinplot([data_compounds,data_monomials],pos)
plt.title('Mass densities of Zapotec name forms')
plt.xticks(pos,plotnames)
plt.ylabel('Log Mass')
plt.show()

# ## What birds are named?

# In[157]:


# violin plot (with log frequency of occurrence)
freqs = list(df['freq'])
data_zapotec = [np.log(i) for i in freqs if i >0]
data_all = [np.log(i) for i in bird_counts.values()]

missing_data = []
for birdcount in bird_counts.keys():
	if birdcount not in bird_list:
		missing_data.append(np.log(bird_counts[birdcount]))

pos = [1,2,3]
plotnames = ('Zapotec','Missing','All OAX')
plt.figure()
plt.violinplot([data_zapotec,missing_data,data_all],pos) 
plt.title('Frequency densities of Zapotec')
plt.xticks(pos,plotnames)
plt.ylabel('Log frequency of occurence')
plt.show()