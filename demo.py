import sys
import os
import statistics
from libdistrict.district import District
from libdistrict.compactness import polsby_popper, schwartzberg, convex_hull_ratio
from libdistrict.equal_population import districts_in_range, districts_in_percent_deviation
from libdistrict.partisan_symmetry import efficiency_gap, mean_median_diff, competitiveness
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


# 2010 population data from: http://www.publicmapping.org/resources/state-resources/wisconsin/wisconsin-2010-census-statistics
# 2016 dem/rep votes for president from: https://data-ltsb.opendata.arcgis.com/datasets/01869b4b585e44bbbac5d550b7bb6fb8_0
ideal_population_size = 710873
for district in district_plan:
    party_votes = []
    if district.id == "1":
        district.population = 728042
        district.party_votes={'dem':150448, 'rep':187380}
    elif district.id == "2":
        district.population = 751169
        district.party_votes = {'dem':271505, 'rep':119606}
    elif district.id == "3":
        district.population = 729957
        district.party_votes = {'dem':161002, 'rep':177179}
    elif district.id == "4":
        district.population = 669015
        district.party_votes = {'dem':228229, 'rep':67290}
    elif district.id == "5":
        district.population = 707580
        district.party_votes = {'dem':148886, 'rep':229313}
    elif district.id == "6":
        district.population = 705102
        district.party_votes = {'dem':141918, 'rep':203436}
    elif district.id == "7":
        district.population = 689279
        district.party_votes = {'dem':137870, 'rep':213459}
    elif district.id == "8":
        district.population = 706840
        district.party_votes = {'dem':142678, 'rep':207621}


"""
Demonstrating libdistrict functions starts here
"""
print("\nCalculating Scores for 2011 Congressional District Plan")

print("\n\t----COMPACTNESS----\n")

"""
Convex Hull Ratio for each district and the district plan average
"""
convex_hull_scores = []
for district in district_plan:
    score = convex_hull_ratio(district)
    convex_hull_scores.append(score)
    print("District: {}\tConvex Hull Ratio: {}".format(district.id, score))

print("Average Convex Hull Ratio: {}".format(statistics.mean(convex_hull_scores)))


"""
Schwartzberg for each district and the district plan average
"""
print("\n\n")
schwartzberg_scores = []
for district in district_plan:
    score = schwartzberg(district)
    schwartzberg_scores.append(score)
    print("District: {}\tSchwartzberg: {}".format(district.id, score))

print("Average Schwartzberg: {}".format(statistics.mean(schwartzberg_scores)))


"""
Polsby_Popper for each district and the district plan average
"""
print("\n\n")
polsby_popper_scores = []
for district in district_plan:
    score = polsby_popper(district)
    polsby_popper_scores.append(score)
    print("District: {}\tPolsby-Popper: {}".format(district.id, score))

print("Average Polsby-Popper: {}".format(statistics.mean(polsby_popper_scores)))


"""
Equal population for the district plan
"""
print("\n\n\t----EQUAL POPULATION 2010 CENSUS DATA----\n")
print("Districts in 10% deviation: {}".format(districts_in_percent_deviation(district_plan, 10)))
print("Districts in 5% deviation: {}".format(districts_in_percent_deviation(district_plan, 5)))
print("Districts in 1% deviation: {}".format(districts_in_percent_deviation(district_plan, 1)))

variation_1 = 41858
min_target_1 = ideal_population_size - variation_1
max_target_1 =  ideal_population_size + variation_1
range_1 = districts_in_range(district_plan, min_target_1, max_target_1)
print("{} districts in range {} to {}".format(range_1, min_target_1, max_target_1))

variation_2 = 20000
min_target_2 = ideal_population_size - variation_2
max_target_2 =  ideal_population_size + variation_2
range_2 = districts_in_range(district_plan, min_target_2, max_target_2)
print("{} districts in range {} to {}".format(range_2, min_target_2, max_target_2))


print("\n\n\t----PARTISAN SYMMETRY 2016 PRESIDENTIAL ELECTION DATA---\n")
print("Efficiency Gap: {}".format(efficiency_gap(district_plan, 'dem', 'rep')))
print("Mean-Median Difference Democrats: {}".format(mean_median_diff(district_plan, 'dem', 'rep')))
print("Mean-Median Difference Republicans: {}".format(mean_median_diff(district_plan, 'rep', 'dem')))