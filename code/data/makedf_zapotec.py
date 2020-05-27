# makedf_zapotec.py
#
# creates pandas df with columns:
# ['species','length','mass','freq','folk_generic','folk_specific','clements_group','prototype']


# species, eBird species group, frequency, mass, PF1, PF2, ..., 
# folk generic name, folk specific name, common english name, 
# group size folk generic, group size folk specific, group size clements, 
# range, author common name, author prototype, author comments


import pandas as pd
import numpy as np


# Functions for parsing source data

#
# (1) Zapotec language naming data
#
def lang_get_folkgeneric(language_data):
	bird_sci2folkgeneric_names = {}

	folkgeneric_name = list(zapotec_data['FOLK GENERIC'])
	science_name = list(zapotec_data['SCIENTIFIC NAME'])

	i=0
	for bird_name in science_name:
		bird_sci2folkgeneric_names[bird_name] = folkgeneric_name[i]
		i+=1

	return bird_sci2folkgeneric_names

def lang_get_folkterminal(language_data):
	bird_sci2folkterminal_names = {}

	terminal_name = list(zapotec_data['LANGUAGE NAME'])
	science_name = list(zapotec_data['SCIENTIFIC NAME'])

	i=0
	for bird_name in science_name:
		if bird_name in bird_sci2folkterminal_names.keys():
			bird_sci2folkterminal_names[bird_name].append(terminal_name[i])
		else:
			bird_sci2folkterminal_names[bird_name] = []
			bird_sci2folkterminal_names[bird_name].append(terminal_name[i])
		i+=1

	return bird_sci2folkterminal_names



#
# (2) eBird data
#
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



#
# (3) Clements taxonomy data
#
def get_clements_group(clementstax_data):
	clements_group = {}
	clements_group_commonname = {}
	clements_sciname = list(clementstax_data['scientific name'])
	clements_species_group = list(clementstax_data['eBird species group'])
	clements_common_name = list(clementstax_data['English name'])

	i=0
	for bird_name in clements_sciname:
		clements_group[bird_name] = clements_species_group[i]
		clements_group_commonname[bird_name] = clements_common_name[i]
		i+=1

	return clements_group, clements_group_commonname


# 
# (4) EltonTrains bird mass data
#
def get_birdmass(bird_name,bird_mass_df):
	try:
		mass = float(bird_mass_df['BodyMass-Value'][bird_mass_df['Scientific'] == bird_name]) 
	except:
		mass = 0
	return mass


#
# (5) Pigot features
#
# def get_Pigotfeats(bird_name,Pigot_feats_df):





#
# main()
#

# load zapotec naming data
zapotec_data = pd.read_csv("./zapotec_bird_naming_table.csv",skipinitialspace=True)
# get mapping of scientific species to basic level name
folkgeneric_levels = lang_get_folkgeneric(zapotec_data)
folkterminal_names = lang_get_folkterminal(zapotec_data)

# define prototypes based on Hunn's marking
prototypes = ['Cathartes aura','Buteo jamaicensis','Columba livia',
'Bubo virginianus','Thryomanes bewickii',
'Haemorhous mexicanus']


# load ebird data
ebd_data = pd.read_csv('./ebird_MX-OAX_cogsci_clean.csv')
# get ebird counts, index by species name
bird_counts = get_birdcounts(ebd_data)
# get mappings between ebird scientific and common names for observed species
bird_sci2com_names, bird_com2sci_names = map_com2sci(ebd_data)


# load clements taxonomy data
clementstax_data = pd.read_csv("./clementstaxonomy.csv")
# get clements groups, index by species name
clements_groups, clements_groups_commonname = get_clements_group(clementstax_data)





