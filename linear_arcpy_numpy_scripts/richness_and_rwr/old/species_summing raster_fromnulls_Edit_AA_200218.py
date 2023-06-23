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


batchsize=100
print ("batchsize: "+str(batchsize))
print ("Setting local parameters and inputs")

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True

beginTime = time.clock()

#Set environment settings

##
##snapgrid = "C:/Data/geo6/raw/grids/snapgrid_dd" # provide a default value if unspecified
##sg=Raster(snapgrid)
##
##arcpy.env.extent= sg.extent
##print "Extent: " + str(arcpy.env.extent)
##arcpy.env.snapRaster=sg
##print "Snap raster: "+str(arcpy.env.snapRaster)

#raster_list = arcpy.ListRasters()
#dataset = raster_list[0]
#spatial_ref = arcpy.Describe(dataset).spatialReference
#cellSize=arcpy.GetRasterProperties_management(dataset,"CELLSIZEX")
#raster_list = raster_list[2584:25000] # test on a few

# Set local variables

arcpy.CheckOutExtension("Spatial")

gdbName = "aoh_summing/"
extension = ".tif"
#out_name = gdbName+".gdb"

tempFolder = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\scratch" 
rawFolder = r"C:\Users\andya\Downloads\AOH_forIIS\AOH_forIIS\Aves_10km"

print("Elapsed time (minutes): " + str((time.clock() - beginTime)/60))

beginTime2 = time.clock()

print ("Summing rasters - carried out in batches due to memory limitations")
arcpy.env.workspace = rawFolder

###########################################################

#############################################
arcpy.env.workspace = rawFolder
raster_list = arcpy.ListRasters()

rstlistlen = len(raster_list)

print ("number of rasters in list to processs: " + str(rstlistlen))
print ("rasters in list to processs: " + str(raster_list))

#to work properly need to ensure number of rasters in raster list is rounded up by one batch as last iteration not run otherwise
#use a rounding up function to do this


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
##rst1 = Raster(raster_list[0])
##rst2 = Raster(raster_list[1])
###outRas = rst1+rst2# 
##outRas = Con(rst1>=1,1,0)+Con(rst2>=1,1,0)#RasterCalculator(Con((rst)>=1, output_raster)
##sr = tempFolder+"/"+gdbName+"summedrst"+str("test")+extension
##outRas.save(sr)

j = 0
for j in range(len(ints)-1):
    i = 0
    rstlist0 = raster_list[ints[j]:ints[j+1]]
    rstlist1 = raster_list[ints[j]+1:ints[j+1]]
    #print ("rst list0"+str(rstlist0))
    #print ("rst list1"+str(rstlist1))
    if j==0:
        for rst in rstlist0:
            rst = Raster(rst)
            if i == 0:               
                outRas = Con(rst>=1,1,1)
                i += 1
                print ("Summed raster: " + str(rst)+" raster number:"+str(i))
            else:
                
                outRas = outRas + Con(rst>=1,1,1)
                i += 1
                print ("Summed raster: " + str(rst)+" raster number:"+str(i))
        sr = tempFolder+"/"+gdbName+"summedrst"+str(j)+extension
        outRas.save(sr)   
    else:
        for rst in rstlist0:
            rst = Raster(rst)
            if i == 0:
                outRas = Con(rst>=1,1,1)
                i += 1
                print ("Summed raster: " + str(rst)+" raster number:"+str(i))
            else:
                outRas = outRas + Con(rst>=1,1,1)
                i += 1
                print ("Summed raster: " + str(rst)+" raster number:"+str(i))
        sr = tempFolder+"/"+gdbName+"summedrst"+str(j)+extension
        outRas.save(sr)
        print ("Saving final summed raster: " + sr)
        
print("Elapsed time (minutes): " + str((time.clock() - beginTime2)/60))


beginTime3 = time.clock()

print ("Combining the summed values of each batch of rasters")
arcpy.env.workspace = tempFolder+"/"+gdbName

raster_list = arcpy.ListRasters("summedrst*","TIF")
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

srAll = tempFolder+"/"+gdbName+"allsummedrst"+extension
print ("Saving to :" + srAll)
outRas.save(srAll)


print("Elapsed time (minutes): " + str((time.clock() - beginTime3)/60))

print ("Finished processing")

print ("N.B. If equal area grid isn't used for species this has to be taken into account by some kind of area wweighted richness")

print("Total elapsed time (minutes): " + str((time.clock() - beginTime)/60))


