import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

plt.rcParams.update({'font.size': 14})

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


def get_basiclevel(zapotec_data):
	bird_sci2basic_names = {}

	basic_name = list(zapotec_data['folk_generic'])
	science_name = list(zapotec_data['species'])

	i=0
	for bird_name in science_name:
		bird_sci2basic_names[bird_name] = basic_name[i]
		i+=1

	return bird_sci2basic_names


# make the same plot but with bird masses
def get_birdmass(bird_name,bird_mass_df):
	try:
		mass = float(bird_mass_df['BodyMass-Value'][bird_mass_df['Scientific'] == bird_name]) 
	except:
		mass = 0
	return mass




# read zapotec data
df = pd.read_csv('./data/df_zapotec.csv')

# load ebird data
ebd_data = pd.read_csv('./data/ebird_MX-OAX_cogsci_clean.csv')
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



# plt.figure(figsize=(9, 4), dpi=100, facecolor='w', edgecolor='k')

# plt.subplot(1,2,1)

pos = [1,2,3]
plotnames = ('Zapotec','Missing','All OAX')
# plt.figure()
plt.violinplot([data_zapotec,missing_data,data_all],pos) 
plt.title('Frequency densities of OAX')
plt.xticks(pos,plotnames)
plt.ylabel('Log frequency')

plt.tight_layout()
plt.show()




bigbirddata_data = pd.read_csv('./data/BirdFuncDat.txt',sep='\t',encoding = "ISO-8859-1")
bird_mass_df = bigbirddata_data[['BodyMass-Value','Scientific']]


basic_levels = get_basiclevel(df)


zapotec_masses = {}
for zapotec_bird in basic_levels.keys():
	mass = get_birdmass(zapotec_bird,bird_mass_df)
	if mass > 0:
		zapotec_masses[zapotec_bird] = mass

oax_masses = {}
for oax_bird in bird_counts.keys():
	mass = get_birdmass(oax_bird,bird_mass_df)
	if mass > 0:
		oax_masses[oax_bird] = mass
        
        
data_zapotec = [np.log(i) for i in zapotec_masses.values()]
data_all = [np.log(i) for i in oax_masses.values()]

missing_data = []
for birdmass in oax_masses.keys():
	if birdmass not in zapotec_masses.keys():
		missing_data.append(np.log(oax_masses[birdmass]))

# plt.subplot(1,2,2)
pos = [1,2,3]
plotnames = ('Zapotec','Missing','All OAX')
# plt.figure()
plt.violinplot([data_zapotec,missing_data,data_all],pos) 
plt.title('Mass densities of Zapotec')
plt.xticks(pos,plotnames)
plt.ylabel('Log mass')


plt.tight_layout()
plt.show()










names = list(df['folk_specific'])
freqs = list(df['freq'])
             
xs = [len(i) for i in names]
ys = freqs
plt.figure()
plt.scatter(np.log(xs),np.log(ys))
plt.ylabel('Log Frequency counts')
plt.xlabel('Log Zapotec name length')

plt.tight_layout()
plt.show()

# In[170]:


slope, intercept, r_value, p_value, std_err = linregress(xs, ys)
print("slope: %f    intercept: %f" % (slope, intercept))
print("R-squared: %f" % r_value**2)


# ## relationship between length and mass

# In[171]:


# # check relationship between length and mass
# xs = list(df['length'])
# ys = list(df['mass'])
# plt.figure()
# plt.scatter(xs,ys)
# plt.ylabel('Body Masses')
# plt.xlabel('Body Length')
# plt.show()


# slope, intercept, r_value, p_value, std_err = linregress(xs, ys)
# print("slope: %f    intercept: %f" % (slope, intercept))
# print("R-squared: %f" % r_value**2)


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
plt.figure(figsize=(9, 4), dpi=100, facecolor='w', edgecolor='k')

plt.subplot(1,2,1)

# violin plot 
data_compounds = [np.log(i) for i in compounds]
data_monomials = [np.log(i) for i in monomials]

