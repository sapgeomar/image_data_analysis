########################################################################################################################
################################### Sahed Ahmed Palash, Biological Oceanography, GEOMAR ################################
############ Master Thesis, Data Analysis, Counting the zooplankton for large size fraction ##########################

######## importing the packages ########

import pandas as pd
import matplotlib.pyplot as plt
import csv

#### reading the csv file using pandas ######

count_file = pd.read_csv("/home/anonyx/Desktop/office/ecotaxa_export_medium.csv", "\t")

df_count=pd.DataFrame({"category":count_file["object_annotation_category"],
                       "haul_net_id": count_file["process_id"],
                       "area": count_file["object_area"]})    ### renaming the "process id" as "net" because they are in group order
df_count["count"]=1                                                       # creating a new column "counter" to count the categoies #


## getting the desired data from the datafile ####

net_d = df_count["haul_net_id"].str.split("_", expand = True)[3]     ### spliting the haul id column
df_count["net"] = net_d                                            ### getting the net id and haul id as a new column ####

haul_d = df_count["haul_net_id"].str.split("_", expand = True)[2] ### spliting haul id column
df_count["haul"]=haul_d   ### getting the haul id as a new column ###

df_grouped=df_count.groupby(["haul", "net", "category", "area"]).count()  ### grouping by the columns to create a dataframe###

df_sorted= df_count.loc[df_count['category'].isin(["Calanoida", "Eucalanidae", "Oithonidae","Oithona" "Oncaeidae",\
                                                   "Corycaeidae", "Euphausiacea", "Pleuroncodes"]).reset_index(drop=True)]                                             ### getting the category data from the dataframe ###
df_sorted_reindex=df_sorted.reset_index()
#print(df_sorted_reindex)

### creating a dataframe with id and count ####

data_sorted=df_sorted.groupby(["haul", "net" ,"category"]).sum()        #["counter"].size() # compute the size of the category ##
data_grouped_reindex=data_sorted.reset_index()                           ### reseting the column names arrordingly ###

#### calculation of biomass

biomass_dict = {"Calanoida" : [43.38, 1.54],
                "Oithona":[43.38, 1.54],
                "Pleuroncodes":[43.97, 1.52],
                "Eucalanidae" : [43.38, 1.54],
                "Corycaeidae": [43.38, 1.54],
                "Oithonidae" :[43.38, 1.54],
                "Oncaeidae":[43.38, 1.54],
                "Euphausiacea": [49.58,1.48]}

#convert area (pixel) into mm⁻², area is in pixel which is the magical number 0.00011236 µm #####

fn=lambda row:biomass_dict[row["category"]][0]*row["area"]*0.00011236**biomass_dict[row["category"]][1]  #df[0]**float(j)
col=data_grouped_reindex.apply(fn, axis=1)
df_grouped_reindex=data_grouped_reindex.assign(biomass_cal=col.values)

#print(df_grouped_reindex)

## importing mean multinet data file and read it ###

mean_file = pd.read_csv("/home/anonyx/Desktop/office/meanData_mn_towed_version.txt", "\t")

haul_id = mean_file["haul"].str.split("_", expand = True)[1]                         ### spliting haul id column by "_" and get the mn haul
mean_file["haul"]=haul_id
haul_id_1 = mean_file["haul"].str.split(".", expand = True)[0]                       ### spliting haul again by "." to get rid of .txt
mean_file["haul"]=haul_id_1
mean_file['net'] = 'n' + mean_file['net'].astype(str)                               ### adding a letter "n" to a string


#### merging the count file and mean data file together ####

df_merged=pd.merge(df_grouped_reindex, mean_file,  how='left', on=['haul','net'])
df_merged=df_merged.reset_index()
df_merged = df_merged.drop('index', 1)


##### creating dictionary for day and night mn files to join in df_merged dataframe ####

data = {"haul": ["mn01", "mn02", "mn03", "mn04", "mn05", "mn06", "mn07", "mn08", "mn09", "mn10", \
                 "mn11", "mn12", "mn13", "mn14", "mn15", "mn16"], "D_N": ["D", "N", "D", "N", "N", "D", "N", "D", "N",\
                                                                          "D", "D", "N", "D", "N", "D", "N"]}

DN_df=pd.DataFrame.from_dict(data)                                       ##### creatina dataframe from the D/N dict ###


######### merging data file with df_merged data file to join day and night on multinet ########

final_df=pd.merge(df_merged, DN_df, on="haul", how="left")

####### creating a column for the spliting ratio and merge with haul and net #######

split_df=pd.read_csv("/home/anonyx/Desktop/office/M138_med_scan_filenames.txt", sep="_")   ### reading the ratio file
df_ratio=split_df.drop(['m138t', '1a.tif', "med"], axis=1, inplace=True)    ### remove multiple columns
df_ratio_rm=split_df.iloc[::2]                                                ### remove duplicate rows
df_ratio_rm1=df_ratio_rm.rename({"mn01":"haul", "n1":"net", "8":"ratio"}, axis=1)
df_ratio_rm1.reset_index(inplace=False)                                         ### reindexing
#df_ratio_rm = ['haul', 'net', " split"]
#split_df.to_csv("ratio.txt", sep='\t', encoding='utf-8')
#df_ratio_col = df_ratio_rm.rename({'mn01':'haul', ' n1':'net', '8':'ratio" axis=1)
#print(df_ratio_rm1)

#### merging final datafrma and split ratio #######

df_final=pd.merge(final_df, df_ratio_rm1, how='left', on=['haul','net'])

#df_final.to_csv("df2.txt", sep='\t', encoding='utf-8')

#### creating function to calculate abundaance (abundance=total count/volume of water [L⁻¹])

fn=lambda row:row["count"]*row["ratio"]/row["volume"]
col=df_final.apply(fn, axis=1)
df_final=df_final.assign(abundance=col.values)
#print(df_final)

####### integrated abundance (multiplying the delta value of depth with biomass (m⁻³) to get in (m⁻²),
# delta value is the difference between net opening and closing)######

fn=lambda row:row["delta_values"]*row["abundance"]
col=df_final.apply(fn, axis=1)
df_final=df_final.assign(integrated_abundance=col.values)

#### biomass/volume [µg/m⁻³] #####

fn=lambda row:row["biomass_cal"]/row["volume"]
col=df_final.apply(fn, axis=1)
df_final=df_final.assign(biomass=col.values)


##### calculating the integrated biomass (multiplying the delta value of depth with biomass (m⁻³) to get in (m⁻²),
# delta value is the difference between net opening and closing)
fn=lambda row:row["delta_values"]*row["biomass"]
col=df_final.apply(fn, axis=1)
df_final=df_final.assign(integrated_biomass=col.values)
df_final.to_csv("m138t_mn_midi_dataframe_medium.txt", sep="\t", encoding="utf-8")



