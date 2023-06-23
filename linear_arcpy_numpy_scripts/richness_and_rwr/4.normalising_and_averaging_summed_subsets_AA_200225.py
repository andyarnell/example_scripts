#ran using arcpy (arcpro version)
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
import numpy as np

arcpy.CheckOutExtension("Spatial")# Check out the ArcGIS Spatial Analyst extension license
arcpy.env.overwriteOutput = True # allow overwrite of tifs

########### setting parameters
gdbName = "aoh_summing/all_sp_rwr"
extension = ".tif"
tempFolder = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020"
rawFolder = tempFolder+os.path.sep+gdbName
arcpy.env.workspace = rawFolder
inputRasterPrefix = "all_summed_*"
outputRasterPrefix= "all_sp_rwr_binaryInputs"
#outputRasterPrefix= "all_sp_richness_binaryInputs"
mask = Raster(tempFolder+"/"+"globalgrid_mollweide_10km.tif")#terrestrial 10km raster with proportion of land as value
mask = SetNull(mask,mask,"Value < 500")#make a mask to only keep cells where majority of pixel is landcover 

file_list = arcpy.ListRasters(inputRasterPrefix,"TIF") 
print (file_list)
splists = list(["splist1","splist2","splist3","splist4","splist5","splist6","splist7","splist8","splist9","splist10"])

#normalising (stretching 0-1) each of the ten rasters (one for each of the ten sets)
for file in file_list:
    rst = arcpy.Raster(file)
    max_val = np.max(arcpy.RasterToNumPyArray(rst))
    print (file)
    print (max_val)
    outRas = Divide(rst,float(max_val))
    outRas.save(tempFolder+os.path.sep+gdbName+os.path.sep+"normalised_"+file+".tif")

#select output normalised rasters from above
file_list = arcpy.ListRasters("normalised_*","TIF")
#set counter
i=0
#loop through new file list and sum them all together 
for rst in file_list:
    rst = Raster(rst)
    if i == 0:
        outRas = rst
        i += 1
##        print ("Summed raster: " + str(rst)+" raster number:"+str(i))
    else:
        outRas = outRas + rst
        i += 1
##        print ("Summed raster: " + str(rst)+" raster number:"+str(i))

#divide by 10 (so taking the average)
outRas = Divide(outRas,int(len(file_list)))

#export output raster
sr = tempFolder+os.path.sep+gdbName+os.path.sep+outputRasterPrefix+"all_sets_combined.tif"
outRas.save(sr)

print("saved output raster: "+sr)

#select only raster cells where over 50% of the raster is land (based on the mask - see above)
out_raster = arcpy.sa.ExtractByMask(outRas, mask);
sr = tempFolder+os.path.sep+gdbName+os.path.sep+outputRasterPrefix+"all_sets_combined_majorityMasked.tif"
out_raster.save(sr)
print("saved output raster majority masked: "+sr)

print("Finished all processing")

