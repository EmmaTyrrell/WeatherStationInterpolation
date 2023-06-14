#testing on creating a point later from xy data

#import directories
import arcpy
from arcpy import env
from arcpy.sa import *
import os
from collections import defaultdict
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
weatherStationDataJoin = (ArcGISdataWorkspace + "\\SanJuanWeatherStation_join.shp")
maxTempNN01312023 = (temporalDataFilesWorkspace + "\\01312023\\SanJuanWeatherStation_MxTpIDW.tif")
minTempNN01312023 = (temporalDataFilesWorkspace + "\\01312023\\SanJuanWeatherStation_MnTpIDW.tif")
sweNN01312023 = (temporalDataFilesWorkspace + "\\01312023\\SanJuanWeatherStation_SWE.tif")
arcpy.env.qualifiedFieldNames = False
GCSsr = arcpy.SpatialReference(4326)
PCSsr = arcpy.SpatialReference(6432)
print("parameters established")

#run tool for XY class
arcpy.management.XYTableToPoint(XYdatafile, outPointClass, xField, yField, "", GCSsr)
print("point class created")

#project class into proper cooridnate system
arcpy.management.Project(outPointClass, projectedOutPointClass, PCSsr)
print("coordinate system projected")
#
#merge table to pointclass

stationDataJoin = arcpy.management.AddJoin(projectedOutPointClass, "Name", dataTableMerge, "Name", "KEEP_COMMON")
print ("join created")
arcpy.management.CopyFeatures(stationDataJoin, weatherStationDataJoin)
print("join finished")
#
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



