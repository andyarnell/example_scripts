#ranking cells in a raster
print ("Importing packages")
import os
import arcpy
from arcpy import env
from arcpy.sa import *
import string
import math
import pandas as pd
import numpy as np
import scipy.stats as ss
from scipy.stats import rankdata
arcpy.CheckOutExtension("Spatial")# Check out the ArcGIS Spatial Analyst extension license
arcpy.env.overwriteOutput = True # allow overwrite of tifs
########### setting parameters
gdbName = "aoh_summing"
extension = ".tif"
tempFolder = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020" 
file_suffix = ""##os.path.sep+"richness change depending
template_rst_name = "rwrall_sets_combined.tif"
mask = Raster(tempFolder+"/"+"globalgrid_mollweide_10km.tif")
mask = SetNull(mask,mask,"Value < 500")
rawFolder = tempFolder+os.path.sep+gdbName

sr = tempFolder+os.path.sep+gdbName+file_suffix+"all_sets_combined_rank_masked_majorityMask.tif"##outpath
arcpy.env.workspace = rawFolder

def NumPyArrayToRasterViaTemplate(npArray,templateRst):
    arcpy.env.outputCoordinateSystem = templateRst
    cellsizex=float(arcpy.GetRasterProperties_management(templateRst,"CELLSIZEX").getOutput(0))
    cellsizey=float(arcpy.GetRasterProperties_management(templateRst,"CELLSIZEY").getOutput(0))
    return arcpy.NumPyArrayToRaster(npArray, arcpy.Point(templateRst.extent.XMin, templateRst.extent.YMin),cellsizex,cellsizey)

file_list = arcpy.ListRasters(template_rst_name,"TIF")
print(file_list[0])
rst = Raster(file_list[0])
templateRst = rst


array = arcpy.RasterToNumPyArray(rst)
#array = ss.rankdata(array)


a = numpy.copy(array)

a = rankdata(a,method='dense').reshape(a.shape)
#a = (a.max()+1) - a
a = a/a.max()
#minVal = a.min()
rst = NumPyArrayToRasterViaTemplate(a,templateRst)
#rst.save(sr)
##exp ="VALUE ="+str(minVal)
##print (exp)#value to turn into null
##rst1 = SetNull(rst,rst,exp)
##rst1.save(sr)
out_raster = arcpy.sa.ExtractByMask(rst, mask);
out_raster.save(sr)
