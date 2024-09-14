from tkinter import Tk, filedialog, simpledialog
import trimesh
import numpy as np
import json
import os

class ObjectToJsonApp():

    def __init__(self):
        super().__init__()

        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        Root = Tk()
        Root.withdraw()

        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        Root.iconbitmap(default=Icon_Path)

        # Get The Object File
        Object_File_Path = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select A OBJ File", filetypes=(("OBJ files", "*.obj"), ("all files", "*.*")))

        Mesh = self.Load_Object(Object_File_Path)

        if Mesh is None:
            return

        # Ask For Model Up Or Down Scaling
        Scale_Factor = simpledialog.askfloat("Scale Factor", "Enter Scaling Factor (Model Size Range: 0.1-3):", minvalue=0.1, maxvalue=3.0)

        if Scale_Factor is None:
            return

        # Ask User For Voxel Size
        Voxel_Size = simpledialog.askfloat("Voxel Size", "Enter Voxel Size (Smaller For More Detail: Range 0.4-5):", minvalue=0.4, maxvalue=5.0)

        if Voxel_Size is None:
            return
    
        # Scale The Mesh
        Mesh.apply_scale(Scale_Factor)

        # Voxelize The Mesh
        Voxel_Matrix = self.Voxelize_Mesh(Mesh, Voxel_Size)

        # Merge Voxels Into Larger Cubes If Possible
        Merged_Voxel_Cubes = self.Merge_Voxels(Voxel_Matrix)

        Model_Name = "Converted_Model"

        Output_File = os.path.join(os.path.expanduser("~\\Downloads"), f"{Model_Name}.json")

        # Create Minecraft JSON Structure
        Minecraft_Json = self.Create_Minecraft_Json(Merged_Voxel_Cubes, Model_Name, Voxel_Size)

        # Save The JSON File
        Output_File = os.path.join(os.path.expanduser("~\\Downloads"), f"{Model_Name}.json")

        with open(Output_File, 'w') as f:
            json.dump(Minecraft_Json, f, indent=4)

        print(f"Number Of Cubes Generated: {len(Merged_Voxel_Cubes)}")

    def Load_Object(self, File_Path):

        try:
            Mesh = trimesh.load(File_Path)
            return Mesh
        
        except Exception as e:
            return 

    def Voxelize_Mesh(self, Mesh, Voxel_Size):

        Voxelized_Mesh = Mesh.voxelized(Voxel_Size)
        return Voxelized_Mesh.matrix

    def Merge_Voxels(self, Voxel_Matrix):

        Merged_Cubes = []
        Visited = np.zeros_like(Voxel_Matrix , dtype=bool)

        for X in range(Voxel_Matrix.shape[0]):
            for Y in range(Voxel_Matrix.shape[1]):
                for Z in range(Voxel_Matrix.shape[2]):

                    if Voxel_Matrix[X, Y, Z] and not Visited[X, Y, Z]:
                        Size_X = Size_Y = Size_Z = 1
                        
                        # X Expansion Priority, With Y, Z Expanding Booleans
                        Can_Expand_Y = True
                        Can_Expand_Z = True

                        # Expand In X Direction
                        while X + Size_X < Voxel_Matrix.shape[0] and Voxel_Matrix[X + Size_X, Y, Z] and not Visited[X + Size_X, Y, Z]:
                            Size_X += 1
                        
                        # Expand In Y Direction
                        while Can_Expand_Y and Y + Size_Y < Voxel_Matrix.shape[1]:

                            for DX in range(Size_X):

                                if not Voxel_Matrix[X + DX, Y + Size_Y, Z] or Visited[X + DX, Y + Size_Y, Z]:

                                    Can_Expand_Y = False
                                    break

                            if Can_Expand_Y:
                                Size_Y += 1
                        
                        # Expand In Z Direction
                        while Can_Expand_Z and Z + Size_Z < Voxel_Matrix.shape[2]:

                            for DX in range(Size_X):

                                for DY in range(Size_Y):

                                    if not Voxel_Matrix[X + DX, Y + DY, Z + Size_Z] or Visited[X + DX, Y + DY, Z + Size_Z]:

                                        Can_Expand_Z = False
                                        break

                                if not Can_Expand_Z:
                                    break
                                
                            if Can_Expand_Z:
                                Size_Z += 1
                        
                        # Mark All Voxels Cube As Visited
                        Visited[X: X + Size_X, Y: Y + Size_Y, Z: Z + Size_Z] = True
                        
                        Merged_Cubes.append(((X, Y, Z), (Size_X, Size_Y, Size_Z)))

        return Merged_Cubes

    def Create_Minecraft_Json(self, Cubes, Model_Name, Voxel_Size):

        Json_Cubes = []

        for Origin, Size in Cubes:

            Cube = {
                "origin": [Values * Voxel_Size for Values in Origin],
                "size": [Values * Voxel_Size for Values in Size],
                "uv": [0, 0]
            }

            Json_Cubes.append(Cube)

        Json_Structure = {

            "format_version": "1.20.80",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": f"geometry.{str(Model_Name).lower()}",
                        "texture_width": 16,
                        "texture_height": 16,
                        "visible_bounds_width": 2,
                        "visible_bounds_height": 2,
                        "visible_bounds_offset": [0, 0.5, 0]
                    },
                    "bones": [
                        {
                            "name": "Root",
                            "pivot": [0, 0, 0],
                            "cubes": Json_Cubes
                        }
                    ]
                }
            ]
        }

        return Json_Structure

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
    ObjectToJsonApp()

if __name__ == "__main__":
    Main()