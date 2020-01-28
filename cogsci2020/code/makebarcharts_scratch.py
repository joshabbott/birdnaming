


bird_list = list(df['species']) 

def get_barheights_freq(bar_species,bird_list,df):
	heights = []
	for bird_name in bar_species:
		if bird_name in bird_list:
			heights.append(float(df[df['species'] == bird_name]['freq']))
		else:
			heights.append(0.0)

	return heights




plt.subplot(1, 2, 1)

# vultures
bar_species = ['Cathartes aura','Coragyps atratus','Sarcoramphus papa']
bar_labels = ('Turkey','Black','King')
subplot_title = 'Vultures'

heights = get_barheights_freq(bar_species,bird_list,df)


y_pos = np.arange(len(bar_labels))
# Create horizontal bars
plt.barh(y_pos, heights)
# Create names on the y-axis
plt.yticks(y_pos, bar_labels)
# add plot title
plt.title(subplot_title)




# plt.subplot(2, 2, 2)

# # vultures
# bar_species = ['Cathartes aura','Coragyps atratus','Sarcoramphus papa']
# bar_labels = ('Turkey','Black','King')
# subplot_title = 'Vultures'

# heights = get_barheights_freq(bar_species,bird_list,df)


# y_pos = np.arange(len(bar_labels))
# # Create horizontal bars
# plt.barh(y_pos, heights)
# # Create names on the y-axis
# plt.yticks(y_pos, bar_labels)
# # add plot title
# plt.title(subplot_title)



plt.subplot(1, 2, 2)

# hawks in general
bar_species = ['Buteo jamaicensis','Accipiter cooperii','Buteo brachyurus','Buteo albonotatus','Falco peregrinus','Accipiter striatus']
bar_labels = ('Red-tailed','Coopers','Short-tailed','Zone-tailed','Peregrine Falcon','Sharp-shinned')
subplot_title = 'Hawks'

heights = get_barheights_freq(bar_species,bird_list,df)


y_pos = np.arange(len(bar_labels))
# Create horizontal bars
plt.barh(y_pos, heights)
# Create names on the y-axis
plt.yticks(y_pos, bar_labels)
# add plot title
plt.title(subplot_title)


# plt.subplot(2, 2, 4)

# # hawks in general
# bar_species = ['Buteo jamaicensis','Accipiter cooperii','Buteo brachyurus','Buteo albonotatus','Falco peregrinus','Accipiter striatus']
# bar_labels = ('Red-tailed','Coopers','Short-tailed','Zone-tailed','Peregrine Falcon','Sharp-shinned')
# subplot_title = 'Hawks'

# heights = get_barheights_freq(bar_species,bird_list,df)


# y_pos = np.arange(len(bar_labels))
# # Create horizontal bars
# plt.barh(y_pos, heights)
# # Create names on the y-axis
# plt.yticks(y_pos, bar_labels)
# # add plot title
# plt.title(subplot_title)



# Show graphic
plt.show()



plt.figure()
# heights = [11514,7346,49]
# bars = ('Turkey Vulture','Black Vulture','King Vulture')

bar_species = ['Cathartes aura','Coragyps atratus','Sarcoramphus papa']
bar_labels = ('Turkey','Black','King')
subplot_title = 'Vultures'

heights = get_barheights_freq(bar_species,bird_list,df)

pos = [1,2,3]
plt.bar(pos,heights,color=['red','black','black'])
plt.title('Vultures')
plt.xticks(pos,bar_labels)
plt.show()






# plt.figure()
# heights = [2488,1169,844,772,745,1354]
# bars = ('Red-tailed','Short-tailed','Zone-tailed','Peregrine Falcon','Sharp-shinned','Coopers')
# 
bar_species = ['Buteo jamaicensis','Accipiter cooperii','Buteo brachyurus','Buteo albonotatus','Falco peregrinus','Accipiter striatus']
bar_labels = ('Red-tailed','Coopers','Short-tailed','Zone-tailed','Peregrine Falcon','Sharp-shinned')
subplot_title = 'Hawks'

heights = get_barheights_freq(bar_species,bird_list,df)
pos = [1,2,3,4,5,6]
plt.bar(pos,heights,color=['red','black','black','black','black','black'])
plt.title('Hawks')
plt.xticks(pos,bar_labels)
plt.show()


