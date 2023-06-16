# testing on creating a point later from xy data

# import directories
import arcpy
from arcpy import env
from arcpy.sa import *
import os
from collections import defaultdict
import datetime
print("arcpy imported")

# estabslish parameters
arcpy.env.workspace = "C:\\Users\\Emma Tyrrell\\Documents\\PSU_SDS\\THESIS_230226"
temporalDataFilesWorkspace = (arcpy.env.workspace + "\\Data\\WeatherStations\\SpatialDataFiles")
terrainDataFilesWorkspace = (arcpy.env.workspace + "\\Data\\TerrainData")
arcpy.env.overwriteOutput = True
ArcGISdataWorkspace = (arcpy.env.workspace + "\\ArcGISProjects\\WeatherStationInterpolation\\Data")
XYdatafile = (arcpy.env.workspace + "\\Data\\WeatherStations\\SanJuanWeatherStationMetadataCoordsXY.csv")
dataTableMerge = (arcpy.env.workspace + "\\Data\\WeatherStations\\SanJuanWeatherStationMetadataCAICWSData01242022.csv")
demFiles = (arcpy.env.workspace + "\\Data\\DEM")
projectBoundary = (arcpy.env.workspace + "\\Data\\StaticDataGDB.gdb\\ProjectBoundary")
xField = "X_Coord"
yField = "Y_Coord"
outPointClass = (ArcGISdataWorkspace + "\\SanJuanWeatherStationsPoint.shp")
projectedOutPointClass = (ArcGISdataWorkspace + "\\SanJuanWeatherStations_projected.shp")
weatherStationDataJoin = (ArcGISdataWorkspace + "\\SanJuanWeatherStation_joinv2.shp")
windWeatherStationShapefile = (ArcGISdataWorkspace + "\\SanJuanWindSpdWeatherStations.shp")
arcpy.env.qualifiedFieldNames = False
GCSsr = arcpy.SpatialReference(4326)
PCSsr = arcpy.SpatialReference(6432)
print("parameters established")

# Prep shapefiles
try:
    # run tool for XY class
    arcpy.management.XYTableToPoint(XYdatafile, outPointClass, xField, yField, "", GCSsr)
    print("point class created")

    #project class into proper cooridnate system
    arcpy.management.Project(outPointClass, projectedOutPointClass, PCSsr)
    print("coordinate system projected")
#
#     #List fields in table
#     fieldsTable = arcpy.ListFields(dataTableMerge)
#     for field in fieldsTable:
#         print(field.name)
#
#     print("NEXT")
#
#     fieldsPointClass = arcpy.ListFields(projectedOutPointClass)
#     for field in fieldsPointClass:
#         print(field.name)
#
#     # #merge table to pointclass
#     # stationDataJoin = arcpy.management.AddJoin(projectedOutPointClass, "CAICName", dataTableMerge, "Name", "KEEP_COMMON")
#     # print("join created")
#     # arcpy.management.CopyFeatures(stationDataJoin, weatherStationDataJoin)
#     # print("join finished")

#
except Exception as ex:
    print(ex)
#
# add field for WindSPD, copy, and interpolate
try:
    fieldsTable = arcpy.ListFields(dataTableMerge)
    for datafield in fieldsTable:

        arcpy.management.AddField(projectedOutPointClass, datafield.name, "SHORT")
        print(datafield.name + " added")

    # list out fields in join table
    fieldList = arcpy.ListFields(projectedOutPointClass)
    for field in fieldList:
        print(field.name)

    #arcpy.management.CalculateField(projectedOutPointClass, "Spd", "Spd" == None, "PYTHON3")

    stationDataJoin = arcpy.management.AddJoin(projectedOutPointClass, "CAICName", dataTableMerge, "Name", "KEEP_COMMON")
    print("tables joined. don't fuck it up")

    arcpy.management.CopyFeatures(stationDataJoin, weatherStationDataJoin)
    print("join finished")

    # arcpy.CalculateField_management(weatherStationDataJoin, "Spd", "!Spd_1!", "PYTHON_9.3")
    # print("Spd copied")

#use update cursor to add Null Values
    # fc_all = [str(el.name) for el in fieldList]
    # for fc in fc_all:
    with arcpy.da.UpdateCursor(weatherStationDataJoin, "Spd") as cursor:
        for row in cursor:
            if (row[0] == 0): row[0] = None

            cursor.updateRow(row)

    print("fields -")

except Exception as ex:
    print(ex)

# select feature and make layer
# try:
#     expression = u'{} = 0'.format(arcpy.AddFieldDelimiters(weatherStationDataJoin, "Spd"))
#
#     with arcpy.SearchCursor(weatherStationDataJoin, "Spd", expression) as cursor:
#
#         for row in cursor:
#             print(row[1])
#
# except Exception as ex:
#     print(ex)

#interpolate wind speed
# try:
#     #spdQuery = "Spd IS NOT NULL"
#     #spdQuery = "{} IS NOT {}".format("[Spd]", "NULL")
#     windSpeedSelection = arcpy.management.SelectLayerByAttribute(weatherStationDataJoin, "NEW_SELECTION", "Spd != 'NULL'")
#     print("layer selected")
#
#     # arcpy.management.MakeFeatureLayer(windSpeedSelection, testWindWeatherStations)
#     # print ("layer created")
#     # arcpy.CreateFeatureDataset_management(ArcGISdataWorkspace, "windSpdStations.shp", PCSsr)
#     # print ("dataset created")
#
#     arcpy.management.CopyFeatures(windSpeedSelection, testWindWeatherStations)
#     print("features copied")
#
# except Exception as ex:
#     print(ex)
#try interpolate from wind
# outNatNeighGst = NaturalNeighbor(weatherStationDataJoin, "Spd", 10)
# outNatNeighGst.save(testWindInterpolate)
# print("interpolation completed for Spd tp")

# #try interpolation for mx temp
# outNatNeighMxT = NaturalNeighbor(weatherStationDataJoin, "MxTp", 10)
# outNatNeighMxT.save(maxTempNN01312023)
# print("interpolation completed for mx tp")
#
# #try interpolation for mn temp
# outNatNeighMnT = NaturalNeighbor(weatherStationDataJoin, "MnTp", 10)
# outNatNeighMnT.save(minTempNN01312023)
# print("interpolation completed for mn tp")
#
# #try interpolation for SWE
# outNatNeighMnT = NaturalNeighbor(weatherStationDataJoin, "SWE", 10)
# outNatNeighMnT.save(sweNN01312023)
# print("interpolation completed for SWE")



