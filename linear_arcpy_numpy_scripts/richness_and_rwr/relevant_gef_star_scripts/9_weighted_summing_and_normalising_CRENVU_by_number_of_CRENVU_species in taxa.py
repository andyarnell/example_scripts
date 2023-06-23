import sys, os
import os
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import itertools

beginTime = time.clock()

# set workspace environment
##myWorkspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits_raster"
##outWorkspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_ALLcats_mar\summed_taxon_mar.gdb"
##pWorkspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_ALLcats_mar"

myWorkspace = r"V:\GEF_STAR\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits_raster"
splitsWorkspace = r"V:\GEF_STAR\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits"
outWorkspace = r"V:\GEF_STAR\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_ALLcats_ter\summed_CRENVU_ter.gdb"
pWorkspace = r"V:\GEF_STAR\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\sums_ALLcats_ter"


arcpy.env.workspace = myWorkspace
folderList = arcpy.ListWorkspaces("*")
out_gdb = "summed_CRENVU_ter.gdb"
print folderList

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True


for f in folderList:
    f_name2 = str(os.path.basename(f))
    arcpy.env.workspace = outWorkspace
    gdb2 = myWorkspace + "\\"+f_name2 +"\\IUCN_boolean1_0_RSR.gdb"
    print gdb2
    arcpy.env.workspace = gdb2

    rscount_CR = len(arcpy.ListRasters("*_CR", "*"))
    rscount_EN = len(arcpy.ListRasters("*_EN", "*"))
    rscount_VU = len(arcpy.ListRasters("*_VU", "*"))
    print "rscount_CR: ", rscount_CR
    print "rscount_EN:", rscount_EN
    print "rscount_VU:", rscount_VU


    rscount_all2 = rscount_CR + rscount_EN + rscount_VU

    ##rscount_all2 = len(arcpy.ListRasters("*", "*"))
    print "rscount_all2:", rscount_all2

    sum_all = outWorkspace +  "\\" + f_name2 + "_threatened_sum_all"
    sum_all_Norm = outWorkspace +  "\\" + f_name2 + "_threatened_sum_all_Norm"
    print "dividing ",sum_all, "by",rscount_all2
    arcpy.env.workspace = outWorkspace
    arcpy.gp.Divide_sa(sum_all, rscount_all2, sum_all_Norm)
    print "normalizing complete for", sum_all

print "script complete"
