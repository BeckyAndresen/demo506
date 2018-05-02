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


for district in district_plan:
    if district.id == "1":
        district.population = 715327
    elif district.id == "2":
        district.population = 757511
    elif district.id == "3":
        district.population = 721847
    elif district.id == "4":
        district.population = 713297
    elif district.id == "5":
        district.population = 722739
    elif district.id == "6":
        district.population = 711318
    elif district.id == "7":
        district.population = 708541
    elif district.id == "8":
        district.population = 728129