pos = [1,2]
plotnames = ('Compounds','Monomials')
# plt.figure()
plt.violinplot([data_compounds,data_monomials],pos)
plt.title('Frequency densities of name forms')
plt.xticks(pos,plotnames)
plt.ylabel('Log frequency')
# plt.show()

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

plt.subplot(1,2,2)
pos = [1,2]
plotnames = ('Compounds','Monomials')
# plt.figure()
plt.violinplot([data_compounds,data_monomials],pos)
plt.title('Mass densities of name forms')
plt.xticks(pos,plotnames)
plt.ylabel('Log Mass')




plt.tight_layout()
plt.show()






# 
# PROTOTYPE analysis
# 

plt.rcParams.update({'font.size': 12})

def get_barheights_freq(bar_species,bird_list,df):
	heights = []
	for bird_name in bar_species:
		if bird_name in bird_list:
			heights.append(float(df[df['species'] == bird_name]['freq']))
		else:
			heights.append(0.0)

	return heights


prototypes = ['Cathartes aura','Buteo jamaicensis','Columba livia',
'Bubo virginianus','Thryomanes bewickii',
'Haemorhous mexicanus']

# read zapotec data
df = pd.read_csv('./data/df_zapotec.csv')

plt.figure(figsize=(12, 6), dpi=100, facecolor='w', edgecolor='k')

plt.subplot(2, 3, 1)
# vultures (3)
bar_species = ['Cathartes aura','Coragyps atratus','Sarcoramphus papa']
bar_labels = ('Turkey','Black','King')
subplot_title = 'Vultures'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3]
plt.bar(pos,heights,color=['red','black','black'])
plt.title(subplot_title)
# plt.xticks(pos,bar_labels)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 2)
# pigeons (2)
bar_species = ['Columba livia','Patagioenas fasciata']
bar_labels = ('Rock','Band-tailed')
subplot_title = 'Pigeons'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2]
plt.bar(pos,heights,color=['red','black'])
plt.title(subplot_title)
# plt.xticks(pos,bar_labels)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 3)
# hawks (6)
bar_species = ['Buteo jamaicensis','Accipiter cooperii','Buteo brachyurus','Buteo albonotatus','Falco peregrinus','Accipiter striatus']
bar_labels = ('Red-tailed','Coopers','Short-tailed','Zone-tailed','Peregrine Falcon','Sharp-shinned')
subplot_title = 'Hawks'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4,5,6]
plt.bar(pos,heights,color=['red','black','black','black','black','black'])
plt.title(subplot_title)
# plt.xticks(pos,bar_labels)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 4)
# owls (3)
bar_species = ['Ciccaba virgata','Bubo virginianus','Asio stygius']
bar_labels = ('Mottled','Great Horned','Stygian')
subplot_title = 'Owls'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3]
plt.bar(pos,heights,color=['black','red','black'])
plt.title(subplot_title)
# plt.xticks(pos,bar_labels)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 5)
# finches (4)
bar_species = ['Haemorhous mexicanus','Icterus wagleri','Pheucticus melanocephalus','Piranga rubra']
bar_labels = ('House','Black-vented','Black-headed','Summer Tanager')
subplot_title = 'Finches'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4]
plt.bar(pos,heights,color=['red','black','black','black'])
plt.title(subplot_title)
# plt.xticks(pos,bar_labels)
plt.tick_params(labelbottom=False)


plt.subplot(2, 3, 6)
# wrens (6)
bar_species = ['Thryomanes bewickii','Catherpes mexicanus','Oreothlypis superciliosa','Troglodytes aedon','Henicorhina leucophrys','Salpinctes obsoletus']
bar_labels = ('Bewicks','Canyon','Crescent-chested','Brown-throated','Gray-breasted','Rock')
subplot_title = 'Wrens'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4,5,6]
plt.bar(pos,heights,color=['red','black','black','black','black','black'])
plt.title(subplot_title)
# plt.xticks(pos,bar_labels)

plt.tick_params(labelbottom=False)
plt.tight_layout()
plt.show()

