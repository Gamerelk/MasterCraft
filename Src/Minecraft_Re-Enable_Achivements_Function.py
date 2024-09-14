import os
from tkinter import Tk, filedialog
import shutil

class WorldReEnableCheatsApp():

    def __init__(self):
        super().__init__()

        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        MinecraftWorldsDirectory = os.path.join(os.path.expanduser('~'), "AppData", "Local", "Packages", "Microsoft.MinecraftUWP_8wekyb3d8bbwe", "LocalState", "games", "com.mojang", "minecraftWorlds")

        Root = Tk()
        Root.withdraw()
        
        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        Root.iconbitmap(Icon_Path)
        
        LevelDat = filedialog.askopenfilename(initialdir=os.path.expanduser(MinecraftWorldsDirectory), title="Select Level", filetypes=(("Minecraft World Dat File", "*level.dat"), ("all files", "*.*")))

        if LevelDat:

            Replacement_File = os.path.join(self.MasterCraftCurrentDirectory, "App_Re-Enable_Cheat_File", "level.dat")

            if Replacement_File:

                shutil.copy(Replacement_File, LevelDat)

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
    WorldReEnableCheatsApp()

if __name__ == "__main__":
    Main()