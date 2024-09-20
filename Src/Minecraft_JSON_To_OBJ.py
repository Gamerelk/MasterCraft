import json
from tkinter import Tk, filedialog, messagebox
import os
import math

class JsonToObjectApp():

    def __init__(self):
        super().__init__()

        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        Root = Tk()
        Root.withdraw()

        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        Root.iconbitmap(default=Icon_Path)

        self.Initialize_Variables()

        # Get The JSON File
        Json_File_Path = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select A JSON File", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))

        Json_Data = self.Load_Json(Json_File_Path)

        Response = messagebox.askyesno("Object Conversion", "Would You Like To Selected A Texture Onto Your Object")

        if Response == True:

            # Get The Texture File
            Texture_File_Path = filedialog.askopenfilename(initialdir=os.path.dirname(Json_File_Path), title="Select Texture File", filetypes=(("PNG files", "*.png"), ("all files", "*.*")))

            self.Create_Object_Modal_With_Textures(Json_Data, Texture_File_Path)

        else:
            self.Create_Object_Modal_Only_Model(Json_Data)
        
    def Initialize_Variables(self):

        self.X_Flip = True
        self.Y_Flip = False
        self.Z_Flip = False
        self.UV_Flip_X = False
        self.UV_Flip_Y = True

    def Load_Json(self, File_Path):

        try:
            with open(File_Path, 'r') as File:
                return json.load(File)
            
        except Exception as e:
            return

    def Write_Object_Data_With_Textures(self, Vertices, Faces, UV_Coords, File_Path, MTL_Name):

        with open(File_Path, 'w') as File:

            File.write(f"mtllib {MTL_Name}\n")
            File.write(f"usemtl material0\n\n")

            for Vertex in Vertices:
                File.write(f"v {Vertex[0]} {Vertex[1]} {Vertex[2]}\n")

            for UV in UV_Coords:
                File.write(f"vt {UV[0]} {UV[1]}\n")

            for Face in Faces:
                File.write(f"f {' '.join(f'{Vertex}/{Vertex_Texture}' for Vertex, Vertex_Texture in Face)}\n")

    def Write_Object_Data_Only_Modal(self, Vertices, Faces, File_Path):

        with open(File_Path, 'w') as File:

            for Vertex in Vertices:
                File.write(f"v {Vertex[0]} {Vertex[1]} {Vertex[2]}\n")

            for Face in Faces:
                File.write(f"f {' '.join(str(Index) for Index in Face)}\n")

    def Write_MTL_Data(self, File_Path, Texture_Name):

        with open(File_Path, 'w') as File:

            File.write("newmtl material0\n")
            File.write("Ka 1.000000 1.000000 1.000000\n")
            File.write("Kd 1.000000 1.000000 1.000000\n")
            File.write("Ks 0.000000 0.000000 0.000000\n")
            File.write("Ns 10.000000\n")
            File.write("illum 2\n")
            File.write(f"map_Kd {Texture_Name}\n")

    def Create_Object_Modal_With_Textures(self, Json_Data, Texture_File_Path):

        # Extract Cubes From The JSON
        Geometry_Data = Json_Data.get('minecraft:geometry', [])

        Vertices = []
        Faces = []
        UV_Coords = []

        Texture_Width = Json_Data['minecraft:geometry'][0]['description']['texture_width']
        Texture_Height = Json_Data['minecraft:geometry'][0]['description']['texture_height']

        for Geometry in Geometry_Data:

            Bones = Geometry.get('bones', [])
            
            for Bone in Bones:

                # Extract Bone Collection Data
                Cubes = Bone.get('cubes', [])
                Bone_Pivot = Bone.get('pivot', [0, 0, 0])
                Bone_Rotation = Bone.get('rotation', [0, 0, 0])

                for Cube in Cubes:

                    Origin = Cube['origin']
                    Size = Cube['size']
                    Pivot = Cube.get('pivot', [0, 0, 0])
                    Rotation = Cube.get('rotation', [0, 0, 0])
                    UV = Cube['uv']

                    # Calculate Cube Vertices
                    X, Y, Z = Origin
                    DX, DY, DZ = Size

                    Cube_Vertices = [
                        [X, Y, Z], [X + DX, Y, Z], [X + DX, Y + DY, Z], [X, Y + DY, Z],
                        [X, Y, Z + DZ], [X + DX, Y, Z + DZ], [X + DX, Y + DY, Z + DZ], [X, Y + DY, Z + DZ]
                    ]

                    def ApplyRotation(Vertices, Pivot, Rotation, Bone_Pivot, Bone_Rotation):

                        Rotated_Vertices = []
                        PX, PY, PZ = Pivot
                        BPX, BPY, BPZ = Bone_Pivot
                        RX, RY, RZ = [math.radians(Angle) for Angle in Rotation]
                        BRX, BRY, BRZ = [math.radians(Angle) for Angle in Bone_Rotation]

                        def Rotation_Matrix(X, Y, Z, Pivot_X, Pivot_Y, Pivot_Z, Rotation_X, Rotation_Y, Rotation_Z):

                            # Translate To Origin
                            X, Y, Z = X - Pivot_X, Y - Pivot_Y, Z - Pivot_Z

                            # Rotate X-Axis
                            Y, Z = Y * math.cos(-Rotation_X) - Z * math.sin(-Rotation_X), Y * math.sin(-Rotation_X) + Z * math.cos(-Rotation_X)

                            # Rotate Y-Axis
                            X, Z = X * math.cos(Rotation_Y) + Z * math.sin(Rotation_Y), -X * math.sin(Rotation_Y) + Z * math.cos(Rotation_Y)
                            
                            # Rotate Z-Axis
                            X, Y = X * math.cos(-Rotation_Z) - Y * math.sin(-Rotation_Z), X * math.sin(-Rotation_Z) + Y * math.cos(-Rotation_Z)

                            # Translate Back
                            return X + Pivot_X, Y + Pivot_Y, Z + Pivot_Z

                        for Vertex in Vertices:

                            X, Y, Z = Vertex

                            # Apply Cube Rotation
                            X, Y, Z = Rotation_Matrix(X, Y, Z, PX, PY, PZ, RX, RY, RZ)

                            # Apply Bone Rotation
                            X, Y, Z = Rotation_Matrix(X, Y, Z, BPX, BPY, BPZ, BRX, BRY, BRZ)

                            Rotated_Vertices.append([X, Y, Z])

                        return Rotated_Vertices

                    Rotated_Vertices = ApplyRotation(Cube_Vertices, Pivot, Rotation, Bone_Pivot, Bone_Rotation)

                    if self.X_Flip:

                        for Cubes in Rotated_Vertices:
                            Cubes[0] = Cubes[0] * -1

                    if self.Y_Flip:

                        for Cubes in Rotated_Vertices:
                            Cubes[1] = Cubes[1] * -1
                        
                    if self.Z_Flip:

                        for Cubes in Rotated_Vertices:
                            Cubes[2] = Cubes[2] * -1

                    # Add Cube Vertices To The Array
                    Vertex_Start = len(Vertices) + 1
                    Vertices.extend(Rotated_Vertices)

                    for Face, UV_Data in UV.items():

                        UV_Position_X, UV_Position_Y = UV_Data['uv']
                        UV_Size_X, UV_Size_Y = UV_Data['uv_size']
                        
                        def Calculate_UV():

                            # Normalize UV Coordinates
                            UV_Left_X, UV_Top_Y = UV_Position_X / Texture_Width, 1 - (UV_Position_Y / Texture_Height)
                            UV_Right_X, UV_Bottom_Y = (UV_Position_X + UV_Size_X) / Texture_Width, 1 - ((UV_Position_Y + UV_Size_Y) / Texture_Height)

                            # Flip UV in the X axis
                            if self.UV_Flip_X and not self.UV_Flip_Y:
                                UV_Coords.extend([
                                    (UV_Right_X, UV_Top_Y),
                                    (UV_Left_X, UV_Top_Y),
                                    (UV_Left_X, UV_Bottom_Y),
                                    (UV_Right_X, UV_Bottom_Y)
                                ])

                            # Flip UV in the Y axis
                            elif self.UV_Flip_Y and not self.UV_Flip_X:
                                UV_Coords.extend([
                                    (UV_Left_X, UV_Bottom_Y), 
                                    (UV_Right_X, UV_Bottom_Y),
                                    (UV_Right_X, UV_Top_Y), 
                                    (UV_Left_X, UV_Top_Y)
                                ])
                                
                            # Flip UV in both X and Y axis
                            elif self.UV_Flip_X and self.UV_Flip_Y:
                                UV_Coords.extend([
                                    (UV_Right_X, UV_Bottom_Y),
                                    (UV_Left_X, UV_Bottom_Y),
                                    (UV_Left_X, UV_Top_Y),
                                    (UV_Right_X, UV_Top_Y)
                                ])

                            # No UV Flip
                            else:
                                UV_Coords.extend([
                                    (UV_Left_X, UV_Top_Y), 
                                    (UV_Right_X, UV_Top_Y), 
                                    (UV_Right_X, UV_Bottom_Y), 
                                    (UV_Left_X, UV_Bottom_Y)
                                ])

                        Calculate_UV()

                    # 24 UV Coordinates Per Cube (4 Per Face)
                    UV_Start = len(UV_Coords) - 23  

                    # Define Faces For The Cube (6 Faces, Each With 4 Vertices)
                    Cube_Faces = [
                        [(Vertex_Start, UV_Start), (Vertex_Start + 1, UV_Start + 1), (Vertex_Start + 2, UV_Start + 2), (Vertex_Start + 3, UV_Start + 3)],
                        [(Vertex_Start + 4, UV_Start + 4), (Vertex_Start + 5, UV_Start + 5), (Vertex_Start + 6, UV_Start + 6), (Vertex_Start + 7, UV_Start + 7)],
                        [(Vertex_Start, UV_Start + 8), (Vertex_Start + 4, UV_Start + 9), (Vertex_Start + 7, UV_Start + 10), (Vertex_Start + 3, UV_Start + 11)],
                        [(Vertex_Start + 1, UV_Start + 12), (Vertex_Start + 5, UV_Start + 13), (Vertex_Start + 6, UV_Start + 14), (Vertex_Start + 2, UV_Start + 15)],
                        [(Vertex_Start, UV_Start + 16), (Vertex_Start + 1, UV_Start + 17), (Vertex_Start + 5, UV_Start + 18), (Vertex_Start + 4, UV_Start + 19)],
                        [(Vertex_Start + 3, UV_Start + 20), (Vertex_Start + 2, UV_Start + 21), (Vertex_Start + 6, UV_Start + 22), (Vertex_Start + 7, UV_Start + 23)]
                    ]

                    Faces.extend(Cube_Faces)

        Model_Name = os.path.splitext(os.path.basename(Texture_File_Path))[0]
        Texture_Name = os.path.basename(Texture_File_Path)

        # Save The OBJ File
        Output_OBJ = os.path.join(os.path.expanduser("~\\Downloads"), f"{Model_Name}.obj")
        Output_MTL = os.path.join(os.path.expanduser("~\\Downloads"), f"{Model_Name}.mtl")

        # Write To OBJ File
        self.Write_Object_Data_With_Textures(Vertices, Faces, UV_Coords, Output_OBJ, f"{Model_Name}.mtl")

        # Write To MTL File
        self.Write_MTL_Data(Output_MTL, Texture_Name)

    def Create_Object_Modal_Only_Model(self, Json_Data):

        # Extract Cubes From The JSON
        Geometry_Data = Json_Data.get('minecraft:geometry', [])

        Vertices = []
        Faces = []

        for Geometry in Geometry_Data:

            Bones = Geometry.get('bones', [])
            
            for Bone in Bones:

                # Extract Bone Collection Data
                Cubes = Bone.get('cubes', [])
                Bone_Pivot = Bone.get('pivot', [0, 0, 0])
                Bone_Rotation = Bone.get('rotation', [0, 0, 0])

                for Cube in Cubes:

                    Origin = Cube['origin']
                    Size = Cube['size']
                    Pivot = Cube.get('pivot', [0, 0, 0])
                    Rotation = Cube.get('rotation', [0, 0, 0])

                    # Calculate Cube Vertices
                    X, Y, Z = Origin
                    DX, DY, DZ = Size

                    Cube_Vertices = [
                        [X, Y, Z], [X + DX, Y, Z], [X + DX, Y + DY, Z], [X, Y + DY, Z],
                        [X, Y, Z + DZ], [X + DX, Y, Z + DZ], [X + DX, Y + DY, Z + DZ], [X, Y + DY, Z + DZ]
                    ]

                    def ApplyRotation(Vertices, Pivot, Rotation, Bone_Pivot, Bone_Rotation):

                        Rotated_Vertices = []
                        PX, PY, PZ = Pivot
                        BPX, BPY, BPZ = Bone_Pivot
                        RX, RY, RZ = [math.radians(Angle) for Angle in Rotation]
                        BRX, BRY, BRZ = [math.radians(Angle) for Angle in Bone_Rotation]

                        def Rotation_Matrix(X, Y, Z, Pivot_X, Pivot_Y, Pivot_Z, Rotation_X, Rotation_Y, Rotation_Z):

                            # Translate To Origin
                            X, Y, Z = X - Pivot_X, Y - Pivot_Y, Z - Pivot_Z

                            # Rotate X-Axis
                            Y, Z = Y * math.cos(-Rotation_X) - Z * math.sin(-Rotation_X), Y * math.sin(-Rotation_X) + Z * math.cos(-Rotation_X)

                            # Rotate Y-Axis
                            X, Z = X * math.cos(Rotation_Y) + Z * math.sin(Rotation_Y), -X * math.sin(Rotation_Y) + Z * math.cos(Rotation_Y)
                            
                            # Rotate Z-Axis
                            X, Y = X * math.cos(-Rotation_Z) - Y * math.sin(-Rotation_Z), X * math.sin(-Rotation_Z) + Y * math.cos(-Rotation_Z)

                            # Translate Back
                            return X + Pivot_X, Y + Pivot_Y, Z + Pivot_Z

                        for Vertex in Vertices:

                            X, Y, Z = Vertex

                            # Apply Cube Rotation
                            X, Y, Z = Rotation_Matrix(X, Y, Z, PX, PY, PZ, RX, RY, RZ)

                            # Apply Bone Rotation
                            X, Y, Z = Rotation_Matrix(X, Y, Z, BPX, BPY, BPZ, BRX, BRY, BRZ)

                            Rotated_Vertices.append([X, Y, Z])

                        return Rotated_Vertices

                    Rotated_Vertices = ApplyRotation(Cube_Vertices, Pivot, Rotation, Bone_Pivot, Bone_Rotation)

                    if self.X_Flip:

                        for Cubes in Rotated_Vertices:
                            Cubes[0] = Cubes[0] * -1

                    if self.Y_Flip:

                        for Cubes in Rotated_Vertices:
                            Cubes[1] = Cubes[1] * -1
                        
                    if self.Z_Flip:

                        for Cubes in Rotated_Vertices:
                            Cubes[2] = Cubes[2] * -1

                    # Add Cube Vertices To The Array
                    Vertex_Start = len(Vertices) + 1
                    Vertices.extend(Rotated_Vertices)

                    # Define Faces For The Cube (6 Faces, Each With 4 Vertices)
                    Cube_Faces = [
                        [Vertex_Start, Vertex_Start + 1, Vertex_Start + 2, Vertex_Start + 3],
                        [Vertex_Start + 4, Vertex_Start + 5, Vertex_Start + 6, Vertex_Start + 7],
                        [Vertex_Start, Vertex_Start + 4, Vertex_Start + 7, Vertex_Start + 3],
                        [Vertex_Start + 1, Vertex_Start + 5, Vertex_Start + 6, Vertex_Start + 2],
                        [Vertex_Start, Vertex_Start + 1, Vertex_Start + 5, Vertex_Start + 4],
                        [Vertex_Start + 3, Vertex_Start + 2, Vertex_Start + 6, Vertex_Start + 7]
                    ]

                    Faces.extend(Cube_Faces)

        Model_Name = "Converted_Model"

        # Save The OBJ File
        Output_OBJ = os.path.join(os.path.expanduser("~\\Downloads"), f"{Model_Name}.obj")

        # Write To OBJ File
        self.Write_Object_Data_Only_Modal(Vertices, Faces, Output_OBJ)

    def SearchDirectory(self):

        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        Common_User_Directories = ['Desktop', 'Downloads', 'Pictures', 'Documents', 'Music', 'Videos']
        self.User_Home = os.path.expanduser("~")

        def Common_Directory():

            for Common_Directories in Common_User_Directories:

                Common_Dir = os.path.join(self.User_Home, Common_Directories)

                for Root, Directory_Names, _ in os.walk(Common_Dir):

                    if self.DirectoryName in Directory_Names:
                        return os.path.join(Root, self.DirectoryName)
                    
            return None

        def Full_Search_Directory():

            Matches = []

            for Root, Directory_Names, _ in os.walk(self.InitialDirectory):

                if self.DirectoryName in Directory_Names:

                    Matches.append(os.path.join(Root, self.DirectoryName))

            return Matches

        def DirectoryPathfinding():

            InitialDirectoryTest = Common_Directory()

            if InitialDirectoryTest is None:
                return Full_Search_Directory()
            
            else:
                return [InitialDirectoryTest]

        Result = DirectoryPathfinding()

        return Result[0] if Result else None

def Main():
    JsonToObjectApp()

if __name__ == "__main__":
    Main()
