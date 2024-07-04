import os
import json
import math
import tkinter as tk
from tkinter import filedialog


# Current Version- Versions 6+ Have Better Methods And Coding Instances As Well As Additional Features In General
# This Script Provides General Cube, Plane, Cone Conversions
# This Script Includes New Conversion Methods For Planes And Cones Present Inside Object Files

def main():

    # Calculate Distances Along Each Axis
    def PlaneCalculateSizes(vertices):

        SizeX = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2 + (vertices[0][2] - vertices[1][2])**2), 2) / 2
        SizeY = 0
        SizeZ = round(math.sqrt((vertices[0][0] - vertices[2][0])**2 + (vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2) / 2

        return SizeX, SizeY, SizeZ

    # Calculates Positions Along Each Axis
    def PlaneCalculatePosition(vertices):

        SizeX, SizeY, SizeZ = PlaneCalculateSizes(vertices)

        PositionX = round(vertices[0][0] + vertices[3][0], 2) / -4 
        PositionY = round(vertices[0][2] + vertices[3][2], 2) / -4
        PositionZ = round(vertices[0][1] + vertices[3][1], 2) / 4

        PositionX = PositionX - (SizeX / 2)
        PositionY = PositionY - (SizeY / 2)
        PositionZ = PositionZ - (SizeZ / 2)

        # The Returned Position Values
        return PositionX, PositionY, PositionZ

    # Calculates Rotations Specific To Each Axis
    def PlaneCalculateRotation(vertices):

        Roll = 0
        Pitch = 0
        Yaw = 0

        # X Rotation (YZ)
        RollXYVector = (vertices[0][0], vertices[2][1], vertices[2][2])
        RollOpposite = round(math.sqrt((vertices[0][1] - RollXYVector[1])**2), 2)
        RollHypotenuse = round(math.sqrt((vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2)
        if RollHypotenuse != 0:
            Roll = round(math.degrees(math.asin(RollOpposite / RollHypotenuse)), 2)
            Roll = -Roll
        
        # Z Rotation (XY)
        PitchXYVector = (vertices[0][0], vertices[1][1], vertices[0][2])
        PitchOpposite = round(math.sqrt((vertices[0][1] - PitchXYVector[1])**2), 2)
        PitchHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2), 2)
        if PitchHypotenuse != 0:
            Pitch = round(math.degrees(math.asin(PitchOpposite / PitchHypotenuse)), 2)

        # Y Rotation (XZ)
        YawXZVector = (vertices[0][0], vertices[1][1], vertices[1][2])
        YawOpposite = round(math.sqrt((vertices[1][0] - YawXZVector[0])**2 + (vertices[1][2] - YawXZVector[2])**2), 2)
        YawHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][2] - vertices[1][2])**2), 2)
        if YawHypotenuse != 0:
            Yaw = round(math.degrees(math.acos(YawOpposite / YawHypotenuse)), 2)
        
        return Roll, Pitch, Yaw

    def PlaneCalculatePivot(vertices):

        SizeX, SizeY, SizeZ = PlaneCalculateSizes(vertices)
        PositionX, PositionY, PositionZ = PlaneCalculatePosition(vertices)

        MidpointPivotX = PositionX + (SizeX / 2)
        MidpointPivotY = PositionY + (SizeY / 2)
        MidpointPivotZ = PositionZ + (SizeZ / 2)

        return MidpointPivotX, MidpointPivotY, MidpointPivotZ



    # Calculate Distances Along Each Axis
    def CubeCalculateSizes(vertices):

        SizeX = round(math.sqrt((vertices[0][0] - vertices[4][0])**2 + (vertices[0][1] - vertices[4][1])**2 + (vertices[0][2] - vertices[4][2])**2), 2) / 2
        SizeY = round(math.sqrt((vertices[7][0] - vertices[5][0])**2 + (vertices[7][1] - vertices[5][1])**2 + (vertices[7][2] - vertices[5][2])**2), 2) / 2
        SizeZ = round(math.sqrt((vertices[4][0] - vertices[5][0])**2 + (vertices[4][1] - vertices[5][1])**2 + (vertices[4][2] - vertices[5][2])**2), 2) / 2

        return SizeX, SizeY, SizeZ

    # Calculates Positions Along Each Axis
    def CubeCalculatePosition(vertices):

        SizeX, SizeY, SizeZ = CubeCalculateSizes(vertices)

        PositionX = round(vertices[0][0] + vertices[7][0], 2) / -4 
        PositionY = round(vertices[0][2] + vertices[7][2], 2) / -4
        PositionZ = round(vertices[0][1] + vertices[7][1], 2) / 4

        PositionX = PositionX - (SizeX / 2)
        PositionY = PositionY - (SizeY / 2)
        PositionZ = PositionZ - (SizeZ / 2)

        # The Returned Position Values
        return PositionX, PositionY, PositionZ

    # Calculates Rotations Specific To Each Axis By Zeroing The Acting Rotation
    def CubeCalculateRotation(vertices):

        Roll = 0
        Pitch = 0
        Yaw = 0

        # X Rotation (YZ)
        RollXYVector = (0, vertices[0][1], vertices[2][2])
        RollOpposite = round(math.sqrt((vertices[0][1] - RollXYVector[1])**2 + (vertices[0][2] - RollXYVector[2])**2), 2)
        RollHypotenuse = round(math.sqrt((vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2)
        if RollHypotenuse != 0:
            Roll = round(math.degrees(math.asin(RollOpposite / RollHypotenuse)), 2)
        
        # Z Rotation (XY)
        PitchXYVector = (vertices[7][0], vertices[7][1], 0)
        PitchOpposite = round(math.sqrt((vertices[5][0] - PitchXYVector[0])**2), 2)
        PitchHypotenuse = round(math.sqrt((vertices[7][0] - vertices[5][0])**2 + (vertices[7][2] - vertices[5][2])**2), 2)
        if PitchHypotenuse != 0:
            Pitch = round(math.degrees(math.asin(PitchOpposite / PitchHypotenuse)), 2)

        # Y Rotation (XZ)
        YawXZVector = (vertices[0][0], 0, vertices[1][2])
        YawOpposite = round(math.sqrt((vertices[1][0] - YawXZVector[0])**2 + (vertices[1][2] - YawXZVector[2])**2), 2)
        YawHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][2] - vertices[1][2])**2), 2)
        if YawHypotenuse != 0:
            Yaw = round(math.degrees(math.asin(YawOpposite / YawHypotenuse)), 2)

        return Roll, Pitch, Yaw

    def CubeCalculatePivot(vertices):

        SizeX, SizeY, SizeZ = CubeCalculateSizes(vertices)
        PositionX, PositionY, PositionZ = CubeCalculatePosition(vertices)

        MidpointPivotX = PositionX + (SizeX / 2)
        MidpointPivotY = PositionY + (SizeY / 2)
        MidpointPivotZ = PositionZ + (SizeZ / 2)

        return MidpointPivotX, MidpointPivotY, MidpointPivotZ



    # Calculate Distances Along Each Axis
    def ConeCalculateSizes(vertices):
        
        ConeCenter = (vertices[32][0], 0, vertices[32][2])

        SizeX = round(math.sqrt((vertices[0][0] - vertices[4][0])**2 + (vertices[0][1] - vertices[4][1])**2 + (vertices[0][2] - vertices[4][2])**2), 2) / 2
        SizeY = round(math.sqrt((vertices[32][1])**2), 2) / 2
        SizeZ = round(math.sqrt((vertices[4][0] - vertices[5][0])**2 + (vertices[4][1] - vertices[5][1])**2 + (vertices[4][2] - vertices[5][2])**2), 2) / 2

        return SizeX, SizeY, SizeZ

    # Calculates Positions Along Each Axis
    def ConeCalculatePosition(vertices):

        SizeX, SizeY, SizeZ = ConeCalculateSizes(vertices)

        PositionX = round(vertices[0][0] + vertices[7][0], 2) / -4 
        PositionY = round(vertices[0][2] + vertices[7][2], 2) / -4
        PositionZ = round(vertices[0][1] + vertices[7][1], 2) / 4

        PositionX = PositionX - (SizeX / 2)
        PositionY = PositionY - (SizeY / 2)
        PositionZ = PositionZ - (SizeZ / 2)

        # The Returned Position Values
        return PositionX, PositionY, PositionZ

    # Calculates Rotations Specific To Each Axis By Zeroing The Acting Rotation
    def ConeCalculateRotation(vertices):

        Roll = 0
        Pitch = 0
        Yaw = 0

        # X Rotation (YZ)
        RollXYVector = (0, vertices[0][1], vertices[2][2])
        RollOpposite = round(math.sqrt((vertices[0][1] - RollXYVector[1])**2 + (vertices[0][2] - RollXYVector[2])**2), 2)
        RollHypotenuse = round(math.sqrt((vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2)
        if RollHypotenuse != 0:
            Roll = round(math.degrees(math.asin(RollOpposite / RollHypotenuse)), 2)
        
        # Z Rotation (XY)
        PitchXYVector = (vertices[7][0], vertices[7][1], 0)
        PitchOpposite = round(math.sqrt((vertices[5][0] - PitchXYVector[0])**2), 2)
        PitchHypotenuse = round(math.sqrt((vertices[7][0] - vertices[5][0])**2 + (vertices[7][2] - vertices[5][2])**2), 2)
        if PitchHypotenuse != 0:
            Pitch = round(math.degrees(math.asin(PitchOpposite / PitchHypotenuse)), 2)

        # Y Rotation (XZ)
        YawXZVector = (vertices[0][0], 0, vertices[1][2])
        YawOpposite = round(math.sqrt((vertices[1][0] - YawXZVector[0])**2 + (vertices[1][2] - YawXZVector[2])**2), 2)
        YawHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][2] - vertices[1][2])**2), 2)
        if YawHypotenuse != 0:
            Yaw = round(math.degrees(math.asin(YawOpposite / YawHypotenuse)), 2)

        return Roll, Pitch, Yaw

    def ConeCalculatePivot(vertices):

        SizeX, SizeY, SizeZ = ConeCalculateSizes(vertices)
        PositionX, PositionY, PositionZ = ConeCalculatePosition(vertices)

        MidpointPivotX = PositionX + (SizeX / 2)
        MidpointPivotY = PositionY + (SizeY / 2)
        MidpointPivotZ = PositionZ + (SizeZ / 2)

        return MidpointPivotX, MidpointPivotY, MidpointPivotZ
    
    # Function To Open File Explorer For Obj File
    def SelectObjFile():
        Root = tk.Tk()
        Root.withdraw()
        FilePath = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select an OBJ file", filetypes=(("OBJ files", "*.obj"), ("all files", "*.*")))
        return FilePath

    # Function To Read The Object File
    def ReadObjData(FilePath):
        with open(FilePath, 'r') as file:
            ObjData = file.read()
        return ObjData

    # Function To Save The Obj File
    def SaveObjFile(FilePath, ObjData):
        with open(FilePath, 'w') as file:
            file.write(ObjData)

    # A Function That Incorporates All Of The Previous Data
    def ProcessObjData(ObjData):

        Vertices = []
        Cubes = []

        for line in ObjData.split('\n'):
            if line.startswith('v '):
            
                Coordinates = [float(coord) for coord in line[2:].split()]
                Vertices.append(Coordinates)
            else:
                
                # Plane Shapes
                if len(Vertices) == 4:
                    # Gets The Position And Size Data For X,Y,Z
                    SizeX, SizeY, SizeZ = PlaneCalculateSizes(Vertices)
                    PositionX, PositionY, PositionZ = PlaneCalculatePosition(Vertices)
                    RotationX, RotationY, RotationZ = PlaneCalculateRotation(Vertices)
                    PivotX, PivotY, PivotZ = PlaneCalculatePivot(Vertices)

                    # Json Formatted Plane Structure
                    Cube = {
                        "origin": [PositionX + 0.5, PositionY, PositionZ],
                        "size": [SizeX, SizeY, SizeZ],
                        "rotation": [RotationX + 90, RotationY, RotationZ],
                        "pivot": [PivotX + 0.5, PivotY, PivotZ],
                        "uv": [16, 16]
                    }

                    Cubes.append(Cube)
                    Vertices = []

                # Cube Shapes
                if len(Vertices) == 8:
                    
                    # Gets The Position And Size Data For X,Y,Z
                    SizeX, SizeY, SizeZ = CubeCalculateSizes(Vertices)
                    PositionX, PositionY, PositionZ = CubeCalculatePosition(Vertices)
                    RotationX, RotationY, RotationZ = CubeCalculateRotation(Vertices)
                    PivotX, PivotY, PivotZ = CubeCalculatePivot(Vertices)

                    # Json Formatted Cube Structure
                    Cube = {
                        "origin": [PositionX + 0.5, PositionY, PositionZ],
                        "size": [SizeX, SizeY, SizeZ],
                        "rotation": [RotationX + 90, RotationY, RotationZ],
                        "pivot": [PivotX + 0.5, PivotY, PivotZ],
                        "uv": [16, 16]
                    }

                    Cubes.append(Cube)
                    Vertices = []

                # Cone Shapes
                if len(Vertices) == 33:
                    
                    # Gets The Position And Size Data For X,Y,Z
                    SizeX, SizeY, SizeZ = ConeCalculateSizes(Vertices)
                    PositionX, PositionY, PositionZ = ConeCalculatePosition(Vertices)
                    RotationX, RotationY, RotationZ = ConeCalculateRotation(Vertices)
                    PivotX, PivotY, PivotZ = ConeCalculatePivot(Vertices)

                    # Json Formatted Cone Structure
                    Cube = {
                        "origin": [PositionX + 0.5, PositionY, PositionZ],
                        "size": [SizeX, SizeY, SizeZ],
                        "rotation": [RotationX + 90, RotationY, RotationZ],
                        "pivot": [PivotX + 0.5, PivotY, PivotZ],
                        "uv": [16, 16]
                    }

                    Cubes.append(Cube)
                    Vertices = []                

            # Fail Safe (Incase Of Error Made From User Or Program)
            if line == '':
                
                # Notify The User Related To Having A Conversion Error
                if len(Vertices) > 0:
                    print(f"Program Has Detected One Or More Objects That Could Not Be Converted Due To It Not Being A Convertitable Mesh Or Possibly A Valid Object That Can Be Currently Used")
                    print(f"System Failed To Convert Object File To Json File. Program Has Aborted This Operation Instance")
                    exit()

                Vertices = []

        GeoJsonData = {
            "format_version": "1.16.100",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": "geometry.convertedobjfile",
                        "texture_width": 16,
                        "texture_height": 16,
                        "visible_bounds_width": 2,
                        "visible_bounds_height": 2.5,
                        "visible_bounds_offset": [0, 0, 0]
                    },
                    "bones": [
                        {
                            "name": "Cube",
                            "pivot": [0, 0, 0],
                            "rotation": [90, 0, 0],
                            "cubes": Cubes
                        }
                    ]
                }
            ]
        }

        GeoJsonStr = json.dumps(GeoJsonData, indent=4)
        return GeoJsonStr

    if __name__ == "__main__":

        # Select and read OBJ file
        ObjFilePath = SelectObjFile()
        if not ObjFilePath:
            print("No file selected. Exiting.")
            exit()

        ObjData = ReadObjData(ObjFilePath)

        # Process ObjData
        GeoJsonResult = ProcessObjData(ObjData)

        # Save The Results To A Geo.Json File
        TxtFilePath = os.path.join(os.path.expanduser("~\\Downloads"), "ConvertObj.geo.json")
        with open(TxtFilePath, 'w') as txt_file:
            txt_file.write(GeoJsonResult)

        # Save The Modified OBJ File
        SaveObjFile(ObjFilePath, ObjData)

        # Notify The User
        print(f"Processing Completed. Result Saved 'ConvertObj.geo.json' Into The Users Download Folder.")
        
main()