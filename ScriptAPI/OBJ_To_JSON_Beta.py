import os
import json
import math
import tkinter as tk
from tkinter import filedialog, messagebox


# Current Version- Versions 6+ Have Better Methods And Coding Instances As Well As Additional Features In General
# This Script Provides General Cube, Plane, Cone Conversions
# This Script Includes New Conversion Methods For Planes And Cones Present Inside Object Files

class Plane:

    def Calculate_Sizes(vertices):

        SizeX = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2 + (vertices[0][2] - vertices[1][2])**2), 2) / 2
        SizeY = 0
        SizeZ = round(math.sqrt((vertices[0][0] - vertices[2][0])**2 + (vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2) / 2

        return SizeX, SizeY, SizeZ

    def Calculate_Position(vertices):

        SizeX, SizeY, SizeZ = Plane.Calculate_Sizes(vertices)

        PositionX = round(vertices[0][0] + vertices[3][0], 2) / -4 
        PositionY = round(vertices[0][2] + vertices[3][2], 2) / -4
        PositionZ = round(vertices[0][1] + vertices[3][1], 2) / 4

        PositionX -= SizeX / 2
        PositionY -= SizeY / 2
        PositionZ -= SizeZ / 2

        return PositionX, PositionY, PositionZ

    def Calculate_Rotation(vertices):

        Roll = 0
        Pitch = 0
        Yaw = 0

        RollXYVector = (vertices[0][0], vertices[2][1], vertices[2][2])
        RollOpposite = round(math.sqrt((vertices[0][1] - RollXYVector[1])**2), 2)
        RollHypotenuse = round(math.sqrt((vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2)

        if RollHypotenuse != 0:
            Roll = round(math.degrees(math.asin(RollOpposite / RollHypotenuse)), 2)
            Roll = -Roll

        PitchXYVector = (vertices[0][0], vertices[1][1], vertices[0][2])
        PitchOpposite = round(math.sqrt((vertices[0][1] - PitchXYVector[1])**2), 2)
        PitchHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2), 2)
        
        if PitchHypotenuse != 0:
            Pitch = round(math.degrees(math.asin(PitchOpposite / PitchHypotenuse)), 2)

        YawXZVector = (vertices[0][0], vertices[1][1], vertices[1][2])
        YawOpposite = round(math.sqrt((vertices[1][0] - YawXZVector[0])**2 + (vertices[1][2] - YawXZVector[2])**2), 2)
        YawHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][2] - vertices[1][2])**2), 2)

        if YawHypotenuse != 0:
            Yaw = round(math.degrees(math.acos(YawOpposite / YawHypotenuse)), 2)

        return Roll, Pitch, Yaw

    def Calculate_Pivot(vertices):

        SizeX, SizeY, SizeZ = Plane.Calculate_Sizes(vertices)
        PositionX, PositionY, PositionZ = Plane.Calculate_Position(vertices)

        MidpointPivotX = PositionX + SizeX / 2
        MidpointPivotY = PositionY + SizeY / 2
        MidpointPivotZ = PositionZ + SizeZ / 2

        return MidpointPivotX, MidpointPivotY, MidpointPivotZ