# these will all have 0 freq since they were not observed in eBird
# list(set(folkgeneric_levels.keys()) - set(bird_counts.keys()))       
# In [6]: list(set(folkgeneric_levels.keys()) - set(bird_counts.keys()))                                                                                        
# Out[6]: 
# ['Caracara plancus',
#  'Aimophila mystacalis',
#  'Oporornis tolmiei',
#  'Caprimulgus arizonae',
#  'Picoides scalaris',
#  'Dendroica occidentalis',
#  'Dendroica coronata',
#  'Vermivora celata',
#  'Carduelis psaltria',
#  'Meleagris gallopavo',
#  'Centurus hypopolius',
#  'Amazilia wagneri',
#  'Aratinga canicularis',
#  'Cypseloides rutilus',
#  'Circus cyaneus',
#  'Vermivora ruficapilla',
#  'Dendroica nigrescens',
#  'Aphelocoma californica',
#  'Anser cygnoides',
#  'Hirundo pyrrhonota',
#  'Ergaticus ruber',
#  'Gallus gallus']


# some latin names that Hunn used do not match the Clements taxonomy names that eBirds uses
# this list updates the names for use with the Clements taxonomy / eBird frequencies

# list(set(folkgeneric_levels.keys()) - set(clements_groups.keys()))
basic2clements = {}
basic2clements['Carduelis psaltria'] = 'Spinus psaltria'
basic2clements['Amazilia wagneri'] = 'Amazilia rutila'
basic2clements['Aimophila mystacalis'] = 'Peucaea mystacalis'
basic2clements['Ergaticus ruber'] = 'Cardellina rubra'
basic2clements['Vermivora celata'] = 'Leiothlypis celata'
basic2clements['Oporornis tolmiei'] = 'Geothlypis tolmiei'
basic2clements['Picoides scalaris'] = 'Dryobates scalaris'
basic2clements['Aratinga canicularis'] = 'Eupsittula canicularis'
basic2clements['Cypseloides rutilus'] = 'Streptoprocne rutila'
basic2clements['Hirundo pyrrhonota'] = 'Petrochelidon pyrrhonota'
basic2clements['Caprimulgus arizonae'] = 'Antrostomus arizonae'
basic2clements['Centurus hypopolius'] = 'Melanerpes hypopolius'
basic2clements['Vermivora ruficapilla'] = 'Leiothlypis ruficapilla'
basic2clements['Dendroica nigrescens'] = 'Setophaga nigrescens'
basic2clements['Dendroica occidentalis'] = 'Setophaga occidentalis'
basic2clements['Dendroica coronata'] = 'Setophaga coronata'

# some latin names that eBird/Clements use do not match the body mass names that Dunning uses
# this list updates that names for use with the Dunning body masses

# NOTE: I THINK PIGOT DATA ALSO FOLLOWS THIS CONVENTION

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
clements2birdmass['Oreothlypis superciliosa'] = 'Parula superciliosa'
clements2birdmass['Ptiliogonys cinereus'] = 'Ptilogonys cinereus'
clements2birdmass['Cardellina pusilla'] = 'Wilsonia pusilla'
clements2birdmass['Spinus notatus'] = 'Carduelis notata'
clements2birdmass['Setophaga townsendi'] = 'Dendroica townsendi'
clements2birdmass['Haemorhous mexicanus'] = 'Carpodacus mexicanus'
clements2birdmass['Melozone albicollis'] = 'Pipilo albicollis'




# load bird masses
bigbirddata_data = pd.read_csv('./EltonTraits_data.txt',sep='\t',encoding = "ISO-8859-1")
bird_mass_df = bigbirddata_data[['BodyMass-Value','Scientific']]

zapotec_masses = {}
for zapotec_bird in folkgeneric_levels.keys():
    mass = get_birdmass(zapotec_bird,bird_mass_df)
    # print("birdname: %s    mass: %f" % (zapotec_bird, mass))
  
    if mass > 0:
        zapotec_masses[zapotec_bird] = mass
    else:
        zapotec_masses[zapotec_bird] = get_birdmass(clements2birdmass[zapotec_bird],bird_mass_df)
        # print("!!! Need to check ebird/clements -> EltonTraits birdname: %s    mass: %f" % (zapotec_bird, mass))
    print("birdname: %s    mass: %f" % (zapotec_bird, zapotec_masses[zapotec_bird]))



# df format:

