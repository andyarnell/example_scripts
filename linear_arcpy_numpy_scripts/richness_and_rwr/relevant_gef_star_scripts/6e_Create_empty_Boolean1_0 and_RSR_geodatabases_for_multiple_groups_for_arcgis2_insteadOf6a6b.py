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

splits_workspace = arcpy.GetParameterAsText(0)
p_workspace = arcpy.GetParameterAsText(1)


##splits_workspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits"
##p_workspace = r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing"

splits_raster = "splits_raster"
new_workspace = p_workspace + "\\"+ splits_raster
filegdb_boolean_1_0 = "IUCN_boolean1_0"
filegdb_boolean_RSR_1_0 = "IUCN_boolean1_0_RSR"
filegdb_boolean = "IUCN_boolean1_nd"
filegdb_boolean_RSR = "IUCN_boolean1_nd_RSR"

arcpy.env.workspace = p_workspace
try:
    os.makedirs(new_workspace)
except OSError:
    pass
    "print test"

arcpy.env.workspace = splits_workspace

arcpy.env.overwriteOutput = True

gdbs = arcpy.ListWorkspaces("*", "FileGDB")
for gdb in gdbs: # CR 25/5/17: Loop over the splits gdbs
        arcpy.env.workspace = new_workspace
        wstr = str(splits_workspace)
        gdbname2 = str(gdb).replace(wstr,"").replace(".gdb","").replace("\\","")
        print gdbname2
        splits_raster_w =new_workspace + "\\"+ gdbname2
        try:
            os.makedirs(splits_raster_w)
            print splits_raster_w

        except OSError:
            pass
            print splits_raster_w, " folder exists"
        arcpy.env.workspace = splits_raster_w

        # Execute CreateFileGDB
        arcpy.CreateFileGDB_management(splits_raster_w, filegdb_boolean)
        arcpy.CreateFileGDB_management(splits_raster_w, filegdb_boolean_RSR)
        arcpy.CreateFileGDB_management(splits_raster_w, filegdb_boolean)
        arcpy.CreateFileGDB_management(splits_raster_w, filegdb_boolean_RSR)
        print filegdb_boolean, " created"
        print filegdb_boolean_RSR, " created"
        print filegdb_boolean, " created"
        print filegdb_boolean_RSR, " created"

print ("Total elapsed time (seconds): " + str((time.clock() - beginTime)/60), " minutes")
print "Script finished"

