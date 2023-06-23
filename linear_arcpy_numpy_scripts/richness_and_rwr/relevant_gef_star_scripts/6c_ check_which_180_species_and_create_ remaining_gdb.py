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

##splits_workspace = arcpy.GetParameterAsText(0)
##folder_name = arcpy.GetParameterAsText(1)

##check_workspace = arcpy.GetParameterAsText(0)
##orig_gdb = arcpy.GetParameterAsText(1)
##new_gdb = arcpy.GetParameterAsText(2)


check_workspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits\BIRDS_Mar_id_cat_fixed_180.gdb"
orig_gdb = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits\BIRDS_Mar_id_cat.gdb"
new_gdb = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits\BIRDS_Mar_id_cat_remaining_for_180.gdb"

FClist = []
arcpy.env.workspace = check_workspace
fcs = arcpy.ListFeatureClasses("*", "polygon")
FClist.append(fcs)
char_list=['u','[',']']
ch = str(char_list)

FCList2 = str(FClist)
FCList3 = FCList2.replace("u","").replace("[","").replace("]","")

arcpy.Copy_management(orig_gdb, new_gdb, data_type="Workspace")
arcpy.env.workspace = orig_gdb
origFCs = arcpy.ListFeatureClasses("*", "polygon")
for fc in origFCs:
    for f in fcs:
        if f == fc:
            in_data = new_gdb + "\\" + f
            arcpy.Delete_management(in_data, data_type="FeatureClass")
            print f, "already created, deleted "
        else:
            pass

print ("Total elapsed time (seconds): " + str((time.clock() - beginTime)/60), " minutes")
print "Script finished"

