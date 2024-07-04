import os
import json
import math
import tkinter as tk
from tkinter import filedialog

# Define functions to process JSON data and convert it into an OBJ file

def main():

    def CubeCalculateSizes(Sizes):
        SizeX = Sizes[0]
        SizeY = Sizes[1]
        SizeZ = Sizes[2]

        return SizeX, SizeY, SizeZ
    
    # Process JSON data
    def ProcessJsonData(JsonData):
        Cubes = []
        for cube in JsonData["minecraft:geometry"][0]["bones"][0]["cubes"]:
            SizeX, SizeY, SizeZ = CubeCalculateSizes(cube["size"])
            PositionX, PositionY, PositionZ = cube["origin"]
            RotationX, RotationY, RotationZ = cube["rotation"]

            vertices = (PositionX, PositionY, PositionZ, SizeX, SizeY, SizeZ, RotationX, RotationY, RotationZ)
            Cubes.append(vertices)

        #ObjData = convert_cubes_to_obj(Cubes)
        #return ObjData

    # Read JSON file
    def ReadJsonData(FilePath):
        with open(FilePath, 'r') as file:
            JsonData = json.load(file)
        return JsonData

    # Function to save the OBJ file
    def SaveObjFile(FilePath, JsonData):
        with open(FilePath, 'w') as file:
            file.write(JsonData)

    # Function To Open File Explorer For Obj File
    def SelectJsonFile():
        Root = tk.Tk()
        Root.withdraw()
        FilePath = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select an JSON file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        return FilePath
    
    if __name__ == "__main__":

        # Select and read JSON file
        JsonFilePath = SelectJsonFile()
        if not JsonFilePath:
            print("No file selected. Exiting.")
            exit()

        JsonData = ReadJsonData(JsonFilePath)

        # Process JSON data
        JsonResult = ProcessJsonData(JsonData)
        print(JsonResult)
        # Save the result as an OBJ file
        ObjFilePath = os.path.join(os.path.expanduser("~\\Downloads"), "ConvertJson.obj")
        SaveObjFile(ObjFilePath, JsonResult)

        # Notify the user
        print(f"Processing Completed. Result Saved 'ConvertJson.obj' Into The Users Download Folder.")

main()
