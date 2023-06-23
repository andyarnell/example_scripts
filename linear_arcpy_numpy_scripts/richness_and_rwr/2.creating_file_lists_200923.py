##aim: make a list of rasters and their filenames into a csv for processing in seperate script
##created by Andy Arnell 29/06/2015
print ("Importing packages")
import os
import arcpy
from arcpy import env
from arcpy.sa import *
import glob
import string
import math
import time
import pandas as pd
arcpy.CheckOutExtension("Spatial")# Check out the ArcGIS Spatial Analyst extension license
arcpy.env.overwriteOutput = True # allow overwrite of tifs
########### setting parameters
batchsize=50#size of each batch - adjust if crashing due to memory
print ("batchsize: "+str(batchsize))
beginTime = time.clock()
gdbName = "aoh_summing/"
extension = ".tif"
tempFolder = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020" 
rawFolder = tempFolder
clean_col = "fullPathClean"
clean_col2 = "fullPathCleanIDNO" ###only for sept 2020 run where two possible merges were carried out
filename_csv = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020\feature_data_list.csv"
#filename_csv = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020\feature_data_list_threatened_plants_and_IUCN_Vert.csv"
#################
join_file_root=(rawFolder+os.path.sep+"sets")#+os.path.sep+"sets")
actual_filepaths = pd.read_csv(os.path.join(tempFolder,gdbName,"filenames.csv"))
print (actual_filepaths.head())

#add fields to join on: firstly by id_no (some have this as first element of the tif) then by binomial (last two elements of tif)
##actual_filepaths[clean_col] = actual_filepaths["root"]+os.path.sep+actual_filepaths["filename"].str.lower().str.replace(" ","_")
##actual_filepaths[clean_col2] = actual_filepaths["root"]+os.path.sep+actual_filepaths["filename"].str.lower().str.replace(" ","_")

actual_filepaths[clean_col2] = actual_filepaths["filename"].str.lower().str.replace(" ","_").str.replace(".tif","").str.split("_").str[0]
actual_filepaths[clean_col] = actual_filepaths["filename"].str.lower().str.replace(" ","_").str.replace(".tif","").str.split("_").str[-2]+"_"+actual_filepaths["filename"].str.lower().str.replace(" ","_").str.replace(".tif","").str.split("_").str[-1]
print ("actual filepaths size", actual_filepaths[clean_col].size)

actual_filepaths.to_csv(os.path.join(tempFolder,gdbName,"actual_filepaths_check.csv"))
##########################################
print("Elapsed time (minutes): " + str((time.clock() - beginTime)/60))
left_col = "iucn_id_no" # joining column name from filename_csv input
right_col = "x" # joining column name from join_file input
#join to subset if there is one
files = pd.read_csv(filename_csv)
#df.loc[df['column name'] condition, 'new column name'] = 'value if condition is met'

#add fields to join on: firstly by id_no (some have this as first element of the tif) then by binomial (last two elements of tif)
##
##files[clean_col2] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"].map(str)+ "__"+files["binomial"].str.lower().str.replace(" ","_")+".tif"
##print (files.head())
##files[clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["fname"].str.lower().str.replace(" ","_")

files[clean_col2] = files["iucn_id_no"].map(str)
files[clean_col] = files["binomial"].str.lower().str.replace(" ","_")


##files.loc[files.folder == "AVES_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")
##files.loc[files.folder == "AMPHIBIA_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")
##files.loc[files.folder == "MAMMALIA_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")
##files.loc[files.folder == "REPTILIA_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")
##files.loc[files.folder == "MAMMALIA_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")
##files.loc[files.folder == "MAMMALIA_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")
##files.loc[files.folder == "MAMMALIA_10km", clean_col] = rawFolder+os.path.sep+files["folder"]+os.path.sep+files["iucn_id_no"]+ "__"+files["binomial"].str.lower().str.replace(" ","_")

##files.to_csv(rawFolder+os.path.sep+"files_check.csv")

print (files.head())
print ("files df before merge: "+str(files[clean_col2].size))
files2 = pd.merge(files,actual_filepaths,how= "inner",on=clean_col2)
print ("files df after merge: "+str(files[clean_col2].size))
files3 = pd.merge(files,actual_filepaths,how= "inner",on=clean_col)
print ("files df after merge2: "+str(files[clean_col].size))

files2.to_csv(rawFolder+os.path.sep+"files_check_merge2.csv")
files3.to_csv(rawFolder+os.path.sep+"files_check_merge3.csv")
files = files2#.append(files3, ignore_index=False, verify_integrity=False)## coded out merging as not needed now all bnased off one id

files.to_csv(rawFolder+os.path.sep+"files_check.csv")

for suffix in list(["splist1","splist2","splist3","splist4","splist5","splist6","splist7","splist8","splist9","splist10"]):
    join_filename=(suffix+".csv")
    join_file_string = os.path.join(join_file_root,join_filename)
    join_file = pd.read_csv(join_file_string)
    #print (" join_file head:",join_file.head())
    print (" join_file name:",join_filename)
    
    ############
    print ("joinfile size:", join_file[right_col].size)
    files_subset = pd.merge(files,join_file,how= "inner",left_on=left_col,right_on=right_col)
    
##    print ("files_subset size:",files_subset[left_col].size)
##    if files_subset[left_col].size==join_file[right_col].size:
##        print ("ALL_SUBSET_JOINED")
##    else:
##        print ("NOT ALL_SUBSET_JOINED")

    files_subset["folder_priority"] = 0
    files_subset.loc[files_subset.folder == "PLANTAE_10km", 'folder_priority'] = 1
    files_subset.loc[files_subset.folder == "KEW_PLANTAE_IUCN_10km", 'folder_priority'] = 2
    files_subset.loc[files_subset.folder == "KEW_PLANTAE_BGCI_10km", 'folder_priority'] = 3
    files_subset.loc[files_subset.folder == "newPlantPPM_10km", 'folder_priority'] = 4
    files_subset.loc[files_subset.folder == "BIEN_PLANTAE_PPM_10km", 'folder_priority'] = 7
    files_subset.loc[files_subset.folder == "newPlantRangebags_10km", 'folder_priority'] = 5
    files_subset.loc[files_subset.folder == "newPlantPoints_10km", 'folder_priority'] = 6
    files_subset.loc[files_subset.folder == "BIEN_PLANTAE_POINTS_10km", 'folder_priority'] = 8
    print ("files_subset length ",str(files_subset[left_col].size))
    files_subset = files_subset.sort_values(by=['folder_priority'],ascending=True)
    files_subset["duplicate"] = files_subset.duplicated(subset=left_col, keep="first")
    files_subset = files_subset[files_subset.duplicate==False]

    #print (files_subset.head())
    print ("files_subset no dups length ",str(files_subset[left_col].size))
    print ("join file length ",str(join_file[right_col].size))
    join_file_subset = join_file
    join_file_subset["duplicate"] = join_file_subset.duplicated(subset=right_col, keep="first")
    join_file_subset = join_file_subset[join_file_subset.duplicate==False]
    print ("join file no dups length ",str(join_file_subset[right_col].size))
    if files_subset[left_col].size==join_file_subset[right_col].size:
        print ("ALL_SUBSET_JOINED")
    else:
        print ("NOT ALL_SUBSET_JOINED")
        
    files_subset.to_csv(os.path.join(tempFolder,gdbName,"fname_nodups_"+join_filename))
    #print (files_subset.head())
    raster_list = files_subset["fullPath"].tolist()
##    print (len(raster_list))
print("Total elapsed time (minutes): " + str((time.clock() - beginTime)/60))



