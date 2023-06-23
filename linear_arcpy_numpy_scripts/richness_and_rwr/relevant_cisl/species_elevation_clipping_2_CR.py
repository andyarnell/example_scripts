#-------------------------------------------------------------------------------
# Name:        module2_new
# Purpose:
#
# Author:      alisonberesford
#
# Created:     10/05/2016
# Copyright:   (c) alisonberesford 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import system modules and check out licences
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

# Set global variables and environment settings
arcpy.env.workspace = "C:\\GFW"
arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "100%"
dem = "C:\\GFW\\dem"
arcpy.env.snapRaster = dem

# Enter name of country to process
#country_name = "Peru"


import time
import datetime
now = datetime.datetime.now()
print now.strftime("%Y-%m-%d %H:%M")
beginTime = time.clock()

### BIRDS #
##
### Set local variables #
##
##taxa_name = "birds"
##input = "D:\\GFW\\species_ranges.gdb\\forest_" + str(taxa_name) + "_" + str(country_name)
##country = "D:\\GFW\\country_boundaries.gdb\\" + str(country_name)
##arcpy.env.extent = country
##
### Process: create weighted ESH rasters #
##
### For each species range in turn, select only areas within the species' altitude range,
### assign the output raster a value of the weighting score x 1,000,000
### convert the raster to type 32-bit signed integer
### clip to species range and country boundary and save as a .tif file.
##
##with arcpy.da.SearchCursor(input, ["conc", "altmin", "altmax", "weighting", "SHAPE@"]) as cur:
##    for row in cur:
##        outconc = row[0]
##        speciesfield = "conc"
##        defwhereclause =  speciesfield + " = '" + outconc + "'"
##        arcpy.MakeFeatureLayer_management(input, "eoo_" + str(outconc), defwhereclause)
##        selection = "eoo_" + str(outconc)
##        outCon1 = Con(Raster(dem) > row[1], 1,)
##        outCon2 = Con(Raster(dem) < row[2], 1,)
##        outCon3 = Con(((outCon1 == 1) & (outCon2 ==1)), row[3],)
##        outTimes = Times(outCon3, 1000000)
##        outInt = Int(outTimes)
##        arcpy.Clip_management(outInt,"#", "D:\\GFW\\Rasters\\temp_" + str(outconc) + ".tif", selection, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##        arcpy.Clip_management("D:\\GFW\\Rasters\\temp_" + str(outconc) + ".tif","#", "D:\\GFW\\Rasters\\" + str(country_name) + "_" + str(taxa_name) + "_" + str(outconc) + ".tif", country, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##        print(str(country_name) + "_" + str(taxa_name) + "_" + str(outconc) + " ESH created")
##print(str(country_name) + "_" + str(taxa_name) + " ESHs complete")
##
### Process: sum weighted rasters for all species in taxa #
##
### Create list of ESH rasters #
##
##arcpy.env.workspace = "D:\\GFW\\Rasters"
##rasterlist = arcpy.ListRasters("" + country_name + "_" + taxa_name + "_*", "TIF")
##
### Loop through list of ESH rasters, change nodata values to zero, add each raster to sum of all preceeding rasters in list, then convert zeros back to nodata # #
##
##i = 0
##for raster in rasterlist:
##    outCon = Con(IsNull(Raster(raster)), 0, Raster(raster))
##    if i == 0:
##        outRas = outCon
##        i += 1
##        print(str(raster + " added"))
##    else:
##        outRas += outCon
##        i += 1
##        print(str(raster + " added"))
##outSetNull = SetNull(outRas, outRas, "VALUE < 1")
##outSetNull.save("D:\\GFW\\weighted_sums\\sum_" + "" + country_name + "_" + taxa_name + ".tif")
##print("sum_" + str(country_name) + "_" + str(taxa_name) + " created")


# MAMMALS #

# Set local variables #

taxa_name = "mammals"

##input = "D:\\GFW\\species_ranges.gdb\\forest_" + str(taxa_name) + "_" + str(country_name) + "2"
##country = "D:\\GFW\\country_boundaries.gdb\\" + str(country_name)
input = "C:\\GFW\\Mammal_filtered_generalised.gdb\\Mammal_filtered_generalised"

arcpy.env.extent = arcpy.Extent(-180.0, -90, 180, 90.0)


# Process: create weighted ESH rasters #

# For each species range in turn, select only areas within the species' altitude range,
# assign the output raster a value of the weighting score x 1,000,000
# convert the raster to type 32-bit signed integer
# clip to species range and country boundary and save as a .tif file.