# species, eBird species group, frequency, mass, PF1, PF2, ..., 
# folk generic name, folk specific name, common english name, 
# group size folk generic, group size folk specific, group size clements, 
# range, author common name, author prototype, author comments


# let's start simple

# this is the main list of bird species to consider
# bird_list = list(set(zapotec_masses.keys()).intersection(set(bird_counts.keys())))  
bird_list = list(set(folkgeneric_levels.keys()))

species = []
common_name = []
masses = []
freq = []
folk_generic = []
folk_specific = []
clements_group = []
prototype = []

for cur_species in bird_list:

	# we record species based off the clements taxonomy
	if cur_species in clements_groups.keys():
		species.append(cur_species)
	else:
		species.append(basic2clements[cur_species])

	try:
		common_name.append(bird_sci2com_names[cur_species])
	except:
		try:
			common_name.append(clements_groups_commonname[basic2clements[cur_species]])
		except:
			common_name.append('NA')

	masses.append(zapotec_masses[cur_species])

	try:
	    freq.append(bird_counts[cur_species])
	except:
	    freq.append(0)

	folk_generic.append(folkgeneric_levels[cur_species])
	if folkgeneric_levels[cur_species] in folkterminal_names[cur_species]:
	    folk_specific.append(folkgeneric_levels[cur_species])
	else:
	    folk_specific.append(folkterminal_names[cur_species][0])

	if cur_species in clements_groups.keys():
	    clements_group.append(clements_groups[cur_species])
	else:
	    clements_group.append(clements_groups[basic2clements[cur_species]])

	if cur_species in prototypes:
	    prototype.append('1')
	else:
	    prototype.append('0')


df = pd.DataFrame(list(zip(species,common_name,masses,freq,folk_generic,folk_specific,clements_group,prototype)),columns =['species','common_name','mass','freq','folk_generic','folk_specific','clements_group','prototype'])


group_size_folk_generics = []
basic_levels = list(df['folk_generic']) 
for basic_level in basic_levels:
	group_size_folk_generics.append(len(df[df['folk_generic'] == basic_level]))
df['group_size_folk_generics'] = group_size_folk_generics 

group_size_folk_specific = []
terminal_levels = list(df['folk_specific']) 
for terminal_level in terminal_levels:
	group_size_folk_specific.append(len(df[df['folk_specific'] == terminal_level]))
df['group_size_folk_specific'] = group_size_folk_specific 


group_size_clements = []
clements_groups = list(df['clements_group'])
for clements_group_item in clements_groups:
	group_size_clements.append(len(df[df['clements_group'] == clements_group_item]))
df['group_size_clements'] = group_size_clements 











# add missing OAX data

bird_list = list(df['species']) 

missing_species = []
missing_freq = []
missing_mass = []
missing_commonname = []

for birdname in bird_counts.keys():
	if birdname not in bird_list:
		# get species name, freq, mass -- everything else is NA
		missing_species.append(birdname)
		missing_freq.append(bird_counts[birdname])
		missing_mass.append(get_birdmass(birdname,bird_mass_df))
		missing_commonname.append(clements_groups_commonname[birdname])



i=0
for cur_item in missing_species:
	foo = {'species':cur_item,'common_name':missing_commonname[i],'mass':missing_mass[i],'freq':missing_freq[i],'folk_generic':'NA','folk_specific':'NA','clements_group':'NA','prototype':'NA','group_size_folk_generics':'NA','group_size_folk_specific':'NA','group_size_clements':'NA'}
	# 'PC1':'NA','PC2':'NA','PC3':'NA','PC4':'NA','PC5':'NA','PC6':'NA','PC7':'NA','PC8':'NA','PC9':'NA','Beak_PC1':'NA','Beak_PC2':'NA','Beak_PC3':'NA','Beak_PC4':'NA','Realm':'NA','TrophicLevel':'NA','TrophicNiche':'NA','ForagingNiche':'NA'}
	# print(foo)
	df = df.append(foo, ignore_index=True)
	i+=1