# plt.figure()
# heights = [1935,803]
# bars = ('Rock','Band-tailed')
# pos = [1,2]
# plt.bar(pos,heights,color=['red','black'])
# plt.title('Pigeons')
# plt.xticks(pos,bars)
# plt.show()


plt.figure()
# heights = [131,264,10]
# bars = ('Great Horned','Mottled','Stygian')
bar_species = ['Bubo virginianus','Ciccaba virgata','Asio stygius']
bar_labels = ('Great Horned','Mottled','Stygian')
subplot_title = 'Owls'

heights = get_barheights_freq(bar_species,bird_list,df)

pos = [1,2,3]
plt.bar(pos,heights,color=['red','black','black'])
plt.title('Owls')
plt.xticks(pos,bar_labels)
plt.show()



bar_species = ['Thryomanes bewickii','Ciccaba virgata','Asio stygius']
bar_labels = ('Great Horned','Mottled','Stygian')
subplot_title = 'Owls'

heights = get_barheights_freq(bar_species,bird_list,df)

pos = [1,2,3]
plt.bar(pos,heights,color=['red','black','black'])
plt.title('Owls')
plt.xticks(pos,bar_labels)
plt.show()

Bewick's Wren, (Thryomanes bewickii): 4937
	Canyon Wren, (Catherpes mexicanus): 2130
	Rock Wren, (Salpinctes obsoletus): 915
	Brown-throated Wren, (Troglodytes bruneicollis): not in ebird
	Gray-breasted Wood-Wren, (Henicorhina leucophrys): 1353
	Crescent-chested Warbler, (Oreothlypis superciliosa): 1845






# In [41]: df[df['prototype'] == 1]                                                                                                                            
# Out[41]: 
#                     species  length     mass   freq       folk_generic      folk_specific                  clements_group  prototype
# 5         Buteo jamaicensis   22.00  1101.16   2978                msì                msì     Vultures, Hawks, and Allies          1
# 13          Icterus wagleri    8.75    41.80   5262              mguěy  mguěy-guièe-pchôg                      Blackbirds          1
# 16   Myadestes occidentalis    8.00    36.40   3842  mguîn̲-guìib-tsár  mguîn̲-guìib-tsár                        Thrushes          1
# 36       Accipiter striatus   12.00   130.59    862                msì            msì-lâg     Vultures, Hawks, and Allies          1
# 55         Bubo virginianus   21.50  1575.70    145               dǎm̲               dǎm̲                            Owls          1
# 59           Cathartes aura   29.00  1518.24  13517               pěch               pěch     Vultures, Hawks, and Allies          1
# 90      Thryomanes bewickii    5.25     9.90   5465            nguzhǐn            nguzhǐn                           Wrens          1
# 138    Haemorhous mexicanus    6.00    21.40   7991              mguěy              mguěy  Finches, Euphonias, and Allies          1
# 144           Columba livia   13.50   354.20   2254              pàlôm              pàlôm               Pigeons and Doves          1

# In [44]: df[df['prototype'] == 1]['freq'].mean()                                                                                                             
# Out[44]: 4701.7777777777774

# In [45]: df[df['prototype'] == 0]['freq'].mean()                                                                                                             
# Out[45]: 1694.2447552447552


# make violint plots for prototypes
allfreqs = list(df['freq'])

freqs_protos = list(df[df['prototype'] == 1]['freq']) 
freqs_nonprotos = list(df[df['prototype'] == 0]['freq']) 
freqs_nonprotos_nonzeros = [i for i in freqs_nonprotos if i > 0] 

np.mean(np.log(freqs_protos))
np.mean(np.log(freqs_nonprotos_nonzeros))

# violin plot 
data_protos = [np.log(i) for i in freqs_protos]
data_nonprotos = [np.log(i) for i in freqs_nonprotos if i > 0]

pos = [1,2]
plotnames = ('Prototypes','Non-prototypes')
plt.figure()
plt.violinplot([data_protos,data_nonprotos],pos)
plt.title('Frequency densities of Zapotec prototypes')
plt.xticks(pos,plotnames)
plt.ylabel('Log Frequency')
plt.show()
