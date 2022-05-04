import arcpy
import os

def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2, identifier):
    #identifer makes the user put in the identifier for the join used in the function 
    
    #checks to see if all the inputs are strings so the function can work
    if type(input_geodatabase) != str:
        print("Error because input_geodatabase needs to be a string")
    if type(fcPolygon1) != str:
        print("Error because fcPolygon1 needs to be a string")
    if type(fcPolygon2) != str:
        print("Error because fcPolygon2 needs to be a string")
    if type(identifier) != str:
        print("Error because identifier needs to be a string")

    #Sets the workspace to where the data is.
    arcpy.env.workspace = input_geodatabase
    
    #gets the area of polygon 2 thta is in polygon 1
    arcpy.analysis.SummarizeWithin('fcPolygon1', 'fcPolygon2', 'summ_within')
    
    #adds a field for the percentage to be calculated
    arcpy.AddField_management("summ_within", "area_percentage", "Double")
    
    #calculates the percentage of area
    arcpy.management.CalculateField('summ_within', 'area_percentage', "!Summarized area! / !Shape_Area!", "PYTHON3")
    
    #joins the percentage calculated to the initial fcPolygon
    arcpy.JoinField_management("fcPolygon1", "identifier", "summ_within", "identifier", 
                           ["area_percentage"])
