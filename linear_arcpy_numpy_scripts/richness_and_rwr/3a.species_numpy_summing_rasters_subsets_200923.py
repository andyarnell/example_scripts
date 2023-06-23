##aim: 
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
import numpy as np
import gc
arcpy.CheckOutExtension("Spatial")# Check out the ArcGIS Spatial Analyst extension license
arcpy.env.overwriteOutput = True # allow overwrite of tifs
########### setting parameters
batchsize=50#size of each batch - adjust if crashing due to memory
print ("batchsize: "+str(batchsize))
beginTime = time.clock()
gdbName = "aoh_summing/"
extension = ".tif"
tempFolder = r"E:\Andy\p08425_naturemap\working\aoh_richness_rwr_sept2020"
rawFolder = tempFolder
rrarityNumber = 1000#should ues the raster area terrestrial grid due to cells with only partial terrestrial cover?
df = pd.DataFrame(columns=["filename","area","rr"])
globalgridRst = Raster(tempFolder+"/"+"globalgrid_mollweide_10km.tif")
globalgrid = arcpy.RasterToNumPyArray(globalgridRst)
print (globalgrid)
globalgrid[globalgrid<0] = 0
print (globalgrid)

for suffix in list(["splist5","splist6","splist7","splist8","splist9","splist10"]):# ["splist1","splist2","splist3","splist4"
    #suffix="splist3"
    join_filename=suffix+".csv"
    files_subset = pd.read_csv(tempFolder+"/"+gdbName+"fname_nodups_"+join_filename)
    print (files_subset.head())
    raster_list = files_subset["fullPath"].tolist()
    #print (raster_list[:10])
    print (len(raster_list))
    print("Elapsed time (minutes): " + str((time.clock() - beginTime)/60))
    print ("Summing rasters - carried out in batches due to memory limitations")

    arcpy.env.workspace = rawFolder

    beginTime2 = time.clock()
    #############################################
    arcpy.env.workspace = rawFolder
    ##raster_list = arcpy.ListRasters()

    rstlistlen = len(raster_list)

    print ("number of rasters in list to processs: " + str(rstlistlen))
    ##print ("rasters in list to processs: " + str(raster_list))

    #to work properly need to ensure number of rasters in raster list is rounded up by one batch as last iteration not run otherwise
    #use a rounding up function to do this
    def NumPyArrayToRasterViaTemplate(npArray,templateRst):
        arcpy.env.outputCoordinateSystem = templateRst
        cellsizex=float(arcpy.GetRasterProperties_management(templateRst,"CELLSIZEX").getOutput(0))
        cellsizey=float(arcpy.GetRasterProperties_management(templateRst,"CELLSIZEY").getOutput(0))
        return arcpy.NumPyArrayToRaster(npArray, arcpy.Point(templateRst.extent.XMin, templateRst.extent.YMin),cellsizex,cellsizey)

    def roundup(x,y):
        return int(math.ceil(x / float(y))) * y

    roundUpVal=roundup(rstlistlen,batchsize)
    print ("roundup val: "+str(roundUpVal))

    #use range function to create list of batch intervals to iterate through
    ints = list(range(0,roundUpVal,batchsize))
    print ("ints : "+str(ints))

    #add extra value to end of list
    ints.append(roundUpVal)
    
   
    print (ints)
    print (range(len(ints)-1))
    j = 0
    for j in range(len(ints)-1):
        i = 0
        rstlist0 = raster_list[ints[j]:ints[j+1]]
        rstlist1 = raster_list[ints[j]+1:ints[j+1]]
        templateRst = globalgridRst#arcpy.Raster(rstlist0[0])
        sr = tempFolder+"/"+gdbName+"summedrst"+suffix+"_"+str(j)+extension
        #print ("rst list0"+str(rstlist0))
        #print ("rst list1"+str(rstlist1))
        if j==0:            
            for rstStr in rstlist0:
                rst = Raster(rstStr)
                array = arcpy.RasterToNumPyArray(rst)
                array[array<0] = 0
                array[array>0] = 1
                #area = np.sum(array)#range rarity code
##                if area >0:
##                    #rr = rrarityNumber/area#range rarity code
##                    rr = np.divide(globalgrid,float(area))#range rarity code
##                else:
##                    rr = float(0)
##                    print ("empty raster - skipping")
                #array = np.multiply(array,rr)  
                if i == 0:
                    summedArray = np.copy(array)
                    i+=1
                else:
                    summedArray = np.add(np.copy(summedArray),np.copy(array))
                i+=1    
                print ("Summed raster: " + str(rstStr)+" raster number:"+str(i))                  
                #df = df.append({"filename":rstStr,'area':area,"rr":rr},ignore_index=True)
                array = None
                del(array)
##                del(rr)
                rst = None
                del(rst)
                #gc.collect()
            #df.to_csv(tempFolder+os.path.sep+suffix+"_sp_areas.csv")            
            print ("Saving final summed raster: " + sr) 
            NumPyArrayToRasterViaTemplate(summedArray,templateRst).save(sr)
            summedArray = None
            del(summedArray)
            gc.collect()
        else:
            for rstStr in rstlist0:
                rst = Raster(rstStr)
                array = arcpy.RasterToNumPyArray(rst)
                array[array<0] = 0
                array[array>0] = 1
##                area = np.sum(array)#range rarity code5
##                if area >0:
##                    #rr = rrarityNumber/area#range rarity code
##                    rr = np.divide(globalgrid,float(area))#range rarity code
##                else:
##                    rr = float(0)
##                    print ("empty raster - skipping")
##                array = np.multiply(array,rr)  
                if i == 0:
                    summedArray = np.copy(array)
                    i+=1
                else:
                    summedArray = np.add(np.copy(summedArray),np.copy(array))
                i+=1    
                print ("Summed raster: " + str(rstStr)+" raster number:"+str(i))                  
                #df = df.append({"filename":rstStr,'area':area,"rr":rr},ignore_index=True)
                array = None
                del(array)
##                del(rr)
                rst = None
                del(rst)
                gc.collect()
            #df.to_csv(tempFolder+os.path.sep+suffix+"_sp_areas.csv")
            print ("Saving final summed raster: " + sr) 
            NumPyArrayToRasterViaTemplate(summedArray,templateRst).save(sr)
            summedArray = None
            del(summedArray)
            gc.collect()
                       
    print("Elapsed time (minutes): " + str((time.clock() - beginTime2)/60))

    beginTime3 = time.clock()

    print ("Combining the summed values of each batch of rasters")
    arcpy.env.workspace = tempFolder+"/"+gdbName
    toFind = "summedrst"+suffix+"*"

    raster_list = arcpy.ListRasters(toFind,"TIF")
    print ("There are " + str(len(raster_list)) + "batches in list :" + str(raster_list))

    i=0
    for rst in raster_list:
                rst = Raster(rst)
                if i == 0:
                    outRas = rst
                    i += 1
                    print (gdbName+"Summed raster: " + str(rst)+" raster number:"+str(i))
                else:
                    outRas = outRas + rst
                    i += 1
                    print (gdbName+"Summed raster: " + str(rst)+" raster number:"+str(i))

    srAll = tempFolder+"/"+gdbName+"all_summed_rasters_"+suffix+extension
    print ("Saving to :" + srAll)
    outRas.save(srAll)

    print("Elapsed time (minutes): " + str((time.clock() - beginTime3)/60))

    print ("Finished processing")

    print ("N.B. If equal area grid isn't used for species this has to be taken into account by some kind of area wweighted richness")

print("Total elapsed time (minutes): " + str((time.clock() - beginTime)/60))
print("End of processing subsets")
