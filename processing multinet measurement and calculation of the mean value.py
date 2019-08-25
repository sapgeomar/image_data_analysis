# Sahed Ahmed Palash, Biological Oceanography, GEOMAR
# Master Thesis, Data Analysis
# mutinet meandata processing

# impoting necessary packages

import codecs                                                                               # used for encode and decode
import matplotlib.pyplot as plt                                                             # for ploting
import numpy as np                                                                          # for mathmatical functions
import pandas as pd                                                                         # for dataframe
import seaborn as sns                                                                       # for ploting
import seawater as sw                                                                       # calculating depth

# creating a dictionary of multinet ctd and cruise ctd with all other relavent information
dict = {"m138t_mn01.txt":["met_138_1_011.ctd", "-10.532"],
        "m138t_mn02.txt":["met_138_1_013.ctd", "-10.57"],
        "m138t_mn03.txt":["met_138_1_014.ctd", "-10.456"],
        "m138t_mn04.txt":["met_138_1_017.ctd", "-10.46698"],
        "m138t_mn06.txt":["met_138_1_041.ctd", "-12.248"],
        "m138t_mn05.txt":["met_138_1_038.ctd", "-12.2477"],
        "m138t_mn08.txt":["met_138_1_049.ctd", "-12.127"],
        "m138t_mn07.txt":["met_138_1_049.ctd", "-12.127"],
        "m138t_mn11.txt":["met_138_1_066.ctd", "-14.178"],
	"m138t_mn12.txt":["met_138_1_049.ctd", "-14.166"],
        "m138t_mn10.txt":["met_138_1_049.ctd", "-14"],
        "m138t_mn09.txt":["met_138_1_049.ctd", "-14.001"],
        "m138t_mn15.txt":["met_138_1_074.ctd", "-15.516"],
        "m138t_mn16.txt":["met_138_1_078.ctd", "-15.516"],
        "m138t_mn13.txt":["met_138_1_049.ctd", "-15.254"],
        "m138t_mn14.txt":["met_138_1_049.ctd", "-15.258"]}


data_frame_exist = 0                                                                        # calling a binary

# creating a for loop with the multinet filename in the dictionary
for mn_filename in dict:
    ctd_filenamelist = dict[mn_filename][0]
    lat=dict[mn_filename][1]

# creating empty lists under the for loop
    mn_pressure=[]
    mn_o2=[]
    mn_net=[]
    mn_index=[]
    mn_haul=[]
    mn_volume=[]
    mn_salinity=[]
    mn_temp=[]
    mn_depth=[]

    # open multinet ctd files (upcast only) under the for loop to iterate over all the multinet files
    mn_upcast=codecs.open("/home/sahed/Desktop/office/mn_ctd_t_cor/" + mn_filename, "r", encoding="utf-8", errors="ignore")
    line_counter = 0                                                                        # adding new line
    xyz = False                                                                             # calling a binary
    for line in mn_upcast:                                                                  # to iteraing over each line
        if xyz == False:
            if "Net []	Pressure [dbar]" in line:                                           # skipping the text
                xyz = True
                continue
        else:
            element_list_1=line.strip().split("\t")                                         # seperating the lines
            m = (float(element_list_1[2]))
            net = int(element_list_1[1])
            if m >= 1 and net>=1:
                mn_pressure.append(m)
                o2_mlL = float((element_list_1[-1]))
                mol_volume_o2 = 44.66
                sw_density = float(element_list_1[11])
                o2_µmol = (o2_mlL*mol_volume_o2/sw_density*1000)
                mn_o2.append(o2_µmol)
                #mn_o2.append(o2_µmol + (-9.196871644229978) + (-0.007655474201452)*o2_µmol +\
                             #(0.011910402128384)*m + (-0.000021367427539)*(m*m) +\
                             #(-0.000326456036203)*(m*o2_µmol))     # o2 conversion ml to µmol
                mn_net.append(net)
                mn_index.append(net)
                mn_haul.append(mn_filename)
                volume=float(element_list_1[3])
                mn_volume.append(volume)
                mn_salinity.append(float(element_list_1[9]))
                mn_temp.append(float(element_list_1[7]))
                depth = sw.dpth(m, float(lat))  # calculating depth
                mn_depth.append(depth)

        line_counter += 1

    #creating dataframe with mean value
    mn_dataframe=pd.DataFrame({"haul": mn_haul, "net": mn_net,\
                               "volume": mn_volume,"pressure": mn_pressure, "depth":mn_depth, "o2": mn_o2,\
                               "salinity": mn_salinity, "temp": mn_temp})

    mn_dataframe.loc[mn_dataframe['o2'] < 0, 'o2'] = 0                                      # get rid of negative value

    # creating columns net opening, closing and delta value to calculate the integrated biomass and abundance
    mn_data_mins = mn_dataframe.groupby(["haul", "net", ]).min()
    mn_net_closing= (mn_data_mins["depth"])
    mn_net_closing.name="net_closing"
    mn_data_maxs = mn_dataframe.groupby(["haul", "net", ]).max()
    mn_net_opening=(mn_data_maxs["depth"])
    mn_net_opening.name="net_opening"
    df=pd.concat([mn_net_opening, mn_net_closing], axis=1)
    df=df.reset_index()
    mn_dataframe=mn_dataframe.merge(df, on=["haul", "net"], how="inner")
    mn_dataframe = mn_dataframe.reset_index()

    # creating a column with delta values by subtracting the net opening and closing values
    fn = lambda row: row["net_opening"] - row["net_closing"]
    col = mn_dataframe.apply(fn, axis=1)
    mn_dataframe = mn_dataframe.assign(delta_values=col.values)

    # creating dataframe grouped with mean value
    mn_data_grouped=mn_dataframe.groupby(["haul", "net",]).mean()
    mn_data_grouped.reset_index()

    #appending the each multinet files under the other one by setting aconditionals
    if data_frame_exist==0:
        final_df=mn_data_grouped
        data_frame_exist=1
    else:
        final_df=final_df.append(mn_data_grouped)

# saving the dataframe as a txt file
final_df.to_csv("1.meanData_mn_towed.txt", sep='\t', encoding='utf-8')





