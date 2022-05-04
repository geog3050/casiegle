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
import arcpy
import os 

def hawkid():
    return(["Caleb Siegle", "casiegle"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):



    #checks to see if the workspace is a string
    if type(workspace) != str:
        print("Enter the path as a string")
        break
    
    #sets the workspace 
    arcpy.env.workspace = workspace
    #creates a list of feature classes in thew workspace
    featureClasses = arcpy.ListFeatureClasses

    
    #loops through the list to show the name and geometry type of that feature class
    for fc in featureClasses:
        dscb = arcpy.Describe(fc)
        print("{0} is a {1} feature class.".format(fc, dscb.shapeType))
    

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    
    #checks to see if the workspace is a string
    if type(workspace) != str:
        print("Enter the path as a string")
    
    #cheks toi see if inputFC is a string
    if type(inputFC) != str:
        print("Enter inputFC as a string")
        
    #sets the workspace 
    arcpy.env.workspace = workspace

    #takes into account the input feature class
    fc = inputFC
    #lists the fields in the feature class
    fields = arcpy.ListFields(fc)
    #loops through the fields in the list of fields and prints the numerical values because of the if statement
    for field in fields:
        if field.type == "Integer" or field.type == "Float" or field.type == "Double":
            print("{0} is a type of {1}.".format(field.name, field.type))

    

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):


    #checks to see if shapeType is one of the options availale in the function
    if shapeType != "point" or shapeType != "line" or shapeType != "polygon":
        print("shapeType must be either point, line, or polygon.)
    #checks to see if inputs (paths) are a string
    if type(input_geodatabase) != str:
              print("input_geodatabase needs to be a string")
    if type(output_geodatabase) != str:
              print("output_geodatabase needs to be a string")


    
    #gets the direct path of the orginal gdb
    dir_path = os.path.dirname(os.path.realpath(input_geodatabase))



    #creates a new gdb with the path of the input and then adds the name of the output gdb
    arcpy.CreateFileGDB_management(dir_path, output_geodatabase)



#copy feature classes given the shape type

    featureClasses = arcpy.ListFeatureClasses(input_geodatabase)

# Execute CopyFeatures for each input shapefile
    for fc in featureClasses:
    
    #takes into account the shapeType from the function
        dscb = arcpy.Describe(fc)
        if dscb.shapeType == shapeType:
        
    # Determine the new output feature class path and name
            out_featureClass = os.path.join(dir_path, os.path.splitext(fc)[0])
     #Copy's specified features from shapeType into new gdb
            arcpy.CopyFeatures_management(fc, output_geodatabase)
    
    
    


###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):

    #sets the workspace 
    arcpy.env.workspace = workspace

    #checks to see if all the inputs are strings so the function can work
    if type(inputFc) != str:
        print("Error because inputFc needs to be a string")
    if type(idFieldInputFc) != str:
        print("Error because idFieldInputFc needs to be a string")
    if type(inputTable) != str:
        print("Error because inputTable needs to be a string")
    if type(idFieldTable) != str:
        print("Error because idFieldTable needs to be a string")
    if type(workspace) != str:
        print("Error because workspace path needs to be a string")
    
    joinedTable = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
    
    #exports new features to a new feature class
    arcpy.CopyFeatures_management(joinedTable, newfc)
    #prints the results of the joined output 
    print(joinedTable)


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
