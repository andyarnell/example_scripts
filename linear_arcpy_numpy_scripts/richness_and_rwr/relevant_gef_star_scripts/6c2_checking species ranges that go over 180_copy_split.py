import sys, os
import os
import arcpy
from arcpy import env
import time
##
beginTime = time.clock()

# set workspace environment
myWorkspace=r"G:\p07698_GEF_Star\IUCN_170609\rlspecies_080617_processing\splits"
clipper = r"G:\p07698_GEF_Star\GEF_Star_toolbox\deg10_wgs84.shp"
##myWorkspace=r"G:\p07698_GEF_Star\tmpsum"
arcpy.env.workspace = myWorkspace

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

arcpy.env.workspace = myWorkspace
gdbList = arcpy.ListWorkspaces("*.gdb", "FileGDB")

#Loop over the feature classes and check if range goes over 180.

for gdb in gdbList:
    arcpy.env.workspace = gdb #--change working directory to each GDB in list
    WSpace=arcpy.env.workspace
    fcs = arcpy.ListFeatureClasses()
    gdb_180 = str(os.path.basename(gdb)).replace(".gdb", "_fixed_180.gdb")
    gdbW_180 = myWorkspace + "\\" + gdb_180
    print "processing", gdb, ".............."
    fclistlen = len(fcs)

    ints =range(0,fclistlen,100)
    print "intervals: ", ints
    ints.append(fclistlen)

    j = 0
    for j in range(len(ints)-1):
        i = 0
        print j
        fclist0 = fcs[ints[j]:ints[j+1]]
        for fc in fclist0:
            desc = arcpy.Describe(fc)
            xmin = desc.extent.XMin
            xmax = desc.extent.XMax
            ymin = desc.extent.YMin
            ymax = desc.extent.YMax

            if xmin < -180 or xmax > 180:
                ##print gdb, fc, ":",xmin, xmax, ymin, ymax
                if arcpy.Exists(gdbW_180):
                    ##print "skipping GDB creation :",  gdb_180
                    in_featureclass = gdb + "\\" + fc
                    out_feature_class = myWorkspace+ "\\" + gdb_180 + "\\" + fc
                else:
                     arcpy.CreateFileGDB_management(myWorkspace, gdb_180)
                     ##print "creating file GDB : ", gdb_180
                     in_featureclass = gdb + "\\" + fc
                     out_feature_class = myWorkspace+ "\\" + gdb_180 + "\\" + fc


                try:
                    print "Clipping and densifying", in_featureclass
                    ##print "Clipping", in_featureclass
                    ##arcpy.RepairGeometry_management(in_featureclass, delete_null=DELETE_NULL)
                    arcpy.Clip_analysis(in_featureclass, clipper, out_feature_class, cluster_tolerance="")
                    arcpy.Densify_edit(out_feature_class, densification_method="DISTANCE", distance="0.1 DecimalDegrees", max_deviation="0.0000009 DecimalDegrees", max_angle="10")
                    ##print out_feature_class, "created (clipped and densified)"
                except:
                    try:
                        "clipping failed - trying mulipart to singlepart first"
                        out_feature_class_sp = myWorkspace+ "\\" + gdb_180 + "\\" + fc
                        arcpy.MultipartToSinglepart_management(in_featureclass, out_feature_class_sp)
                        print "Now trying clipping and densifying again", in_featureclass
                        arcpy.Clip_analysis(out_feature_class_sp, clipper, out_feature_class, cluster_tolerance="")
                        arcpy.Densify_edit(out_feature_class, densification_method="DISTANCE", distance="0.1 DecimalDegrees", max_deviation="0.0000009 DecimalDegrees", max_angle="10")
                    except:
                        print in_featureclass, "still failed to clip and densify"
                        ##Note from CR 24/07/17. I need to add in this identity to the script as tyhis is how I manually fixed the ones that still failed:
                        ###arcpy.Intersect_analysis(in_features="T190464_0_LC #;G:/p07698_GEF_Star/GEF_Star_toolbox/deg10_wgs84.shp #", out_feature_class="C:/Users/corinnar/Documents/ArcGIS/Default.gdb/T190464_0_LC_Intersect", join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")
            else:
                pass
                ##print fc, "extent ok"

print "Script finished"





