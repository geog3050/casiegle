

import arcpy
import os 
import sys


#Sets the workspace to where the data is.
arcpy.env.workspace = '//Client/H$/Desktop/Spring 2022 Classes/Geo Programming/Quizzes/Quiz4/airports'

#Resets the output made by previous code so it is back to normal
arcpy.env.overwriteOutput = True


#Creates the fields in the airports.shp file to see what is in it.
fcairport = 'airports.shp'
fields = arcpy.ListFields(fcairport)


#This creates a field in the airports.shp file named "buffer" 
#so we can use it later with the update cursor
arcpy.management.AddField(fcairport, "buffer", "FLOAT")


#A for loop to go through each field in the data file so you can see the data that is in it and to make sure
#the buffer field is made
for field in fields:
    print("{0} is a type of {1} with a length of {2}"
         .format(field.name, field.type, field.length))


#This uses a cursor to update the empty values of 'buffer'
#The for loop uses the if statements to look at the value of FEATURE and updates the buffer to 7500 for seaplane, 15000 for #airport, and 0 for other types.
#Then the buffer analysis makes it into an actual buffer that can be shown on the map

with arcpy.da.UpdateCursor(fcairport, ["buffer", "FEATURE"]) as rows:
    for row in rows:
        if row[1] == "Seaplane Base":
            row[0] = 7500
        elif row[1] == "Airport":
            row[0] = 15000
        else:
            row[0] = 0
        rows.updateRow(row)
        print(row[0])
        arcpy.Buffer_analysis(fcairport, "buffer", str(row[0]) + " " + "Meters")

# Error handling for errors in the buffer\

try:
    arcpy.Buffer_analysis('//Client/H$/Desktop/Spring 2022 Classes/Geo Programming/Quizzes/Quiz4/airports/airports.shp', '//Client/H$/Desktop/Spring 2022 Classes/Geo Programming/Quizzes/Quiz4/airports/buffer.shp')\
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
}
