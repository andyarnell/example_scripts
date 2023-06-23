import sys, os
import os
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import itertools

beginTime = time.clock()

# set workspace environment
myWorkspace=r"V:\GEF_STAR\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits_raster"
outWorkspace = r"V:\GEF_STAR\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_represented"
out_gdb = "summed_taxon_ter.gdb"
catlist = ['LC','DD','NT','EX','RE','LR_cd','LR_nt','LR_lc','NA','VU','EN','CR']
weightlist = ['1','1','1','1','1','1','1','1','1','1','1','1']
arcpy.env.workspace = myWorkspace
folderList = arcpy.ListWorkspaces("*Birds_Ter_id_cat")



# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True




for f in folderList:
    #print "f:",f
    for c,w in itertools.izip(catlist,weightlist):
        print "c:",c
        print "w:",w
        f_name = str(os.path.basename(f)).replace("_id_cat", "_"+c)
        arcpy.env.workspace = f
        ##print "f_name:", f_name
        gdbList = arcpy.ListWorkspaces("IUCN_boolean1_0_RSR.gdb", "FileGDB")
        for gdb in gdbList:
            ##print "gdb:", gdb
            arcpy.env.workspace = gdb
            ras_cat = arcpy.ListRasters("*_"+c, "*")

            ##print "ras_cat:", ras_cat
            rscount_cat = len(arcpy.ListRasters("*_"+c, "*"))
            print "rscount_cat:", rscount_cat
            ##print rscount_cat, "species in category", c," in ", f_name
            if rscount_cat > 0:
                weight = float(w)
                ##print "weight:", weight
                #executes weighted sum for of all matchedRasters with using value field and given a weight of 1
                raster_list = ([[c,"VALUE", weight] for c in ras_cat])
                ##print raster_list
                rstlistlen = len(raster_list)

                ints =range(0,rstlistlen,150)
                print "intervals: ", ints
                ints.append(rstlistlen)

                j = 0
                for j in range(len(ints)-1):
                    i = 0
                    rstlist0 = raster_list[ints[j]:ints[j+1]]
                    ##print rstlist0
                    WSumTableObj = WSTable(rstlist0)
                    ##print "WSumTableObj:", WSumTableObj
                    print "Processing set ", j+1, "..........."
                    print "summing species with category", c," using weight = ", weight, ", for geodatabase ", gdb
                    outWeightedSum = WeightedSum(WSumTableObj)
                    ##print outWeightedSum
                    if arcpy.Exists(outWorkspace + "\\" + out_gdb):
                        print "skipping GDB creation :",  out_gdb
                    else:
                        print "creating GDB:",outWorkspace + "\\", out_gdb
                        arcpy.CreateFileGDB_management(outWorkspace, out_gdb)
                        outsumcat =  outWorkspace + "\\" + out_gdb + "\\" + f_name + "_W" + str(weight).replace(".","_")
                    outsumcat =  outWorkspace + "\\" + out_gdb + "\\" + f_name + "_W" + str(weight).replace(".","_") + "_set"+ str(j+1)
                    set = f_name + "_W" + str(weight).replace(".","_") + "_set"
                    ##print "set:", set
                    ##print outsumcat, "Created"
                    outWeightedSum.save(outsumcat)
                    print outsumcat, "Saved"

                arcpy.env.workspace =outWorkspace + "\\" + out_gdb
                set_list = arcpy.ListRasters(set+"*","")
                if len(set_list) > 1 :
                    print "Combining the summed values of each batch of rasters"
                    arcpy.env.workspace =outWorkspace + "\\" + out_gdb
                    set_list = arcpy.ListRasters(set+"*","")
                    ##print set_list
                    print "There are " + str(len(set_list)) + " batches in the list to sum: " + str(set_list)

                    i=0
                    for s in set_list:
                                if i == 0:
                                    OutRaster = Raster(s)
                                    i += 1
                                    print "Summed raster: " + str(s)+" raster number:"+str(i)
                                else:
                                    OutRaster = OutRaster + s
                                    i += 1
                                    print "Summed raster: " + str(s)+" raster number:"+str(i)

                    set_all = outWorkspace + "\\" + out_gdb + "\\" + f_name + "_W" + str(weight).replace(".","_") + "_set_all"
                    print "Saving to :" + set_all
                    OutRaster.save(set_all)

                else:
                    arcpy.env.workspace =outWorkspace + "\\" + out_gdb
                    set_all =  f_name + "_W" + str(weight).replace(".","_") + "_set_all"
                    arcpy.Rename_management(outsumcat, set_all)