class Cube:

    def Calculate_Sizes(vertices):

        SizeX = round(math.sqrt((vertices[0][0] - vertices[4][0])**2 + (vertices[0][1] - vertices[4][1])**2 + (vertices[0][2] - vertices[4][2])**2), 2) / 2
        SizeY = round(math.sqrt((vertices[7][0] - vertices[5][0])**2 + (vertices[7][1] - vertices[5][1])**2 + (vertices[7][2] - vertices[5][2])**2), 2) / 2
        SizeZ = round(math.sqrt((vertices[4][0] - vertices[5][0])**2 + (vertices[4][1] - vertices[5][1])**2 + (vertices[4][2] - vertices[5][2])**2), 2) / 2

        return SizeX, SizeY, SizeZ

    def Calculate_Position(vertices):

        SizeX, SizeY, SizeZ = Cube.Calculate_Sizes(vertices)

        PositionX = round(vertices[0][0] + vertices[7][0], 2) / -4 
        PositionY = round(vertices[0][2] + vertices[7][2], 2) / -4
        PositionZ = round(vertices[0][1] + vertices[7][1], 2) / 4

        PositionX -= SizeX / 2
        PositionY -= SizeY / 2
        PositionZ -= SizeZ / 2

        return PositionX, PositionY, PositionZ

    def Calculate_Rotation(vertices):

        Roll = 0
        Pitch = 0
        Yaw = 0

        RollXYVector = (0, vertices[0][1], vertices[2][2])
        RollOpposite = round(math.sqrt((vertices[0][1] - RollXYVector[1])**2 + (vertices[0][2] - RollXYVector[2])**2), 2)
        RollHypotenuse = round(math.sqrt((vertices[0][1] - vertices[2][1])**2 + (vertices[0][2] - vertices[2][2])**2), 2)

        if RollHypotenuse != 0:
            Roll = round(math.degrees(math.asin(RollOpposite / RollHypotenuse)), 2)

        PitchXYVector = (vertices[7][0], vertices[7][1], 0)
        PitchOpposite = round(math.sqrt((vertices[5][0] - PitchXYVector[0])**2), 2)
        PitchHypotenuse = round(math.sqrt((vertices[7][0] - vertices[5][0])**2 + (vertices[7][2] - vertices[5][2])**2), 2)

        if PitchHypotenuse != 0:
            Pitch = round(math.degrees(math.asin(PitchOpposite / PitchHypotenuse)), 2)

        YawXZVector = (vertices[0][0], 0, vertices[1][2])
        YawOpposite = round(math.sqrt((vertices[1][0] - YawXZVector[0])**2 + (vertices[1][2] - YawXZVector[2])**2), 2)
        YawHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][2] - vertices[1][2])**2), 2)

        if YawHypotenuse != 0:
            Yaw = round(math.degrees(math.asin(YawOpposite / YawHypotenuse)), 2)

        return Roll, Pitch, Yaw

    def Calculate_Pivot(vertices):

        SizeX, SizeY, SizeZ = Cube.Calculate_Sizes(vertices)
        PositionX, PositionY, PositionZ = Cube.Calculate_Position(vertices)

        MidpointPivotX = PositionX + SizeX / 2
        MidpointPivotY = PositionY + SizeY / 2
        MidpointPivotZ = PositionZ + SizeZ / 2

        return MidpointPivotX, MidpointPivotY, MidpointPivotZ

class Cone:

    def Calculate_Sizes(vertices):

        ConeCenter = (vertices[32][0], 0, vertices[32][2])

        SizeX = round(math.sqrt((vertices[0][0] - vertices[4][0])**2 + (vertices[0][1] - vertices[4][1])**2 + (vertices[0][2] - vertices[4][2])**2), 2) / 2
        SizeY = round(math.sqrt((vertices[32][1])**2), 2) / 2
        SizeZ = round(math.sqrt((vertices[4][0] - vertices[5][0])**2 + (vertices[4][1] - vertices[5][1])**2 + (vertices[4][2] - vertices[5][2])**2), 2) / 2

        return SizeX, SizeY, SizeZ

    def Calculate_Position(vertices):

        SizeX, SizeY, SizeZ = Cone.Calculate_Sizes(vertices)

        PositionX = round(vertices[32][0] + vertices[16][0], 2) / -4
        PositionY = round(vertices[32][1], 2) / -2
        PositionZ = round(vertices[32][2] + vertices[16][2], 2) / 4

        PositionX -= SizeX / 2
        PositionY -= SizeY / 2
        PositionZ -= SizeZ / 2

        return PositionX, PositionY, PositionZ

    def Calculate_Rotation(vertices):

        Roll = 0
        Pitch = 0
        Yaw = 0

        RollXYVector = (vertices[0][0], vertices[32][1], vertices[0][2])
        RollOpposite = round(math.sqrt((vertices[0][1] - RollXYVector[1])**2 + (vertices[0][2] - RollXYVector[2])**2), 2)
        RollHypotenuse = round(math.sqrt((vertices[0][1] - vertices[32][1])**2 + (vertices[0][2] - vertices[32][2])**2), 2)

        if RollHypotenuse != 0:
            Roll = round(math.degrees(math.asin(RollOpposite / RollHypotenuse)), 2)

        PitchXYVector = (vertices[32][0], vertices[0][1], vertices[0][2])
        PitchOpposite = round(math.sqrt((vertices[32][1] - PitchXYVector[1])**2), 2)
        PitchHypotenuse = round(math.sqrt((vertices[32][0] - vertices[0][0])**2 + (vertices[32][1] - vertices[0][1])**2), 2)

        if PitchHypotenuse != 0:
            Pitch = round(math.degrees(math.asin(PitchOpposite / PitchHypotenuse)), 2)

        YawXZVector = (vertices[0][0], 0, vertices[1][2])
        YawOpposite = round(math.sqrt((vertices[1][0] - YawXZVector[0])**2 + (vertices[1][2] - YawXZVector[2])**2), 2)
        YawHypotenuse = round(math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][2] - vertices[1][2])**2), 2)

        if YawHypotenuse != 0:
            Yaw = round(math.degrees(math.asin(YawOpposite / YawHypotenuse)), 2)

        return Roll, Pitch, Yaw

    def Calculate_Pivot(vertices):

        SizeX, SizeY, SizeZ = Cone.Calculate_Sizes(vertices)
        PositionX, PositionY, PositionZ = Cone.Calculate_Position(vertices)

        MidpointPivotX = PositionX + SizeX / 2
        MidpointPivotY = PositionY + SizeY / 2
        MidpointPivotZ = PositionZ + SizeZ / 2
        
        return MidpointPivotX, MidpointPivotY, MidpointPivotZ

