import sys, os
import os
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import itertools

beginTime = time.clock()

# set workspace environment

myWorkspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits_raster"
outWorkspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_ALLcats_mar\summed_ALLcats_mar.gdb"
pWorkspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_ALLcats_mar"
arcpy.env.workspace = myWorkspace
folderList = arcpy.ListWorkspaces("BIRDS*")
out_gdb = "summed_ALLcats_mar.gdb"
print folderList

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

for f in folderList:
    print "f:",f
    f_name = str(os.path.basename(f))
    print "f_name:", f_name
    gdb = myWorkspace + "\\"+f_name +"\\IUCN_boolean1_0_RSR.gdb"
    print gdb
    arcpy.env.workspace = gdb
    ras_all = arcpy.ListRasters("*", "*")

    ##print "ras_cat:", ras_cat
    rscount_all = len(arcpy.ListRasters("*", "*"))
    print "rscount_all:", rscount_all
    ##print rscount_cat, "species in category", c," in ", f_name
    arcpy.env.workspace = outWorkspace
    set_list = arcpy.ListRasters(f_name+"*_set*")
    print set_list
    ##print set_list
    print "There are " + str(len(set_list)) + " sets in the list to sum: " + str(set_list)

    weight = 1
    print "weight:", weight
    #executes weighted sum for of all matchedRasters with using value field and given a weight of 1
    raster_list = ([[s,"VALUE", weight] for s in set_list])
    rstlistlen = len(raster_list)
    print "rstlistlen:", rstlistlen

    ints =range(0,rstlistlen,50)
    print "intervals: ", ints
    ints.append(rstlistlen)

    j = 0
    for j in range(len(ints)-1):
        i = 0
        rstlist0 = raster_list[ints[j]:ints[j+1]]
        ##print rstlist0
        WSumTableObj = WSTable(rstlist0)
        ##print "WSumTableObj:", WSumTableObj
        print "Processing batch ", j+1, "..........."
        print "summing species sets for geodatabase ", gdb
        outWeightedSum = WeightedSum(WSumTableObj)
        ##print outWeightedSum
        if arcpy.Exists(pWorkspace + "\\" + out_gdb):
            print "skipping GDB creation :", out_gdb
        else:
            print "creating GDB:",pWorkspace + "\\", out_gdb
            arcpy.CreateFileGDB_management(pWorkspace, out_gdb)
        outsumall =  outWorkspace + "\\" + f_name + "_W" + str(weight).replace(".","_") + "_sum"+ str(j+1)
        ##set = f_name + "_W" + str(weight).replace(".","_") + "_sum"
        ##print "set:", set
        ##print outsumcat, "Created"
        outWeightedSum.save(outsumall)
        print outsumall, "Saved"

print "Summing sets complete, now chking if more than one batch and normalising...."

for f in folderList:
    arcpy.env.workspace = outWorkspace
    sum_list = arcpy.ListRasters(f_name+"*_sum*")
    sum_list2 = ([[s,"VALUE", weight] for s in sum_list])
    sumlistlen = len(sum_list)
    print "sumlistlen:", sumlistlen
    if sumlistlen == 1:
        sum = sum_list[0]
        print"Only one batch so  renaming _sum1 to _sum_all"
        sumrename = sum.replace("_sum1","_sum_all")
        arcpy.Copy_management(outWorkspace+"\\"+sum, outWorkspace+"\\"+sumrename, data_type="RasterDataset")
        print "Only one set_sum, renamed to:", sumrename
        sum_all_Norm = outWorkspace +  "\\" + f_name + "_W" + str(weight).replace(".","_") + "_sum_all_Norm"
        print "dividing ",sumrename, "by",rscount_all
        arcpy.gp.Divide_sa(sumrename, rscount_all, sum_all_Norm)
        sum_all = outWorkspace +  "\\" + f_name + "_W" + str(weight).replace(".","_") + "_sum_all"
        print "normalizing complete for", sum_all
    else:
        WSumTableObj = WSTable(sum_list2)
        print "More than one set so summing batches..........."
        outWeightedSum = WeightedSum(WSumTableObj)
        outsumall =  outWorkspace + "\\" + f_name + "_W" + str(weight).replace(".","_") + "_sum_all"
        print "outsumall:", outsumall
        sum_all = f_name + "_W" + str(weight).replace(".","_") + "_sum_all"
        print "Saving sum:" + sum_all
        outWeightedSum.save(outsumall)
        sum_all_Norm = outWorkspace +  "\\" + f_name + "_W" + str(weight).replace(".","_") + "_sum_all_Norm"
        print "dividing ",outsumall, "by",rscount_all
        arcpy.gp.Divide_sa(outsumall, rscount_all, sum_all_Norm)
        print "normalizing complete for", sum_all



