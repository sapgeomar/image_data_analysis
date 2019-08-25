# Sahed Ahmed Palash, Biological Oceanography, GEOMAR
# Master Thesis, Data Analysis
# creating a plot wit environmental parameters of all the stations

# impoting necessary packages

import codecs                                                                               # used for encode and decode
import matplotlib.pyplot as plt                                                             # for ploting
import numpy as np                                                                          # for mathmatical functions
import pandas as pd                                                                         # for dataframe
import seaborn as sns                                                                       # for ploting
import seawater as sw                                                                       # calculating depth

# creating a dictionary of multinet ctd and cruise ctd with all other relavent information
dict = {"m138t_mn01.txt":["met_138_1_011.ctd", 0.1, 0.79, "D", "Station 1 (offshore)", "-10.888"],
        "m138t_mn02.txt":["met_138_1_013.ctd", 0.1, 0.79, "N", "Station 1", "-10.951"],
        "m138t_mn03.txt":["met_138_1_014.ctd", 0.5, 0.79, "D", "Station 2 (onshore)", "-10.761" ],
        "m138t_mn04.txt":["met_138_1_017.ctd", 0.5, 0.79, "N", "Station 2", "-10.777" ],
        "m138t_mn06.txt":["met_138_1_041.ctd", 0.1, 0.55, "D", "Station 3 (offshore)", "-12.414"],
        "m138t_mn05.txt":["met_138_1_038.ctd", 0.1, 0.55, "N", "Station 3", "-12.412"],
        "m138t_mn08.txt":["met_138_1_051.ctd", 0.5, 0.55, "D", "Station 4 (onshore)", "-12.212"],
        "m138t_mn07.txt":["met_138_1_049.ctd", 0.5, 0.55, "N", "Station 4", "-12.212"],
        "m138t_mn11.txt":["met_138_1_068.ctd", 0.1, 0.31, "D", "Station 5 (offshore)", "-14.297"],
	    "m138t_mn12.txt":["met_138_1_071.ctd", 0.1, 0.31, "N", "Station 5", "-14.277"],
        "m138t_mn10.txt":["met_138_1_064.ctd", 0.5, 0.31, "D", "Station 6 (onshore)", "-14.001"],
        "m138t_mn09.txt":["met_138_1_060.ctd", 0.5, 0.31, "N", "Station 6", "-14.001"],
        "m138t_mn15.txt":["met_138_1_086.ctd", 0.1, 0.06, "D", "Station 7 (offshore)", "-15.861"],
        "m138t_mn16.txt":["met_138_1_090.ctd", 0.1, 0.06, "N", "Station 7", "-15.860"],
        "m138t_mn13.txt":["met_138_1_070.ctd", 0.5, 0.06, "D", "Station 8 (onshore)", "-15.424"],
        "m138t_mn14.txt":["met_138_1_074.ctd", 0.5, 0.06, "N", "Station 8", "-15.430"]}

data_frame_exist = 0                                                                        # calling a binary

fig=plt.figure(figsize=[8,10])

# creating a for loop with the multinet filename in the dictionary
for mn_filename in dict:
    ctd_filenamelist = dict[mn_filename][0]
    x_pos = dict[mn_filename][1]
    y_pos = dict[mn_filename][2]
    D_N=dict[mn_filename][3]
    station_id = dict[mn_filename][4]
    lat=dict[mn_filename][5]

    # creating empty lists for ctd
    ctd_pressure = []
    ctd_o2 = []
    ctd_index = []
    ctd_salinity = []
    ctd_temp = []
    ctd_depth = []

    # import the ctd files
    ctd = codecs.open("/home/sahed/Desktop/office/m138_ctd/" + ctd_filenamelist, "r", encoding="utf-8", errors="ignore")
    line_counter = 0  # adding new line
    xyz = 0  # calling a binary
    for line in ctd:  # iterating over each line
        if xyz == 0:  # skippinng the text
            if "tim:p" in line:
                xyz = 1  # !!!!!!
                continue
        else:
            element_list_2 = line.strip().split()  # seperating the lines
            # print(element_list_2)
            depth = float(element_list_2[2])
            if depth <= 150:
                oxygen = float(element_list_2[5])
                ctd_o2.append(oxygen)
                ctd_depth.append(depth)
                temp = float(element_list_2[3])
                ctd_temp.append(temp)
                salinity = float(element_list_2[4])
                ctd_salinity.append(salinity)

        line_counter += 1

    # creating the plot
    if D_N == "D":
        sns.set_style("ticks")
        sns.set_context("paper")
        ax = fig.add_axes([x_pos, y_pos, 0.32, 0.13])
        ax.plot(ctd_o2, ctd_depth, lw=3, color="black", alpha= 0.7,label="daytime ox.")
        plt.title(station_id, fontsize=10, y=1.33)
        ax.set_ylabel("Depth [m]", fontsize=8)
        ax.set_ylim(160, 0)
        ax.set_xlabel("Oxygen [µmol/kg]", fontsize=8)
        ax.plot(0, 0, '-r', label='daytime temp.', lw=3, color="red")                     # creating additional label
        plt.xlim(-15,275)
        ax1 = ax.twiny()
        ax1.set_xlabel("Temperature [°C]", fontsize=8)
        ax1.set_xlim(13,21)
        ax1.plot(ctd_temp, ctd_depth, lw=3, color="r", alpha=0.6)

    if D_N == "N":
        sns.set_style("ticks")
        sns.set_context("paper")
        ax = fig.add_axes([x_pos, y_pos, 0.32, 0.13])
        ax.plot(ctd_o2, ctd_depth, ls="--", color="black", lw=2, label="nighttime ox.", alpha=1)
        ax.plot(0, 0, '-r', label='nighttime temp.', ls=":", lw=3, color="red")
        ax1.plot(ctd_temp, ctd_depth, ls="--", lw=3, color="r", label="nighttime temp.", alpha=1)
        legend = plt.legend(loc='lower right', shadow=True, fontsize='small')

plt.savefig("9.ctd_Profile.png", dpi=300)
#plt.show()
plt.close()