def main():

    def SearchDirectory():

        # Getting User Pathway
        User_Home = os.path.expanduser("~")
        InitialDirectory = '/'
        DirectoryName = 'MasterCraft'

        Common_User_Directories = ['Desktop', 'Downloads', 'Pictures', 'Documents', 'Music', 'Videos']

        def Common_Directory():
            for Common_Directories in Common_User_Directories:
                Common_Dir = os.path.join(User_Home, Common_Directories)
                for root, dirnames, _ in os.walk(Common_Dir):
                    if DirectoryName in dirnames:
                        return os.path.join(root, DirectoryName)
            return None

        def Full_Search_Directory():
            matches = []
            for root, dirnames, _ in os.walk(InitialDirectory):
                if DirectoryName in dirnames:
                    matches.append(os.path.join(root, DirectoryName))
            return matches

        def DirectoryPathfinding():
            InitialDirectoryTest = Common_Directory()
            if InitialDirectoryTest is None:
                return Full_Search_Directory()
            else:
                return [InitialDirectoryTest]

        return DirectoryPathfinding()

    # Function To Open File Explorer For Obj File
    def SelectObjFile():

        Root = tk.Tk()

        MasterCraftCurrentDirectory = os.path.normpath(SearchDirectory()[0])

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(MasterCraftCurrentDirectory, "Textures", "IconImage.ico")
        Root.iconbitmap(Icon_Image_Path)

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

    # A Function That Incorporates Shape Conversions Of The Read Data
    def ProcessObjDataShape(ObjData):

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
                    SizeX, SizeY, SizeZ = Plane.Calculate_Sizes(Vertices)
                    PositionX, PositionY, PositionZ = Plane.Calculate_Position(Vertices)
                    RotationX, RotationY, RotationZ = Plane.Calculate_Rotation(Vertices)
                    PivotX, PivotY, PivotZ = Plane.Calculate_Pivot(Vertices)

                    # Json Formatted Plane Structure
                    CubeData = {
                        "origin": [PositionX + 0.5, PositionY, PositionZ],
                        "size": [SizeX, SizeY, SizeZ],
                        "rotation": [RotationX + 90, RotationY, RotationZ],
                        "pivot": [PivotX + 0.5, PivotY, PivotZ],
                        "uv": [16, 16]
                    }

                    Cubes.append(CubeData)
                    Vertices = []

                # Cube Shapes
                if len(Vertices) == 8:
                    
                    # Gets The Position And Size Data For X,Y,Z
                    SizeX, SizeY, SizeZ = Cube.Calculate_Sizes(Vertices)
                    PositionX, PositionY, PositionZ = Cube.Calculate_Position(Vertices)
                    RotationX, RotationY, RotationZ = Cube.Calculate_Rotation(Vertices)
                    PivotX, PivotY, PivotZ = Cube.Calculate_Pivot(Vertices)

                    # Json Formatted Cube Structure
                    CubeData = {
                        "origin": [PositionX + 0.5, PositionY, PositionZ],
                        "size": [SizeX, SizeY, SizeZ],
                        "rotation": [RotationX + 90, RotationY, RotationZ],
                        "pivot": [PivotX + 0.5, PivotY, PivotZ],
                        "uv": [16, 16]
                    }

                    Cubes.append(CubeData)
                    Vertices = []

                # Cone Shapes
                if len(Vertices) == 33:
                    
                    # Gets The Position And Size Data For X,Y,Z
                    SizeX, SizeY, SizeZ = Cone.Calculate_Sizes(Vertices)
                    PositionX, PositionY, PositionZ = Cone.Calculate_Position(Vertices)
                    RotationX, RotationY, RotationZ = Cone.Calculate_Rotation(Vertices)
                    PivotX, PivotY, PivotZ = Cone.Calculate_Pivot(Vertices)

                    # Json Formatted Cone Structure
                    CubeData = {
                        "origin": [PositionX + 0.5, PositionY, PositionZ],
                        "size": [SizeX, SizeY, SizeZ],
                        "rotation": [RotationX + 90, RotationY, RotationZ],
                        "pivot": [PivotX + 0.5, PivotY, PivotZ],
                        "uv": [16, 16]
                    }

                    Cubes.append(CubeData)
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

    # A Function That Incorporates Plane Conversions Of The Read Data
    def ProcessObjDataPlane(ObjData):

        Vertices = []
        Normal_Vertices = []
        Vertex_Texture = []
        PlaneData = []

        for line in ObjData.split('\n'):

            if line.startswith('v '):

                Coordinates = [float(coord) for coord in line[2:].split()]
                Vertices.append(Coordinates)

        for line in ObjData.split('\n'):

            if line.startswith('vn '):

                Coordinates = [float(coord) for coord in line[2:].split()]
                Normal_Vertices.append(Coordinates)
            
        for line in ObjData.split('\n'):

            if line.startswith('vt '):

                Coordinates = [float(coord) for coord in line[3:].split()]
                Vertex_Texture.append(Coordinates)
            
        for line in ObjData.split('\n'):

            if line.startswith('f '):

                Coordinates = line[2:].split()
                PlaneData.append(Coordinates)

        # v/vt/vn Face Pattern
        def ProcessPlaneData(PlaneData, Vertices, Vertex_Texture, Normal_Vertices):

            AllFaces = []

            for Plane in PlaneData:

                Triangles = []

                for vertex in Plane:

                    V, VT, VN = map(int, vertex.split('/'))
                    PlaneVertex = Vertices[V - 1]
                    PlaneVertexTexture = Vertex_Texture[VT - 1]
                    PlaneVertexNormal = Normal_Vertices[VN - 1]

                    Triangles.append((PlaneVertex, PlaneVertexTexture, PlaneVertexNormal))

                FaceLength = 4

                for I in range(0, len(Triangles), FaceLength):

                    Face = Triangles[I:I+FaceLength]
                    
                    if len(Face) == FaceLength:
                        AllFaces.append(Face)

            return AllFaces
        
        # Debugging Purposes
        def TraingleInterpreter():

            VertexData = ProcessPlaneData(PlaneData, Vertices, Vertex_Texture, Normal_Vertices)
            TriangleFaces = []

            for I in range(0, len(VertexData), 1):
                
                print("s")

                # Face
                V1 = VertexData[I][0]
                V2 = VertexData[I][1]
                V3 = VertexData[I][2]
                V4 = VertexData[I][3]             

                TriangleFaces.append((V1, V2, V3, V4))
                VertexData[3:]

            return TriangleFaces

        def TraingleConverter():
            
            Plane = TraingleInterpreter()
            Vertices_Coordinate = []
            Cubes = []
            Lines = []

            for I in range(0, len(Plane), 1):
                
                VPlane1 = Plane[I][0][0]
                VPlane2 = Plane[I][1][0]
                VPlane3 = Plane[I][2][0]
                VPlane4 = Plane[I][3][0]
                
                Sizes = []

                def CubeGenerate():
                    
                    # Side 1
                    if VPlane1[0] != VPlane2[0]:
                        Sizes.append(abs(VPlane1[0] - VPlane2[0]))
                    else:
                        Sizes.append(1)

                    if VPlane1[1] != VPlane2[1]:
                        Sizes.append(abs(VPlane1[0] - VPlane2[0]))
                    else:
                        Sizes.append(1)

                    if VPlane1[2] != VPlane2[2]:
                        Sizes.append(abs(VPlane1[0] - VPlane2[0]))
                    else:
                        Sizes.append(1)

                    # Side 3
                    if VPlane2[0] != VPlane3[0]:
                        Sizes.append(abs(VPlane2[0] - VPlane3[0]))
                    else:
                        Sizes.append(1)

                    if VPlane2[1] != VPlane3[1]:
                        Sizes.append(abs(VPlane2[1] - VPlane3[1]))
                    else:
                        Sizes.append(1)

                    if VPlane2[2] != VPlane3[2]:
                        Sizes.append(abs(VPlane2[2] - VPlane3[2]))
                    else:
                        Sizes.append(1)
                    
                    # Side 3
                    if VPlane3[0] != VPlane4[0]:
                        Sizes.append(abs(VPlane3[0] - VPlane4[0]))
                    else:
                        Sizes.append(1)

                    if VPlane3[1] != VPlane4[1]:
                        Sizes.append(abs(VPlane3[1] - VPlane4[1]))
                    else:
                        Sizes.append(1)

                    if VPlane3[2] != VPlane4[2]:
                        Sizes.append(abs(VPlane3[2] - VPlane4[2]))
                    else:
                        Sizes.append(1)

                
                #Sizes.append(abs(vertices[0][0] - vertices[3][0]))  # Size between VPlane4 and VPlane1 (X dimension)
                #Sizes.append(abs(vertices[0][2] - vertices[2][2]))  # Size between VPlane1 and VPlane3 (Z dimension)

                CubeData = {
                    "origin": [PositionX + 0.5, PositionY, PositionZ],
                    "size": [SizeX, SizeY, SizeZ],
                    "rotation": [0, 0, 0],
                    "pivot": [0, 0, 0],
                    "uv": [16, 16]
                }
                
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
                
                Cubes[3:]
                Vertices_Coordinate.append((VPlane1, VPlane2, VPlane3, VPlane4))
                Plane[3:]


                GeoJsonStr = json.dumps(GeoJsonData, indent=4)
                return GeoJsonStr

    if __name__ == "__main__":
        
        Message = messagebox.askquestion(title="MasterCraft - Object Conversion Type", message="Would You Like To Use Plane Converter Method? This Method Simply Makes Plane Triangles Like How Object Files Would Be Converted (However It May Produce Tons Of Cube Blocks). If So Please Press Yes. Otherwise If You Would Like To Use Shape Converter Method Press No")

        if Message == "yes":

            # Select and read OBJ file
            ObjFilePath = SelectObjFile()

            if not ObjFilePath:
                print("No file selected. Exiting.")
                exit()

            ObjData = ReadObjData(ObjFilePath)

            # Process ObjData
            GeoJsonResult = ProcessObjDataPlane(ObjData)

            # Save The Results To A Geo.Json File
            TxtFilePath = os.path.join(os.path.expanduser("~\\Downloads"), "ConvertObj.geo.json")

            with open(TxtFilePath, 'w') as txt_file:
                txt_file.write(GeoJsonResult)

            # Save The Modified OBJ File
            SaveObjFile(ObjFilePath, ObjData)

            # Notify The User
            print(f"Processing Completed. Result Saved 'ConvertObj.geo.json' Into The Users Download Folder.")
        
        else:

            # Select and read OBJ file
            ObjFilePath = SelectObjFile()

            if not ObjFilePath:
                print("No file selected. Exiting.")
                exit()

            ObjData = ReadObjData(ObjFilePath)

            # Process ObjData
            GeoJsonResult = ProcessObjDataShape(ObjData)

            # Save The Results To A Geo.Json File
            TxtFilePath = os.path.join(os.path.expanduser("~\\Downloads"), "ConvertObj.geo.json")

            with open(TxtFilePath, 'w') as txt_file:
                txt_file.write(GeoJsonResult)

            # Save The Modified OBJ File
            SaveObjFile(ObjFilePath, ObjData)

            # Notify The User
            print(f"Processing Completed. Result Saved 'ConvertObj.geo.json' Into The Users Download Folder.")

main()