#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      corinnar
#
# Created:     09/06/2017
# Copyright:   (c) corinnar 2017
# Licence:     <your licence>
#------------------------------------------------------------------------

import sys, os
import os
import arcpy, arcinfo
from arcpy import env
from arcpy.sa import *

import time

beginTime = time.clock()
arcpy.env.overwriteOutput = True

p180_gdb = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits_raster180\WRASSE_Mar_id_cat_fixed_180"
porig_gdb = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits_raster\WRASSE_Mar_id_cat"


RSlist = []
arcpy.env.workspace = p180_gdb+"\\IUCN_boolean1_0_RSR.gdb"
rsts = arcpy.ListRasters("*", "ALL")
rstlen = len(rsts)
print rstlen

RSlist.append(rsts)
char_list=['u','[',']']
ch = str(char_list)

RSList2 = str(RSlist)
RSList3 = RSList2.replace("u","").replace("[","").replace("]","")
print RSList3

for rst in rsts:

    in_1_0_RSR = p180_gdb+"\\IUCN_boolean1_0_RSR.gdb\\"+rst
    out_1_0_RSR = porig_gdb+"\\IUCN_boolean1_0_RSR.gdb\\"+rst
    arcpy.Copy_management(in_1_0_RSR, out_1_0_RSR, data_type="RasterDataset")
    print rst, "copied to ", out_1_0_RSR

    in_1_0 = p180_gdb+"\\IUCN_boolean1_0.gdb\\"+rst
    out_1_0 = porig_gdb+"\\IUCN_boolean1_0.gdb\\"+rst
    arcpy.Copy_management(in_1_0, out_1_0, data_type="RasterDataset")
    print rst, "copied to ", out_1_0

    in_1_nd_RSR = p180_gdb+"\\IUCN_boolean1_nd_RSR.gdb\\"+rst
    out_1_nd_RSR = porig_gdb+"\\IUCN_boolean1_nd_RSR.gdb\\"+rst
    arcpy.Copy_management(in_1_nd_RSR, out_1_nd_RSR, data_type="RasterDataset")
    print rst, "copied to ", out_1_nd_RSR

    in_1_nd = p180_gdb+"\\IUCN_boolean1_nd.gdb\\"+rst
    out_1_nd = porig_gdb+"\\IUCN_boolean1_nd.gdb\\"+rst
    arcpy.Copy_management(in_1_nd, out_1_nd, data_type="RasterDataset")
    print rst, "copied to ", out_1_nd

print ("Total elapsed time (seconds): " + str((time.clock() - beginTime)/60), " minutes")
print "Script finished"

