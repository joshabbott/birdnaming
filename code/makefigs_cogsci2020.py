import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import seaborn as sns
from scipy.stats import pearsonr


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

def get_terminallevel(zapotec_data):
	bird_sci2terminal_names = {}

	terminal_name = list(zapotec_data['folk_specific'])
	science_name = list(zapotec_data['species'])

	i=0
	for bird_name in science_name:
		if bird_name in bird_sci2terminal_names.keys():
			bird_sci2terminal_names[bird_name].append(terminal_name[i])
		else:
			bird_sci2terminal_names[bird_name] = []
			bird_sci2terminal_names[bird_name].append(terminal_name[i])
		i+=1

	return bird_sci2terminal_names




# read zapotec data
# zapotec_data_all = pd.read_csv('./data/df_zapotec.csv')
zapotec_data_all = pd.read_csv('./data/df_zapotec_fullfeats_cogsci2020.csv')

df = zapotec_data_all[zapotec_data_all['folk_generic'].notna()] 

basic_levels = get_basiclevel(df)
basic_level_names = list(set(df['folk_generic']))
terminal_names = get_terminallevel(df)

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
# bird_list = list(df[df['folk_generic'].notna()]['species'])
# freqs = list(df[df['folk_generic'].notna()]['freq'])

data_zapotec = [np.log(i) for i in freqs if i >0]
data_all = [np.log(i) for i in bird_counts.values()]

missing_data = []
for birdcount in bird_counts.keys():
	if birdcount not in bird_list:
		missing_data.append(np.log(bird_counts[birdcount]))



plt.figure(figsize=(9, 4), dpi=100, facecolor='w', edgecolor='k')
plt.rcParams.update({'font.size': 12})
plt.subplot(1,2,1)

pos = [1,2,3]
plotnames = ('Zapotec','Missing','All OAX')
# plt.figure()
plt.violinplot([data_zapotec,missing_data,data_all],pos,showmeans=True) 
plt.title('Frequency densities of Zapotec')
plt.xticks(pos,plotnames)
plt.ylabel('Log frequency')






zapotec_masses = {}
for zapotec_bird in basic_levels.keys():
	mass = float(df[df['species'] == zapotec_bird]['mass'])  
	if mass > 0:
		zapotec_masses[zapotec_bird] = mass

oax_masses = {}
for oax_bird in bird_counts.keys():
	mass = float(zapotec_data_all[zapotec_data_all['species'] == oax_bird]['mass'])
	if mass > 0:
		oax_masses[oax_bird] = mass
        
        
data_zapotec = [np.log(i) for i in zapotec_masses.values()]
data_all = [np.log(i) for i in oax_masses.values()]

missing_data = []
for birdmass in oax_masses.keys():
	if birdmass not in zapotec_masses.keys():
		missing_data.append(np.log(oax_masses[birdmass]))

plt.subplot(1,2,2)
pos = [1,2,3]
plotnames = ('Zapotec','Missing','All OAX')
# plt.figure()
plt.violinplot([data_zapotec,missing_data,data_all],pos,showmeans=True) 
plt.title('Mass densities of Zapotec')
plt.xticks(pos,plotnames)
plt.ylabel('Log mass')


plt.tight_layout()
plt.show()




#
# Figure 2: category size plots
#
SSRR_species = {}
xs = []
ys = []
zs = []
for bird_species in bird_list:
    # get basic level

    if float(df[df['species'] == bird_species]['freq']) > 0.0:
	    basic_taxon = basic_levels[bird_species]
	    len_unique_species_in_basic = len(list(set(zapotec_data_all[zapotec_data_all['folk_generic'] == basic_taxon]['species'])))
	    # SSRR_species[bird_species] = 1/len_unique_species_in_basic
	    SSRR_species[bird_species] = len_unique_species_in_basic
	    # xs.append(bird_sizes[bird_species])
	    xs.append(float(df[df['species'] == bird_species]['mass']))
	    ys.append(SSRR_species[bird_species])
	    zs.append(float(df[df['species'] == bird_species]['freq']))
    




