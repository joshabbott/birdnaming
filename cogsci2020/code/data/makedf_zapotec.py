# makedf_zapotec.py
#
# creates pandas df with columns:
# ['species','length','mass','freq','folk_generic','folk_specific','clements_group','prototype']


import pandas as pd
import numpy as np

# some functions for parsing
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

def map_com2sci(ebd_data):
	# read ebird count and name data
	bird_sci2com_names = {}
	bird_com2sci_names = {}

	common_name = list(ebd_data['COMMON NAME'])
	science_name = list(ebd_data['SCIENTIFIC NAME'])

	i=0
	for bird_name in science_name:
		bird_sci2com_names[bird_name] = common_name[i]
		bird_com2sci_names[common_name[i]] = bird_name
		i+=1

	return bird_sci2com_names, bird_com2sci_names

def get_clements_group(clementstax_data):
	clements_group = {}
	clements_sciname = list(clementstax_data['scientific name'])
	clements_species_group = list(clementstax_data['eBird species group'])

	i=0
	for bird_name in clements_sciname:
		clements_group[bird_name] = clements_species_group[i]
		i+=1

	return clements_group

def get_birdsizes(bird_sizes_df):
	bird_size_scientific_names = [i.strip() for i in list(bird_sizes_df['SCIENTIFIC NAME'])]
	bird_size_ranges = [i.strip() for i in list(bird_sizes_df['SIZE'])]	

	bird_sizes = {}
	for i in range(len(bird_size_scientific_names)):
		zap_size = bird_size_ranges[i].split()
		if len(zap_size) > 1:
			#check to see if it's a range or not
			avg_size = zap_size[0]
			range_check = avg_size.split('-')
			if len(range_check) > 1:
				# it is a range, compute the median
				a = float(range_check[0])
				b = float(range_check[1])
				avg_size = np.median([a,b])
			else:
				avg_size = float(range_check[0])	

			bird_sizes[bird_size_scientific_names[i]] = avg_size

	return bird_sizes

def get_birdmass(bird_name,bird_mass_df):
	try:
		mass = float(bird_mass_df['BodyMass-Value'][bird_mass_df['Scientific'] == bird_name]) 
	except:
		mass = 0
	return mass



def get_basiclevel(zapotec_data):
	bird_sci2basic_names = {}

	basic_name = list(zapotec_data['BASIC LEVEL'])
	science_name = list(zapotec_data['SCIENTIFIC NAME'])

	i=0
	for bird_name in science_name:
		bird_sci2basic_names[bird_name] = basic_name[i]
		i+=1

	return bird_sci2basic_names


def get_terminallevel(zapotec_data):
	bird_sci2terminal_names = {}

	terminal_name = list(zapotec_data['LANGUAGE NAME'])
	science_name = list(zapotec_data['SCIENTIFIC NAME'])

	i=0
	for bird_name in science_name:
		if bird_name in bird_sci2terminal_names.keys():
			bird_sci2terminal_names[bird_name].append(terminal_name[i])
		else:
			bird_sci2terminal_names[bird_name] = []
			bird_sci2terminal_names[bird_name].append(terminal_name[i])
		i+=1

	return bird_sci2terminal_names




# THIS IS FOR EXISTING ZAPOTEC DATASTRUCTURES

# load clements taxonomy data
clementstax_data = pd.read_csv("./clementstaxonomy.csv")
# get clements groups, index by species name
clements_groups = get_clements_group(clementstax_data)

# load ebird data
ebd_data = pd.read_csv('./ebird_MX-OAX_relJul-2019_clean.csv')
# get bird counts, index by species name
bird_counts = get_birdcounts(ebd_data)

# load bird sizes
bird_sizes_df = pd.read_csv("./bird_species-size.csv",skipinitialspace=True)
# compute average bird size, index by species name
bird_sizes = get_birdsizes(bird_sizes_df)

# load zapotec naming data
zapotec_data = pd.read_csv("./zapotec_bird_naming_table.csv",skipinitialspace=True)
# get mapping of scientific species to basic level name
basic_levels = get_basiclevel(zapotec_data)
terminal_names = get_terminallevel(zapotec_data)


# define prototypes based on Hunn's marking
prototypes = ['Cathartes aura','Buteo jamaicensis','Accipiter striatus','Columba livia','Bubo virginianus','Thryomanes bewickii','Myadestes occidentalis','Haemorhous mexicanus','Icterus wagleri']




# these will all have 0 freq since they were not observed in eBird
# list(set(basic_levels.keys()) - set(bird_counts.keys()))                                                                                      

# ['Anser cygnoides',
#  'Ergaticus ruber',
#  'Picoides scalaris',
#  'Centurus hypopolius',
#  'Cypseloides rutilus',
#  'Hirundo pyrrhonota',
#  'Aphelocoma californica',
#  'Vermivora ruficapilla',
#  'Dendroica occidentalis',
#  'Circus cyaneus',
#  'Troglodytes bruneicollis',
#  'Caracara plancus',
#  'Dendroica nigrescens',
#  'Dendroica coronata',
#  'Aimophila mystacalis',
#  'Gallus gallus',
#  'Anser anser',
#  'Carduelis psaltria',
#  'Amazilia wagneri',
#  'Oporornis tolmiei',
#  'Vermivora celata',
#  'Aratinga canicularis',
#  'Meleagris gallopavo',
#  'Caprimulgus arizonae',
#  'Anas platyrhynchos']

