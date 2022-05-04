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

#####################################################################################################
# 100 Points Total
#
# Given a linear shapefile (roads) and a point shapefile representing facilities(schools),
# this function should generate either a time-based (1-,2-,3- minute) or road network distance-based (200-, 400-, 600-, .. -2000 meters)
# concentric service areas around facilities and save the results to a layer file on an output geodatabase.
# Although you are not required to map the result, make sure to check your output service layer feature.
# The service area polygons can be used to visualize the areas that do not have adequate coverage from the schools.

# Each parameter is described below:

# inFacilities: The name of point shapefile (schools)
# roads: The name of the roads shapefile
# workspace: The workspace folder where the shapefiles are located.

# Below are suggested steps for your program. More code may be needed for exception handling
# and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs.
# 2- Check all possible cases where inputs can be in wrong type, different projections, etc.
# 3- Create a geodatabase using arcpy and import all initial shapefiles into feature classes. All your processes and final output should be saved into
#    the geodatabase you created. Therefore, set the workspace parameter to the geodatabase once it is created.
# 4- Using the roads linear feature class, create and build a network dataset. Check the Jupyter notebook shared on ICON,
#    which covers the basics of how to create and build a network dataset from scratch.
# 5- Use arcpy's MakeServiceAreaLayer function in the link below:
#    https://pro.arcgis.com/en/pro-app/tool-reference/network-analyst/make-service-area-layer.htm
#    Specify the following options while creating the new service area layer. Please make sure to read all the parameters needed for the function.
#       If you use "length" as impedance_attribute, you can calculate concentric service areas using 200, 400, 600, .. 2000 meters for break values.
#       Feel free to describe your own break values, however, make sure to include at least three of them.
#       Generate the service area polygons as rings, so that anyone can easily visualize the coverage for any given location if needed.
#       Use overlapping polygons to determine the number of facilities (schools) that cover a given location.
#       Use hierarchy to speed up the time taken to create the polygons.
#       Use the following values for the other parameters:
#       "TRAVEL_FROM", "DETAILED_POLYS", "MERGE"
####################################################################################################################


#REVISED FROM FEEDBACK fixed driving time
#and saves the layer file
def calculateNetworkServiceArea(inFacilities, roads, workspace):
    import os
    import sys
    import arcpy

    try:
        #Check out Network Analyst license if available. Fail if the Network Analyst license is not available.
        if arcpy.CheckExtension("network") == "Available":
            arcpy.CheckOutExtension("network")
        else:
            raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

        arcpy.env.overwriteOutput = True

        env.workspace = workspace

        #creates a geodatabase
        workspace = arcpy.CreateFileGDB_management(workspace, "mygdb.gdb")

        dscbRoad = arcpy.Describe(roads)
        dscbFac = arcpy.Describe(inFacilities)

        #Checks the projections and changes them if they are different to the projection of the inFacilities
        if dscbRoad.SpatialReference.PCSCode != dscbFac.SpatialReference.PCSCode:
            arcpy.Project_management(roads, 'roads', dscbFac.SpatialReference.PCSCode)

        #makes a variable for roads and inFacilities
        roads_shp = roads
        fac_shp = inFacilities

        #creates feature dataset
        arcpy.CreateFeatureDataset_management(arcpy.env.workspace, "featuredataset", descRoad.spatialReference)

        #copy features from the roads shapefile
        arcpy.CopyFeatures_management(roads_shp, "featuredataset/roads")

        #copy features from inFacilities file
        arcpy.CopyFeatures_management(fac_shp, "featuredataset/inFacilities")

        #creates a network dataset from the roads
        arcpy.na.CreateNetworkDataset("featuredataset", "roads_ND", ["roads"])

        #builds a network
        arcpy.BuildNetwork_na("featuredataset/roads_ND")

        #creates a service layer with length in meters of 200,400,800,1500.
        area = arcpy.na.MakeServiceAreaAnalysisLayer("featuredataset/roads_ND", "myArea", "Length",
                                                     "FROM_FACILITIES",  [200, 400, 800, 1500],
                                                     polygon_detail="HIGH", geometry_at_overlaps="OVERLAP",
                                                     geometry_at_cutoffs = "RINGS")

        #gets the output
        areaLayer = area.getOutput(0)

        #creates the classes
        na_classes = arcpy.na.GetNAClassNames(areaLayer, "INPUT")

        #gets the facilities part of the classes
        sublayer = na_classes["Facilities"]

        #adds locations of inFacilities
        arcpy.na.AddLocations(areaLayer, sublayer, "inFacilities", "", "")

        #creates a layer in the gdb
        serviceArea = arcpy.na.Solve(areaLayer)

        #saves layer file
        arcpy.management.SaveToLayerFile(serviceArea, "serviceArea")

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