# # load Pigot features
Pigot_df = pd.read_csv('./Pigot_data.csv')
Pigot_df['Binomial'] = Pigot_df['Binomial'].str.replace('_',' ')
Pigot_df = Pigot_df.drop(columns=['Unnamed: 18']) 

all_df = pd.merge(df, Pigot_df, how='left', left_on='species', right_on='Binomial')
all_df = all_df.drop(columns=['Binomial']) 


# WE ALREADY DID THIS AND NOW NEED TO MANUALLY HACK IT
# all_df.to_csv('./df_zapotec_fullfeats_cogsci2020.csv', index=False)




In [82]: all_df[all_df['TrophicLevel'].isna()][['species','common_name']]                                                                                                    
                                         species                          common_name
9                             Leiothlypis celata               Orange-crowned Warbler
Leiothlypis celata,Orange-crowned Warbler,9.19,0,wǐt,wǐt,Wood-Warblers,0,12,11,15,-2.115629225,0.00096453,-0.163527183,0.12222412,0.259543174,0.063500359,0.011553655,-0.092295733,-0.047868629,-0.942694465,-0.162597739,0.010292343,0.093822592,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

12                              Poecile sclateri                    Mexican Chickadee
Poecile sclateri,Mexican Chickadee,10.09,1172,mguîn̲-pàyâs,mguîn̲-pàyâs,"Tits, Chickadees, and Titmice",0,2,2,2,-2.025787199,0.238728485,-0.350927728,-0.062910776,0.132980165,0.070106331,-0.160737468,0.020596584,-0.045727448,-1.128930655,-0.211657559,-0.155379796,0.095004552,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

26                           Setophaga townsendi                   Townsend's Warbler
Setophaga townsendi,Townsend's Warbler,8.84,3787,yěets,yěets-pînt,Wood-Warblers,0,3,1,15,-2.251090547,0.164996408,-0.057571689,-0.131520941,0.210924904,0.059075091,-0.02431695,-0.105238991,-0.036608791,-1.212296515,0.034687802,-0.026125604,0.053491139,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

27                          Haemorhous mexicanus                          House Finch
Haemorhous mexicanus,House Finch,21.4,7991,mguěy,mguěy,"Finches, Euphonias, and Allies",1,4,2,3,-0.992391686,-0.016822716,-0.657889341,0.602201429,-0.00994912,-0.029375894,-0.062018321,-0.111062029,-0.152756717,-0.270881483,-0.827347006,-0.032033604,0.233252538,Nearctic,Herbivore,Granivore,Generalist

31                          Antrostomus arizonae               Mexican Whip-poor-will
Antrostomus arizonae,Mexican Whip-poor-will,53.3,0,pùrpùrwít,pùrpùrwít,Nightjars,0,1,1,1,-0.231660553,0.716370861,-0.141775201,-0.643026273,-0.624212822,0.054886031,0.291324597,-0.0044018,0.229053676,-0.87069187,0.148823586,0.314918111,-0.319828596,Nearctic,Carnivore,Invertivore,Generalist

38                            Setophaga coronata                Yellow-rumped Warbler
Setophaga coronata,Yellow-rumped Warbler,11.94,0,wǐt,wǐt,Wood-Warblers,0,12,11,15,-1.870837532,0.288333776,-0.11085163,-0.171386276,0.158207393,0.109103972,0.000844327,-0.056208912,0.010769417,-1.134823293,-0.010056843,-0.001265468,-0.004062227,Nearctic,Carnivore,Invertivore,Generalist

39                            Peucaea mystacalis                      Bridled Sparrow
Peucaea mystacalis,Bridled Sparrow,22.2,0,mtsùu,mtsùu,New World Sparrows,0,8,8,10,-0.944699989,0.098834176,-0.413137144,0.087395248,0.191501131,-0.172291726,-0.11492413,0.018027878,-0.0306892,-0.442670166,-0.334031963,-0.133578406,0.052298079,Neotropic,Omnivore,Omnivore,

