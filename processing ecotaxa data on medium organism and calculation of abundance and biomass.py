# Sahed Ahmed Palash, Biological Oceanography, GEOMAR
# Master Thesis, Data Analysis
# processing the ecotaxa and multinet mean value together for the medium size fraction

# import important packages
import pandas as pd
import matplotlib.pyplot as plt
import csv

# reading ecotaxa output file for the medium size fraction using pandas
count_file = pd.read_csv("/home/sahed/Desktop/office/3.ecotaxa_export_medium.csv", "\t")
df_count=pd.DataFrame({"category":count_file["object_annotation_category"],
                       "haul_net_id": count_file["process_id"],
                       "area": count_file["object_area"]})                              # renaming columns
df_count["count"]=1                                                                     # new column for counting
net_d = df_count["haul_net_id"].str.split("_", expand = True)[3]                        # split haul id
df_count["net"] = net_d                                                                 # creating net id column
haul_d = df_count["haul_net_id"].str.split("_", expand = True)[2]                       # split again
df_count["haul"]=haul_d                                                                 # creating haul id
df_grouped=df_count.groupby(["haul", "net", "category", "area"]).count()                # grouping the dataframe with count

# sort the dataframe based on specifci categories
df_sorted= df_count.loc[df_count['category'].isin(["Calanoida", "Eucalanidae", "Oithona","Euphausiacea",\
                                                   "Pleuroncodes"]).reset_index(drop=True)]
df_sorted_reindex=df_sorted.reset_index()                                               # reindexing
data_sorted=df_sorted.groupby(["haul", "net" ,"category"]).sum()                        # grouping with sum
data_grouped_reindex=data_sorted.reset_index()                                          # reindexing

# biomass calculation by creating a dictionary with intercept and slope from " Lehette and Hernández-León, 2011"
biomass_dict = {"Calanoida" : [43.38, 1.54],
                "Oithona":[43.38, 1.54],
                "Pleuroncodes":[43.97, 1.52],
                "Eucalanidae" : [43.38, 1.54],
                "Euphausiacea": [49.58,1.48]}

#convert area (pixel) into mm⁻², area is in pixel which is the magical number 0.00011236 µm (calculated biomass in df)
fn=lambda row:biomass_dict[row["category"]][0]*row["area"]*0.00011236**biomass_dict[row["category"]][1]
col=data_grouped_reindex.apply(fn, axis=1)                                                 # reindexing dataframe
df_grouped_reindex=data_grouped_reindex.assign(biomass_cal=col.values)                     # creating biomass column

# open file with multinet ctd mean value
mean_file = pd.read_csv("/home/sahed/Desktop/office/1.meanData_mn_towed.txt", "\t")
haul_id = mean_file["haul"].str.split("_", expand = True)[1]                               # split haul to get rid "-"
mean_file["haul"]=haul_id
haul_id_1 = mean_file["haul"].str.split(".", expand = True)[0]                             # get rid of ".text"
mean_file["haul"]=haul_id_1
mean_file['net'] = 'n' + mean_file['net'].astype(str)                                      # add letter "n" to a string

# merge multinet ctd mean value dataframe and ecotaxa count dataframe
df_merged=pd.merge(df_grouped_reindex, mean_file,  how='outer', on=['haul','net'])
df_merged=df_merged.reset_index()
df_merged = df_merged.drop('index', 1)                                                     # delete column 1

data = {"haul": ["mn01", "mn02", "mn03", "mn04", "mn05", "mn06", "mn07", "mn08",\
                 "mn09", "mn10", "mn11", "mn12", "mn13", "mn14", "mn15", "mn16"],\
        "D_N": ["D", "N", "D", "N", "N", "D", "N", "D", "N", "D", "D", "N", "D",\
                "N", "D", "N"]}                                                            # dict for day and night hauls                                                           # dict for day and night hauls

DN_df=pd.DataFrame.from_dict(data)                                                         # dict to column in dataframe
final_df=pd.merge(df_merged, DN_df, how="left", on="haul")                                 # merging two dataframe

# reading the scan file and create a column for the spliting ratio and merge with haul and net
split_df=pd.read_csv("/home/sahed/Desktop/office/metaData_scanFile_shipLog/M138_med_scan_filenames.txt", sep="_")
df_ratio=split_df.drop(['m138t', '1a.tif', "med"], axis=1, inplace=True)                   # remove multiple columns
df_ratio_rm=split_df.iloc[::2]                                                             # remove duplicate rows
df_ratio_rm1=df_ratio_rm.rename({"mn01":"haul", "n1":"net", "8":"ratio"}, axis=1)          # renaming the columns
df_ratio_rm1.reset_index(inplace=False)                                                    # reindexing
df_final=pd.merge(final_df, df_ratio_rm1, how='left', on=['haul','net'])                   # marging dataframes

# creating a function to calculate abundance (abundance=total count/volume of water [L⁻¹])
fn=lambda row:row["count"]*row["ratio"]/row["volume"]
col=df_final.apply(fn, axis=1)                                                             # apply the function
df_final=df_final.assign(abundance=col.values)                                             # with new column

#### creating a function to calculat the exact biomass (formula: biomass = calculated biomass/volume [µg/m⁻³])
fn=lambda row:row["biomass_cal"]/row["volume"]
col=df_final.apply(fn, axis=1)                                                             # apply the function
df_final=df_final.assign(biomass=col.values)                                               # with new column

# saving the dataframe as a txt file

df_final.to_csv("3. m138t_mn_midi_dataframe_medium.txt", sep="\t", encoding="utf-8")





