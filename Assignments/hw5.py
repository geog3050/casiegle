######################################################################
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
#
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
#
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
######################################################################
def hawkid():
    return(["Caleb Siegle", "casiegle"])

######################################################################
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population)
#
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems.
#
######################################################################

#REVISED ASSIGNMENT
#import arcpy
# Uses selectbyattributes functions to select the particular polygon or polygons before clip.
def calculateDensity(fcpolygon, attributeStatementSQL, geodatabase = "hw5.gdb"):

    import arcpy

    #sets workspace
    arcpy.env.workspace = geodatabase

    #enables overwrite if field name already exists
    arcpy.env.overwriteOutput = True


    #checks to make sure the fcpolygon is a polygon
    dscb = arcpy.Describe(fcpolygon)
    if dscb.shapeType != 'Polygon':
        print("fcpolygon is not a polygon type")

    #checks to see if the type of reference is geographic and gives a warning if it is
    if dscb.SpatialReference.type == 'Geographic':
        print('Warning: This is a geographic projection')

    #determines the unit of measurement
    unit = dscb.SpatialReference.linearUnitName
    print('The unit measurement is ' + unit)

    #Makes sure the input is a string
    if type(fcpolygon) != str:
        print("Error because fcpolyon needs to be a string")
    #Makes sure the input is a string
    if type(attribute) != str:
        print("Error because attribute needs to be a string")



    arcpy.AddField_management(fcpolygon, "areainsqm", "Double")

    #creates sqmeter field
    arcpy.CalculateGeometryAttributes_management(fcpolygon, [["areainsqm", "AREA"]], "MILES_US" , "SQUARE_MILES_US")

    #creates an empty density field
    arcpy.AddField_management(fcpolygon, 'density', "Double")

    #selects attributes
    fcpolygon1 = arcpy.SelectLayerByAttribute_management(fcPolygon, "NEW_SELECTION")
                                        "attributeStatementSQL")

    #calculates the density and takes the count attribute divided by the areainsqm that was calculated before
    arcpy.management.CalculateField(fcpolygon1, 'density', '!attribute! / !areainsqm!', 'PYTHON3')

######################################################################
# Problem 2 (40 Points)
#
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase,
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
#
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#
######################################################################

#I changed the inputs to the fcPolygon. Then it will output an output feature class with just the attributes of the polygon they want.
def estimateTotalLineLengthInPolygons(fcLine, fcPolygon, polygonIDFieldName, PolygonID, geodatabase = "hw5.gdb"):

    #sets workspace
    arcpy.env.workspace = geodatabase

    #enables overwrite if field name already exists
    arcpy.env.overwriteOutput = True

    #checks to make sure the fcpolygon is a polygon and finds unit of measurement
    dscbPoly = arcpy.Describe(fcPolygon)
    unit = dscbPoly.SpatialReference.linearUnitName
    print('The unit measurement for fcPolygon is ' + unit)
    if dscbPoly.shapeType != 'Polygon':
        print("fcpolygon is not a polygon type")

    #checks to make sure the fcline is a polygon and finds unit of measurement
    dscbLine = arcpy.Describe(fcLine)
    unit = dscbLine.SpatialReference.linearUnitName
    print('The unit measurement for fcLine is ' + unit)
    if dscbLine.shapeType != 'Polyline':
        print("fcLine is not a Polyline type")


    #Makes sure the input is not a string
    if type(polygonIDFieldName) == str:
        print("Error because polygonIDFieldName does not need to be string")
    #Makes sure the input is not a string
    if type(PolygonID) == str:
        print("Error because PolygonID does not need to be string")


    #Checks the projections and changes them if they are different to the projection of the fcPolygon
    if dscbLine.SpatialReference.PCSCode != dscbPoly.SpatialReference.PCSCode:
        arcpy.Project_management(fcLine, 'fcLine', dscbPoly.SpatialReference.PCSCode)

    #calculates the length of polylines in the selected polygon
    arcpy.analysis.SummarizeWithin('fcPolygon', 'fcLine', 'summ_within', '#', '#', '#', 'MILES')

    #selects the polygon by using an expression made from their inputs of the field name and the polygonID
    arcpy.analysis.Select('summ_within', 'output', 'PolygonID = "polygonIDFieldName"')



######################################################################
# Problem 3 (30 points)
#
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################

#I combined the distance and unit into one input by the user because it works better in my function and added a joinID so they can use
#the ID they want since every class is different and will have different ID's
def countObservationsWithinDistance(fcPoint, distanceAndUnit, joinID, geodatabase = "hw5.gdb"):


    #sets workspace
    arcpy.env.workspace = geodatabase

    #enables overwrite if field name already exists
    arcpy.env.overwriteOutput = True

    #creates buffer that is the distance and unit for next part (creates polygons)
    arcpy.analysis.Buffer(fcPoint, "buffer", distanceAndUnit)

    #this function counts the numbers of points in the buffers
    arcpy.analysis.SummarizeWithin("buffer", fcPoint, "summ_within")

    #Joins the count of points to the fcPoint feature class
    arcpy.JoinField_management(fcPoint, joinID, "summ_within", joinID, "Point_Count")



    #sets workspace
    arcpy.env.workspace = geodatabase

    #enables overwrite if field name already exists
    arcpy.env.overwriteOutput = True

    #determines the unit of measurement
    dscb = arcpy.Describe(fcPoint)
    unit = dscb.SpatialReference.linearUnitName
    print('The unit measurement is ' + unit)

    if dscb.shapeType != 'Point':
        print("fcPoint is not a Point type")

    #checks to see if the type of reference is geographic and gives a warning if it is
    if dscb.SpatialReference.type == 'Geographic':
        print('Warning: This is a geographic projection')

    #Makes sure the input is a string
    if type(fcPoint) != str:
        print("Error because fcPoint needs to be a string")
    #Makes sure the input is a string
    if type(distanceAndUnit) != str:
        print("Error because distanceAndUnit needs to be a string")
    #Makes sure the input is a string
    if type(joinID) != str:
        print("Error because joinID needs to be a string")

    #Creates buffer for each point using the distance and unit
    arcpy.analysis.Buffer(fcPoint, "buffer", distanceAndUnit)

    #Uses the SummarizeWithin function to get a count for each buffer created for each point
    arcpy.analysis.SummarizeWithin("buffer", fcPoint, 'summ_within')

    #Joins the summwithin table by the user input joinID (They are the same because it is the same FC)
    #created to the fcPoint feature class and only keeps the Point_Count to the orginal FC
    arcpy.JoinField_management(fcPoint, joinID, 'summ_within', joinID, "Point_Count")


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