40                      Oreothlypis superciliosa             Crescent-chested Warbler
Oreothlypis superciliosa,Crescent-chested Warbler,9.0,2207,nguzhǐn,nguzhǐn-gùts,Wood-Warblers,0,6,1,15,-2.116071568,-0.080630313,-0.119143836,-0.133527619,0.158245013,0.024766274,-0.00894847,-0.050870373,0.002726955,-0.943362252,0.072783299,-0.009636384,0.04486531,Neotropic,Carnivore,Invertivore,Invertivore glean arboreal

44                            Dryobates villosus                     Hairy Woodpecker
Dryobates villosus,Hairy Woodpecker,62.65,1156,càrpìntêr,càrpìntêr-ló-guì,Woodpeckers,0,7,1,8,0.703445573,-0.614512179,-0.127170555,-0.022604197,0.016243936,0.158071141,0.15649355,0.054611535,-0.081609168,0.849636801,0.113413965,0.182611648,0.158339153,Nearctic,Carnivore,Invertivore,Invertivore bark

46                        Setophaga occidentalis                       Hermit Warbler
Setophaga occidentalis,Hermit Warbler,10.4,0,wǐt,wǐt,Wood-Warblers,0,12,11,15,-2.033412549,0.148281266,-0.133096883,-0.110508517,0.132298767,0.043038925,-0.069506722,-0.075128211,-0.04111856,-1.091967552,-0.023454753,-0.065434742,0.068172446,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

57                            Geothlypis tolmiei               MacGillivray's Warbler
Geothlypis tolmiei,MacGillivray's Warbler,10.4,0,wǐt,wǐt,Wood-Warblers,0,12,11,15,-2.071197907,0.157043429,0.032992409,-0.11089502,0.316237297,-0.078919572,-0.001727357,-0.107048829,-0.010786733,-1.109382574,0.076609489,-0.027089865,-0.002347406,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

78                            Cardellina pusilla                     Wilson's Warbler
Cardellina pusilla,Wilson's Warbler,6.96,7578,yěets,yěets,Wood-Warblers,0,3,1,15,-2.449244901,0.068839108,-0.216992566,-0.018294738,0.324864193,0.005683247,0.051064382,-0.109410986,-0.036312624,-1.168925232,-0.114155912,0.039976306,0.066380617,Nearctic,Carnivore,Invertivore,Generalist

79                              Mareca americana                      American Wigeon
Mareca americana,American Wigeon,754.61,271,bǎd,bǎd-guìx,Waterfowl,0,7,5,10,3.235575548,-0.062563115,0.400017516,0.390616176,-0.521030685,0.059075795,0.371368339,-0.120244153,0.014891589,1.575272962,-0.069736501,0.405112723,-0.097920303,Nearctic,Herbivore,Omnivore,

81                              Cardellina rubra                          Red Warbler
Cardellina rubra,Red Warbler,8.1,0,x-quǐit-ngùbìdz,x-quǐit-ngùbìdz,Wood-Warblers,0,1,1,15,-2.234817426,0.138089688,-0.322452134,-0.059239447,0.288827915,-0.02952933,-0.02164055,-0.059045868,0.045586613,-1.114783707,-0.173676067,-0.040610123,-0.013254963,Neotropic,Carnivore,Invertivore,Invertivore glean arboreal

83                            Dryobates scalaris             Ladder-backed Woodpecker
Dryobates scalaris,Ladder-backed Woodpecker,31.59,0,càrpìntêr,càrpìntêr-psì-yèen̲,Woodpeckers,0,7,1,8,-0.428873634,-0.309508146,-0.175864277,0.208780777,-0.077525176,0.201250119,0.150966795,0.05717681,-0.046737882,0.092944127,-0.150591152,0.181989953,0.124215711,Nearctic,Carnivore,Invertivore,Invertivore bark

94                               Spatula discors                     Blue-winged Teal
Spatula discors,Blue-winged Teal,359.44,2080,bǎd,bǎd-guìx,Waterfowl,0,7,5,10,2.479185808,-0.613521588,0.475520911,0.585734269,-0.363623968,0.078865295,0.328464611,-0.178740042,0.013636225,1.714390999,0.010231259,0.364213512,-0.016944818,Nearctic,Omnivore,Herbivore aquatic,Herbivore aquatic surface

