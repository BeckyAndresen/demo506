import sys
import os
from libdistrict.district import District
from osgeo import gdal, ogr


# the name of the folder and the name of the shapefile
shape_file = r"Wisconsin_Congressional_Districts_2011/Wisconsin_Congressional_Districts_2011.shp"

driver = ogr.GetDriverByName('ESRI Shapefile')

data_source = driver.Open(shape_file, 0)

if data_source is None:
    print ("Open failed.\n")
    sys.exit( 1 )


layer = data_source.GetLayer()
layer.ResetReading()

district_plan = []

# iterate through all of the features
# to get individual district numbers and geometries
# Congress has 8 unique districts, which are numbered 1-8
for feature in layer:

    # the number of the current district
    district_number = feature["District_N"]

    # use district_geometry for the geometry
    geom = feature.GetGeometryRef()
    district_geometry = geom.Clone()

    district_plan.append(District(id=district_number, geometry=district_geometry))


# 2010 data from: http://www.publicmapping.org/resources/state-resources/wisconsin/wisconsin-2010-census-statistics
ideal_population_size = 710873
for district in district_plan:
    if district.id == "1":
        district.population = 728042
    elif district.id == "2":
        district.population = 751169
    elif district.id == "3":
        district.population = 729957
    elif district.id == "4":
        district.population = 669015
    elif district.id == "5":
        district.population = 707580
    elif district.id == "6":
        district.population = 705102
    elif district.id == "7":
        district.population = 689279
    elif district.id == "8":
        district.population = 706840

