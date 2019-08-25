# Sahed Ahmed Palash, Biological Oceanography, GEOMAR
# Master Thesis, Data Analysis
# Plotting biomass

#import necessary packages/libraries
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# reading through the datafile with latitude and longitude informations
mn_biomass = pd.read_csv("/home/sahed/Desktop/office/4. m138t_mn_midi_final_dataframe.txt", "\t")
mn_biomass = mn_biomass.groupby('haul')["integrated_biomass"].sum()                                   # grouping the dataframe
mn_biomass=mn_biomass.reset_index()                                                        # re-indexing
print(mn_biomass)
quit()

# constructing the map using basemap library
map =Basemap(projection='merc',llcrnrlat=-17,urcrnrlat=-9, llcrnrlon=-80,urcrnrlon=-73,resolution='h')
map.drawmapboundary(fill_color='aqua')                                                     # creating map boundary lines
map.fillcontinents(color='grey',lake_color='aqua')                                         # creating continent
map.drawcoastlines()                                                                       # creating coastline
parallels= np.arange(-17.,-09.,2.)                                                         # creating grid for latitude
map.drawparallels(parallels, labels=[False,True,True,False])
meridians= np.arange(-79.,-73.,2.)                                                         # creating grid for longitude
map.drawmeridians(meridians, labels=[True,False,False,True])

# constructing biomass with factor on the map

lats = [-10.888, -10.951, -10.761, -10.778, -12.412, -12.414, -12.212, -12.212333,\
        -14.001, -14.0015, -14.297, -14.277, -15.424, -15.430, -15.861, -15.860]
lons = [-78.5685, -78.564, -78.271, -78.270, -77.813, -77.812, -77.439, -77.439,\
         -76.660, -76.660, -77.169, -77.177, -75.444, -75.44, -76.105, -76.106]

#lons=mn_biomass["longitude"].tolist()                                                      # creating list from column
#lats=mn_biomass["latitude"].tolist()                                                       # creating list from column
biomass_list = mn_biomass["integrated_biomass"].tolist()                                              # creating list from column
# setting the factor to to have the size fractioning visualization of biomass over the map
factor=200000                                                                              # changeable depending on size
biomass = np.divide(biomass_list, factor)                                                  # quotient determine the size of the visual represntation

# creating the map using tissot (representation of a circle on the map)
iterator = range(0,len(biomass_list))
for i in iterator:                                                                         # tissot can not be used on lists, need to loop through
    map.tissot(lons[i],lats[i], biomass[i], 20, edgecolor = 'k', facecolor='b', alpha=1)

# creating legends for the size fractioning of the biomass circles on the map
fac_list= [0.3, 0.2, 0.1, 0.04]                                                           # quotient for size of visual representation
lat_list=[-12, -12.7, -13.2, -13.6]                                                        # latitudinal position of the legends
lon = -74                                                                                  # logitudinal position of the legends
label_list= ["60000 µgCm⁻²", "40000 µgCm⁻²", "20000 µgCm⁻²", "8000 µgCm⁻²"]             # text in the legends
for i in range(0,len(label_list)):                                                         # iterating ove the label list
    map.tissot(-74.9, lat_list[i], fac_list[i], 20, edgecolor='k', facecolor='g', alpha=1)   # tissot map

# annotating the label list and text over the map

a, b = map(-73.4, -12)                                                                     # long and lats for labels
c, d = map(-73.4, -12.6)
e, f = map(-73.4, -13.1)
g, h = map(-73.4, -13.5)
x, y = map(-75.4, -11.5)
a2, b2 = (-73, -9)                                                                         # long and lats for the whole map
plt.annotate(label_list[0], xy=(a, b), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=13)
plt.annotate(label_list[1], xy=(c, d), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=12)
plt.annotate(label_list[2], xy=(e, f), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=11)
plt.annotate(label_list[3], xy=(g, h), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=10)
plt.annotate("Lima", xy=(x,y), xytext=(a2, b2), textcoords='offset points',color='yellow', fontsize=18)

# Mapping station names
i,j = map(-77.7, -11.1)
k,l = map(-77.3, -10.3)
m,n = map(-76.9, -12.6)
o,p = map(-76.5, -11.8)
q,r = map(-75.7, -13.5)
s,t = map(-76.3, -14.5)
u,v = map(-74.5, -15.2)
w,z = map(-75.2, -16)
plt.annotate("st1", xy=(i,j), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st2", xy=(k,l), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st3", xy=(m,n), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st4", xy=(o,p), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st6", xy=(q,r), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st5", xy=(s,t), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st8", xy=(u,v), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.annotate("st7", xy=(w,z), xytext=(a2, b2), textcoords='offset points',color='black', fontsize=14)
plt.show()

# save the fig as png
#plt.savefig("8. Biomass_distribution.png", dpi=300)