# some latin names that Hunn used do not match the Clements taxonomy names that eBirds uses
# this list updates the names for use with the Clements taxonomy / eBird frequencies

# list(set(basic_levels.keys()) - set(clements_groups.keys()))
basic2clements = {}
basic2clements['Carduelis psaltria'] = 'Spinus psaltria'
basic2clements['Amazilia wagneri'] = 'Amazilia rutila'
basic2clements['Aimophila mystacalis'] = 'Peucaea mystacalis'
basic2clements['Ergaticus ruber'] = 'Cardellina rubra'
basic2clements['Vermivora celata'] = 'Oreothlypis celata'
basic2clements['Oporornis tolmiei'] = 'Geothlypis tolmiei'
basic2clements['Picoides scalaris'] = 'Dryobates scalaris'
basic2clements['Aratinga canicularis'] = 'Eupsittula canicularis'
basic2clements['Troglodytes bruneicollis'] = 'Troglodytes aedon'
basic2clements['Cypseloides rutilus'] = 'Streptoprocne rutila'
basic2clements['Hirundo pyrrhonota'] = 'Petrochelidon pyrrhonota'
basic2clements['Caprimulgus arizonae'] = 'Antrostomus arizonae'
basic2clements['Centurus hypopolius'] = 'Melanerpes hypopolius'
basic2clements['Vermivora ruficapilla'] = 'Oreothlypis ruficapilla'
basic2clements['Dendroica nigrescens'] = 'Setophaga nigrescens'
basic2clements['Dendroica occidentalis'] = 'Setophaga occidentalis'
basic2clements['Dendroica coronata'] = 'Setophaga coronata'

# some latin names that Hunn used do not match the body mass names that Dunning uses
# this list updates that names for use with the Dunning body masses
clements2birdmass = {}
clements2birdmass['Spatula discors'] = 'Anas discors'
clements2birdmass['Mareca americana'] = 'Anas americana'
clements2birdmass['Ciccaba virgata'] = 'Strix virgata'
clements2birdmass['Caprimulgus arizonae'] = 'Caprimulgus vociferus'
clements2birdmass['Cypseloides rutilus'] = 'Streptoprocne rutila'
clements2birdmass['Hirundo pyrrhonota'] = 'Petrochelidon pyrrhonota'
clements2birdmass['Amazilia wagneri'] = 'Amazilia rutila'
clements2birdmass['Centurus hypopolius'] = 'Melanerpes hypopolius'
clements2birdmass['Dryobates villosus'] = 'Picoides villosus'
clements2birdmass['Poecile sclateri'] = 'Parus sclateri'
clements2birdmass['Troglodytes bruneicollis'] = 'Troglodytes aedon'
clements2birdmass['Oreothlypis superciliosa'] = 'Parula superciliosa'
clements2birdmass['Ptiliogonys cinereus'] = 'Ptilogonys cinereus'
clements2birdmass['Cardellina pusilla'] = 'Wilsonia pusilla'
clements2birdmass['Spinus notatus'] = 'Carduelis notata'
clements2birdmass['Setophaga townsendi'] = 'Dendroica townsendi'
clements2birdmass['Haemorhous mexicanus'] = 'Carpodacus mexicanus'
clements2birdmass['Melozone albicollis'] = 'Pipilo albicollis'


# load bird masses
bigbirddata_data = pd.read_csv('./BirdFuncDat.txt',sep='\t',encoding = "ISO-8859-1")
bird_mass_df = bigbirddata_data[['BodyMass-Value','Scientific']]

zapotec_masses = {}
for zapotec_bird in basic_levels.keys():
    mass = get_birdmass(zapotec_bird,bird_mass_df)
#     print("birdname: %s    mass: %f" % (zapotec_bird, mass))
    if mass > 0:
        zapotec_masses[zapotec_bird] = mass
    else:
        zapotec_masses[zapotec_bird] = get_birdmass(clements2birdmass[zapotec_bird],bird_mass_df)
#         print("birdname: %s    mass: %f" % (zapotec_bird, mass))




# this is the main list of bird species to consider
# bird_list = list(set(zapotec_masses.keys()).intersection(set(bird_counts.keys())))  
bird_list = list(set(basic_levels.keys()))

species = []
masses = []
lengths = []
freq = []
folk_generic = []
folk_specific = []
clements_group = []
prototype = []

for cur_species in bird_list:
    species.append(cur_species)
    lengths.append(bird_sizes[cur_species])
    masses.append(zapotec_masses[cur_species])
    
    try:
        freq.append(bird_counts[cur_species])
    except:
        freq.append(0)
    
    folk_generic.append(basic_levels[cur_species])
    if basic_levels[cur_species] in terminal_names[cur_species]:
        folk_specific.append(basic_levels[cur_species])
    else:
        folk_specific.append(terminal_names[cur_species][0])
    
    if cur_species in clements_groups.keys():
        clements_group.append(clements_groups[cur_species])
    else:
        clements_group.append(clements_groups[basic2clements[cur_species]])
    
    if cur_species in prototypes:
        prototype.append('1')
    else:
        prototype.append('0')


df = pd.DataFrame(list(zip(species,lengths,masses,freq,folk_generic,folk_specific,clements_group,prototype)),columns =['species','length','mass','freq','folk_generic','folk_specific','clements_group','prototype'])
df.to_csv('./df_zapotec.csv', index=False)