# library & dataset

plt.figure(figsize=(9, 4), dpi=100, facecolor='w', edgecolor='k')
plt.title('Zapotec category organization')

plt.subplot(1,2,1)
ssrrdf = pd.DataFrame(list(zip(np.log(zs),ys)),columns =['log freq','num species'])
sns.regplot(x=ssrrdf["log freq"], y=ssrrdf["num species"])
plt.xlabel('Log frequency')
plt.ylabel('# species per label')

# plt.xlim([0.,1.])
plt.ylim([0.,15.])
plt.yticks((0, 2, 4,6,8,10,12,14))


plt.subplot(1,2,2)
ssrrdf = pd.DataFrame(list(zip(np.log(xs),ys)),columns =['log size','num species'])
sns.regplot(x=ssrrdf["log size"], y=ssrrdf["num species"])
plt.xlabel('Log size')
plt.ylabel('')
# plt.xlim([0.,1.])
plt.ylim([0.,15.])
plt.yticks((0, 2, 4,6,8,10,12,14))
plt.tight_layout()
plt.show()





















#
# Figure 3: Prototype plots
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
clrs = ['black','lightgrey','lightgrey']
sns.barplot(pos,heights,palette=clrs,edgecolor="Black")
plt.title(subplot_title)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 2)
# pigeons (2)
bar_species = ['Columba livia','Patagioenas fasciata']
bar_labels = ('Rock','Band-tailed')
subplot_title = 'Pigeons'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2]
clrs = ['black','lightgrey']
sns.barplot(pos,heights,palette=clrs,edgecolor="Black")
plt.title(subplot_title)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 3)
# hawks (6)
bar_species = ['Buteo jamaicensis','Accipiter cooperii','Buteo brachyurus','Buteo albonotatus','Falco peregrinus','Accipiter striatus']
bar_labels = ('Red-tailed','Coopers','Short-tailed','Zone-tailed','Peregrine Falcon','Sharp-shinned')
subplot_title = 'Hawks'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4,5,6]
plt.title(subplot_title)
clrs = ['black','lightgrey','lightgrey','lightgrey','lightgrey','lightgrey']
sns.barplot(pos,heights,palette=clrs,edgecolor="Black")
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 4)
# owls (3)
bar_species = ['Ciccaba virgata','Bubo virginianus','Asio stygius']
bar_labels = ('Mottled','Great Horned','Stygian')
subplot_title = 'Owls'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3]
clrs = ['lightgrey','black','lightgrey']
sns.barplot(pos,heights,palette=clrs,edgecolor="Black")
plt.title(subplot_title)
plt.tick_params(labelbottom=False)

plt.subplot(2, 3, 5)
# finches (4)
bar_species = ['Haemorhous mexicanus','Icterus wagleri','Pheucticus melanocephalus','Piranga rubra']
bar_labels = ('House','Black-vented','Black-headed','Summer Tanager')
subplot_title = 'Finches'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4]
clrs = ['black','lightgrey','lightgrey','lightgrey']
sns.barplot(pos,heights,palette=clrs,edgecolor="Black")
plt.title(subplot_title)
plt.tick_params(labelbottom=False)


plt.subplot(2, 3, 6)
# wrens (6)
bar_species = ['Thryomanes bewickii','Catherpes mexicanus','Oreothlypis superciliosa','Troglodytes aedon','Henicorhina leucophrys','Salpinctes obsoletus']
bar_labels = ('Bewicks','Canyon','Crescent-chested','Brown-throated','Gray-breasted','Rock')
subplot_title = 'Wrens'
heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4,5,6]
clrs = ['black','lightgrey','lightgrey','lightgrey','lightgrey','lightgrey']
sns.barplot(pos,heights,palette=clrs,edgecolor="Black")
plt.title(subplot_title)

plt.tick_params(labelbottom=False)
plt.tight_layout()
plt.show()




