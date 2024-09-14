import json
from tkinter import Tk, filedialog
import os

class JsonToObjectApp():

    def __init__(self):
        super().__init__()

        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        Root = Tk()
        Root.withdraw()

        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        Root.iconbitmap(default=Icon_Path)

        # Get The JSON File
        Json_File_Path = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select A JSON File", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))

        Json_Data = self.Load_Json(Json_File_Path)

        if Json_Data:
            self.Create_Object_Modal(Json_Data)

    def Load_Json(self, File_Path):

        try:
            with open(File_Path, 'r') as File:
                return json.load(File)
            
        except Exception as e:
            return

    def Write_Object_Data(self, Vertices, Faces, File_Path):

        with open(File_Path, 'w') as File:

            for Vertex in Vertices:
                File.write(f"v {Vertex[0]} {Vertex[1]} {Vertex[2]}\n")

            for Face in Faces:
                File.write(f"f {' '.join(str(Index) for Index in Face)}\n")

    def Create_Object_Modal(self, Json_Data):

        # Extract Cubes From The JSON
        Cubes = Json_Data['minecraft:geometry'][0]['bones'][0]['cubes']

        Vertices = []
        Faces = []

        for Cube in Cubes:

            Origin = Cube['origin']
            Size = Cube['size']

            # Calculate Cube Vertices
            X, Y, Z = Origin
            DX, DY, DZ = Size

            Cube_Vertices = [
                [X, Y, Z], [X + DX, Y, Z], [X + DX, Y + DY, Z], [X, Y + DY, Z],
                [X, Y, Z + DZ], [X + DX, Y, Z + DZ], [X + DX, Y + DY, Z + DZ], [X, Y + DY, Z + DZ]
            ]

            # Add Cube Vertices To The Array
            Vertex_Start = len(Vertices) + 1
            Vertices.extend(Cube_Vertices)

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
        Output_File = os.path.join(os.path.expanduser("~\\Downloads"), f"{Model_Name}.obj")

        # Write To OBJ File
        self.Write_Object_Data(Vertices, Faces, Output_File)

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