104                          Melozone albicollis                White-throated Towhee
Melozone albicollis,White-throated Towhee,46.4,9110,chûurr,chûurr,New World Sparrows,0,1,1,10,-0.069038543,0.138694222,-0.375162362,0.269303962,0.175316867,-0.270589029,-0.090769748,-0.014112041,-0.098377049,-0.02861635,-0.465964285,-0.11242581,0.086154858,Neotropic,Herbivore,Granivore,Granivore ground

113                              Spinus psaltria                     Lesser Goldfinch
Spinus psaltria,Lesser Goldfinch,8.77,0,mdzíl-dò,mdzíl-dò,"Finches, Euphonias, and Allies",0,1,1,3,-2.121530646,-0.251605385,-0.419720096,0.477011867,-0.029136714,0.167566894,-0.161988531,-0.017997147,-0.015997567,-0.675171465,-0.493024247,-0.127102243,0.16314387,Nearctic,Herbivore,Granivore,Generalist

122                         Ptiliogonys cinereus                Gray Silky-flycatcher
Ptiliogonys cinereus,Gray Silky-flycatcher,33.6,5476,péedrùuch,péedrùuch,Silky-flycatchers,0,1,1,1,-0.753435794,0.543112011,-0.342927022,-0.171150102,-0.286746977,-0.177157038,0.062940322,0.0770378,0.115451694,-0.830314344,-0.237814864,0.056384838,-0.163789554,Neotropic,Omnivore,Omnivore,

124                              Ciccaba virgata                          Mottled Owl
Ciccaba virgata,Mottled Owl,283.97,338,dǎm̲,dǎm̲-yêt,Owls,0,3,2,6,2.540458981,0.236250339,-0.446972638,-0.035115589,0.002473579,0.157297741,-0.228360548,0.103169151,0.145559039,1.101124846,-0.369750368,-0.23183564,-0.13309803,Neotropic,Carnivore,Vertivore,Vertivore perch

126                               Spinus notatus                  Black-headed Siskin
Spinus notatus,Black-headed Siskin,10.9,664,yěets,yěets-dán,"Finches, Euphonias, and Allies",0,3,1,3,-1.843237693,-0.394694674,-0.231612736,0.43735479,-0.029531675,0.152191854,-0.144397121,-0.048554199,-0.021408162,-0.455365483,-0.31140146,-0.11022648,0.161189332,Neotropic,Herbivore,Granivore,Granivore arboreal

127                         Setophaga nigrescens          Black-throated Gray Warbler
Setophaga nigrescens,Black-throated Gray Warbler,8.7,0,wǐt,wǐt,Wood-Warblers,0,12,11,15,-2.209157752,0.15325584,-0.16473352,0.035063244,0.275935251,0.118382263,-0.062512738,-0.07062752,0.010084872,-1.122688357,-0.145622193,-0.068306187,0.032320092,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

135                      Leiothlypis ruficapilla                    Nashville Warbler
Leiothlypis ruficapilla,Nashville Warbler,8.09,0,mguîn̲-tsíríic,mguîn̲-tsíríic,Wood-Warblers,0,1,1,15,-2.41589102,0.092365063,-0.026905952,0.079954307,0.177817893,0.084266774,-0.122226536,-0.043857112,0.0060314,-1.198755377,-0.064440543,-0.123941375,0.042669417,Nearctic,Carnivore,Invertivore,Invertivore glean arboreal

148                       Eupsittula canicularis              Orange-fronted Parakeet
Eupsittula canicularis,Orange-fronted Parakeet,85.0,0,pèrícw,pèrícw,"Parrots, Parakeets, and Allies",0,1,1,3,0.94760872,-0.68024379,-0.826989558,0.708600148,-0.648825966,-0.136443089,-0.256599134,-0.045008827,-0.062335853,1.172711232,-0.842640155,-0.179955858,0.234492726,Neotropic,Herbivore,Frugivore,Fugivore glean

