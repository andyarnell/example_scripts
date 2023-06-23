##aim: 
##created by Andy Arnell 29/06/2015

print "Importing packages"

import os
import arcpy
from arcpy import env
from arcpy.sa import *
import glob
import string
import math
import time

print "Setting local parameters and inputs"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True

beginTime = time.clock()



#Set environment settings


snapgrid = "C:/Data/geo6/raw/grids/snapgrid_dd" # provide a default value if unspecified
sg=Raster(snapgrid)

arcpy.env.extent= sg.extent
print "Extent: " + str(arcpy.env.extent)
arcpy.env.snapRaster=sg
print "Snap raster: "+str(arcpy.env.snapRaster)


#raster_list = arcpy.ListRasters()
#dataset = raster_list[0]
#spatial_ref = arcpy.Describe(dataset).spatialReference
#cellSize=arcpy.GetRasterProperties_management(dataset,"CELLSIZEX")
#raster_list = raster_list[2584:25000] # test on a few

# Set local variables

arcpy.CheckOutExtension("Spatial")

gdbName = "IUCN_range_raritytest"

out_name = gdbName+".gdb"


tempFolder = "C:/Data/geo6/scratch" 

rawFolder = "C:/Data/geo6/scratch/"+out_name


print("Elapsed time (minutes): " + str((time.clock() - beginTime)/60))


beginTime2 = time.clock()

print "Summing rasters - carried out in batches due to memory limitations"
arcpy.env.workspace = rawFolder

###########################################################

#############################################
arcpy.env.workspace = rawFolder
raster_list = arcpy.ListRasters()
raster_list = new_raster_list
rstlistlen = len(raster_list)


print "number of rasters in list to processs: " + str(rstlistlen)

#to work properly need to ensure number of rasters in raster list is rounded up by one batch as last iteration not run otherwise
#use a rounding up function to do this

batchsize=1000

def roundup(x,y):
    return int(math.ceil(x / float(y))) * y

roundUpVal=roundup(rstlistlen,batchsize)
print roundUpVal

#use range function to create list of batch intervals to iterate through
ints =range(0,roundUpVal,batchsize)
#add extra value to end of list
ints.append(roundUpVal)

print ints


j = 0
for j in range(len(ints)-1):
    i = 0
    rstlist0 = raster_list[ints[j]:ints[j+1]]
    rstlist1 = raster_list[ints[j]+1:ints[j+1]]
    #print rstlist0
    print rstlist1
    if j==0:
        for rst in rstlist0:
            if i == 0:
                OutRaster = Con(IsNull(rst),0,rst)
                i += 1
                print "Summed raster: " + str(rst)+" raster number:"+str(i)
            else:
                OutRaster = OutRaster + Con(IsNull(rst),0,rst)
                i += 1
                print "Summed raster: " + str(rst)+" raster number:"+str(i)
        sr = tempFolder+"/"+gdbName+"summedrst"+str(j)+".tif"
        OutRaster.save(sr)   
    else:
        for rst in rstlist1:
            if i == 0:
                OutRaster = Con(IsNull(rst),0,rst)
                i += 1
                print "Summed raster: " + str(rst)+" raster number:"+str(i)
            else:
                OutRaster = OutRaster + Con(IsNull(rst),0,rst)
                i += 1
                print "Summed raster: " + str(rst)+" raster number:"+str(i)
        sr = tempFolder+"/"+gdbName+"summedrst"+str(j)+".tif"
        OutRaster.save(sr)
        print "Saving final summed raster: " + sr


print("Elapsed time (minutes): " + str((time.clock() - beginTime2)/60))


beginTime3 = time.clock()

print "Combining the summed values of each batch of rasters"
arcpy.env.workspace = tempFolder

raster_list = arcpy.ListRasters(gdbName+"summedrst*","TIF")
print "There are " + str(len(raster_list)) + "batches in list :" + str(raster_list)

i=0
for rst in raster_list:
            if i == 0:
                OutRaster = Raster(rst)
                i += 1
                print gdbName+"Summed raster: " + str(rst)+" raster number:"+str(i)
            else:
                OutRaster = OutRaster + rst
                i += 1
                print gdbName+"Summed raster: " + str(rst)+" raster number:"+str(i)

srAll = tempFolder+"/"+gdbName+"allsummedrst.tif"
print "Saving to :" + srAll
OutRaster.save(srAll)


print("Elapsed time (minutes): " + str((time.clock() - beginTime3)/60))

print "Finished processing"

print "N.B. If equal area grid isn't used for species this has to be taken into account by some kind of area wweighted richness"

print("Total elapsed time (minutes): " + str((time.clock() - beginTime)/60))