with arcpy.da.SearchCursor(input, ["id_seas", "min_alt", "max_alt", "sum_remaining", "SHAPE@"]) as cur:
    for row in cur:
        rowTime = time.clock()
        outconc = row[0]
        speciesfield = "id_seas"
        defwhereclause =  speciesfield + " = '" + outconc + "'"
        arcpy.MakeFeatureLayer_management(input, "eoo_" + str(outconc), defwhereclause)
        selection = "eoo_" + str(outconc)
        outCon1 = Con(Raster(dem) > row[1], 1,)
        outCon2 = Con(Raster(dem) < row[2], 1,)
        outCon3 = Con(((outCon1 == 1) & (outCon2 ==1)), row[3],)
        outTimes = Times(outCon3, 1000000)
        outInt = Int(outTimes)
        arcpy.Clip_management(outInt,"#", "C:\\GFW\\Mammals_Rasters\\"+ str(outconc) + ".tif", selection, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        ##arcpy.Clip_management("D:\\GFW\\Rasters\\temp_" + str(outconc) + ".tif","#", "D:\\GFW\\Rasters\\" + str(country_name) + "_" + str(taxa_name) + "_2000_" + str(outconc) + ".tif", country, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        print(str(taxa_name) + ": " + str(outconc) + " ESH created")
        now = datetime.datetime.now()
        print str(now)
        print ("Total elapsed time for species (seconds): " + str((time.clock() - rowTime)/60), " minutes")
        print ("Total elapsed time so far (seconds): " + str((time.clock() - beginTime)/60), " minutes")
print(str(taxa_name) + " ESHs complete")
print ("Total elapsed time for section (seconds): " + str((time.clock() - beginTime)/60), " minutes")

# Process: sum weighted rasters for all species in taxa #

# Create list of ESH rasters #

arcpy.env.workspace = "C:\\GFW\\Mammals_Rasters"
rasterlist = arcpy.ListRasters("*", "TIF")

# Loop through list of ESH rasters, change nodata values to zero, add each raster to sum of all preceeding rasters in list, then convert zeros back to nodata #

i = 0
for raster in rasterlist:
    outCon = Con(IsNull(Raster(raster)), 0, Raster(raster))
    if i == 0:
        outRas = outCon
        i += 1
        print(str(raster + " added"))
    else:
        outRas += outCon
        i += 1
        print(str(raster + " added"))
outSetNull = SetNull(outRas, outRas, "VALUE < 1")
outSetNull.save("C:\\GFW\\weighted_sums\\sum_2000" + "_" + taxa_name + ".tif")
print("sum_" + "_" + str(taxa_name) + " created")


### AMPHIBIANS #
##
### Set local variables #
##
##taxa_name = "amphibians"
##input = "D:\\GFW\\species_ranges.gdb\\forest_" + str(taxa_name) + "_" + str(country_name)
##country = "D:\\GFW\\country_boundaries.gdb\\" + str(country_name)
##arcpy.env.extent = country
##
### Process: create weighted ESH rasters #
##
### For each species range in turn, select only areas within the species' altitude range,
### assign the output raster a value of the weighting score x 1,000,000
### convert the raster to type 32-bit signed integer
### clip to species range and country boundary and save as a .tif file.
##
##with arcpy.da.SearchCursor(input, ["id_seas", "weighting", "SHAPE@"]) as cur:
##    for row in cur:
##        outconc = row[0]
##        speciesfield = "id_seas"
##        defwhereclause =  speciesfield + " = '" + outconc + "'"
##        arcpy.MakeFeatureLayer_management(input, "eoo_" + str(outconc), defwhereclause)
##        selection = "eoo_" + str(outconc)
##        outCon = Con(Raster(dem) >= 0, row[1],)
##        outTimes = Times(outCon, 1000000)
##        outInt = Int(outTimes)
##        arcpy.Clip_management(outInt,"#", "D:\\GFW\\Rasters\\temp_" + str(outconc) + ".tif", selection, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##        arcpy.Clip_management("D:\\GFW\\Rasters\\temp_" + str(outconc) + ".tif","#", "D:\\GFW\\Rasters\\" + str(country_name) + "_" + str(taxa_name) + "_" + str(outconc) + ".tif", country, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##        print(str(country_name) + "_" + str(taxa_name) + "_" + str(outconc) + " ESH created")
##print(str(country_name) + "_" + str(taxa_name) + " ESHs complete")
##
### Process: sum weighted rasters for all species in taxa #
##
### Create list of ESH rasters #
##
##arcpy.env.workspace = "D:\\GFW\\Rasters"
##rasterlist = arcpy.ListRasters("" + country_name + "_" + taxa_name + "_*", "TIF")
##
### Loop through list of ESH rasters, change nodata values to zero, add each raster to sum of all preceeding rasters in list, then convert zeros back to nodata #
##
##i = 0
##for raster in rasterlist:
##    outCon = Con(IsNull(Raster(raster)), 0, Raster(raster))
##    if i == 0:
##        outRas = outCon
##        i += 1
##        print(str(raster + " added"))
##    else:
##        outRas += outCon
##        i += 1
##        print(str(raster + " added"))
##outSetNull = SetNull(outRas, outRas, "VALUE < 1")
##outSetNull.save("D:\\GFW\\weighted_sums\\sum_" + "" + country_name + "_" + taxa_name + ".tif")
##print("sum_" + str(country_name) + "_" + str(taxa_name) + " created")


### Process: sum the weighting outputs across taxa #
##
##outCellStatistics = CellStatistics(["D:\\GFW\\weighted_sums\\sum_2000" + "" + country_name + "_birds.tif", "D:\\GFW\\weighted_sums\\sum_2000" + "" + country_name + "_mammals.tif", "D:\\GFW\\weighted_sums\\sum_2000" + "" + country_name + "_amphibians.tif"], "SUM", "DATA")
##outCellStatistics.save("D:\\GFW\\weighted_sums\\sum_2000" + "" + country_name + "_all_taxa.tif")
##print("sum_" + str(country_name) + "_all_taxa created")
##
##print(str(country_name) + " all taxa completed successfully")


### Reproject all summed rasters to World Mercator #
##
##arcpy.env.workspace = "D:\\GFW\\weighted_sums"
##sum_list = arcpy.ListRasters("sum_*", "TIF")
##for weighted_raster in sum_list:
##    out_raster = "projected_" + str(weighted_raster)
###    arcpy.ProjectRaster_management(weighted_raster, out_raster, "PROJCS['World_Behrmann',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Behrmann'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]", "BILINEAR", "999.984945754986 999.984945754986")
##    arcpy.ProjectRaster_management(weighted_raster, out_raster, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.017453292519943295]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "BILINEAR", "999.984945754986 999.984945754986")
##print("reprojections complete")
print ("Total elapsed time (seconds): " + str((time.clock() - beginTime)/60), " minutes")
print "Script complete: ", now.strftime("%Y-%m-%d %H:%M")
