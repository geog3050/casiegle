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
# Problem 1 (20 points)
#
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#
######################################################################
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):




    dscb = arcpy.Describe(fcPolyline)
    if dscb.shapeType != 'Polyline':
        print("fcPolygon is not a polyline type")

    dscb = arcpy.Describe(fcPoint)
    if dscb.shapeType != 'Point':
        print("fcPoint is not a point type")

    if type(input_geodatabase) != str:
        print("Error because input_deodatabase path needs to be a string")
    
        
    #Sets the workspace to where the data is.
    arcpy.env.workspace = input_geodatabase
    
    #This takes the polyline(bike routes) and then finds the closest points and appends the ID and the distance to the polyline table
    arcpy.Near_analysis(fcPolyline, fcPoint)

    

######################################################################
# Problem 2 (30 points)
#
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in tagghe polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):


    dscb = arcpy.Describe(fcPolygon)
    if dscb.shapeType != 'Polygon':
        print("fcPolygon is not a polygon type")

    dscb = arcpy.Describe(fcPoint)
    if dscb.shapeType != 'Point':
        print("fcPoint is not a point type")

    if type(input_geodatabase) != str:
        print("Error because input_deodatabase path needs to be a string")

    if type(pointFieldName) != str:
        print("Error because pointFieldName needs to be a string")

    if type(pointFieldValue) != str:
        print("Error because pointFieldValue needs to be a string")

    #Sets the workspace to where the data is.
    arcpy.env.workspace = input_geodatabase

    #gets the points in the polygons and groups them by the pointFieldName
    arcpy.analysis.SummarizeWithin(fcPolygon, fcPoint, 'summ_within', '#', '#', '#', '#',
                              pointFieldName, '#', '#', 'group_table')

    #Pivots the table created from SummarizeWithin so it can be joined with the specified type from the user and creates a new table
    arcpy.PivotTable_management('group_table', 'Join_ID', pointFieldName, 'Point_Count', 'pivot')
    
    #Joins the new pivot table to the fcPolygon class with the field specified by the pointFieldValue input
    arcpy.JoinField_management(fcPolygon, 'OBJECTID', 'pivot', 'Join_ID', pointFieldValue)
    

    
######################################################################
# Problem 3 (50 points)
#
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.


######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):

#TESTER
    dscb = arcpy.Describe(fcPolygon)
    if dscb.shapeType != 'Polygon':
        print("fcPolygon is not a polygon type")

    dscb = arcpy.Describe(fcPoint)
    if dscb.shapeType != 'Point':
        print("fcPoint is not a point type")

    if type(workspace) != str:
        print("Error because workspace needs to be a string")

    if type(pointFieldName) != str:
        print("Error because pointFieldName needs to be a string")
    

    
    #Sets the workspace to where the data is.
    arcpy.env.workspace = workspace

    
    #gets the points in the polygons and groups them by the pointFieldName
    arcpy.analysis.SummarizeWithin(fcPolygon, fcPoint, 'summ_within', '#', '#', '#', '#',
                              pointFieldName, '#', '#', 'group_table')

    #Pivots the table created from SummarizeWithin so it can be joined with the specified type from the user and creates a new table
    arcpy.PivotTable_management('group_table', 'Join_ID', pointFieldName, 'Point_Count', 'pivot')

    #Joins the table with the fcPolygon table and has a field for each field value in the field name given by the user
    arcpy.JoinField_management('fcPolygon', 'OBJECTID', 'pivot', 'Join_ID')
    
#When i tested my code, it worked without changing the names below 13 characters. 


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
