import tkinter as tk
import tkinter.font as TkFont
from PIL import Image, ImageTk
import os
from subprocess import call
import ctypes as ct
import json
import uuid

# Constants
CURRENT_MINECRAFT_SERVER_STABLE_VERSION = "1.11.0"
CURRENT_MINECRAFT_SERVER_UI_STABLE_VERSION = "1.1.0"

# MasterCraft Screen
class ManifestGenerator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Getting User Pathway
        self.User_Home = os.path.expanduser("~")
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = os.path.normpath(f"{self.SearchDirectory()}")[2: -2]

        # Set Initial Window Size
        self.Screen_Width = self.winfo_screenwidth()
        self.Screen_Height = self.winfo_screenheight()
        self.geometry(f"{self.Screen_Width}x{self.Screen_Height}")

        # Set The Title Of The Window
        self.title("MasterCraft - Manifest Generator")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "IconImage.ico")
        self.iconbitmap(Icon_Image_Path)

        # Load The Initial Background Image
        BG_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Background.png")
        self.BG_Image = Image.open(BG_Image_Path)
        
        # Create A Label For The Background Image
        self.Background_Label = tk.Label(self)
        self.Background_Label.pack(fill="both", expand=True)

        # Creates A Button
        self.Create_Buttons()

        # Creates A Dropdown Menu
        self.Create_DropDown()

        # Creates Input Text
        self.Text_Entries()

        # Creates Title Bar Background
        self.Dark_Title_Bar()

        # Create The Background Mosaic
        self.Create_Background_Mosaic()
    
    # A Multi-Functional File Directory Tool To Find The MasterCraft
    def SearchDirectory(self):
        
        Common_User_Directories = ['Desktop', 'Downloads', 'Pictures', 'Documents', 'Music', 'Videos']

        def Common_Directory():

            for Common_Directories in Common_User_Directories:

                Common_Dir = os.path.join(self.User_Home, Common_Directories)

                for root, dirnames, _ in os.walk(Common_Dir):

                    if self.DirectoryName in dirnames:
                        return os.path.join(root, self.DirectoryName)
                    
            return None

        def Full_Search_Directory():

            matches = []

            for root, dirnames, _ in os.walk(self.InitialDirectory):

                if self.DirectoryName in dirnames:
                    matches.append(os.path.join(root, self.DirectoryName))

            return matches

        def DirectoryPathfinding():

            InitialDirectoryTest = Common_Directory()

            if InitialDirectoryTest is None:
                return Full_Search_Directory()
            else:
                return [InitialDirectoryTest]

        return DirectoryPathfinding()

    # A Function That Handles The Mosaic Background Creation
    def Create_Background_Mosaic(self):

        BG_Composite = Image.new('RGB', (self.Screen_Width, self.Screen_Height))
        Repeat_X = self.Screen_Width // self.BG_Image.width + 1
        Repeat_Y = self.Screen_Height // self.BG_Image.height + 1

        for Y in range(Repeat_Y):
            for X in range(Repeat_X):
                BG_Composite.paste(self.BG_Image, (X * self.BG_Image.width, Y * self.BG_Image.height))

        self.Background_Image = ImageTk.PhotoImage(BG_Composite)
        self.Background_Label.config(image=self.Background_Image)

    def Dark_Title_Bar(self):

        self.update()

        Set_Window_Attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        Get_Parent = ct.windll.user32.GetParent
        Hwnd = Get_Parent(self.winfo_id())
        Value = 2
        Value = ct.c_int(Value)
        Set_Window_Attribute(Hwnd, 20, ct.byref(Value), 4)

    # Function To Setup The Buttons
    def Create_Buttons(self):

        Button_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "ButtonBackground.png")
        Button_Hover_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "SelectedBackground.png")

        Button_Width = int(self.Screen_Width / 5)
        Button_Height = int(self.Screen_Height / 11)

        Button_Image = Image.open(Button_Image_Path).resize((Button_Width, Button_Height))
        Button_Hover_Image = Image.open(Button_Hover_Image_Path).resize((Button_Width, Button_Height))

        self.Button_Images = {
            'default': ImageTk.PhotoImage(Button_Image),
            'hover': ImageTk.PhotoImage(Button_Hover_Image)
        }

        Font = TkFont.Font(family="HP Simplified Jpan", size=16)

        BackButton = tk.Button(self, text="Back", image=self.Button_Images['default'], command=self.Return, compound="center", wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font=Font)
        BackButton.place(x=self.Screen_Width - Button_Width - 10, y=self.Screen_Height - 160)

        BackButton.bind("<Enter>", lambda event, b=BackButton: self.On_Enter(event, b, 'default'))
        BackButton.bind("<Leave>", lambda event, b=BackButton: self.On_Leave(event, b, 'default'))

        DownloadButton = tk.Button(self, text="Download RP And BP Manifest", image=self.Button_Images['default'], command=self.Download, compound="center", wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font=Font)
        DownloadButton.place(x=self.Screen_Width - Button_Width - 10, y=self.Screen_Height - 260)

        DownloadButton.bind("<Enter>", lambda event, b=DownloadButton: self.On_Enter(event, b, 'default'))
        DownloadButton.bind("<Leave>", lambda event, b=DownloadButton: self.On_Leave(event, b, 'default'))

    # A Function To Setup The Dropdown Menu
    def Create_DropDown(self):
        
        Font = TkFont.Font(family="HP Simplified Jpan", size=13)

        self.Manifest_Download_Label = tk.Label(self, text="Select Manifest Download Type:", font=Font)
        self.Manifest_Download_Label.place(x=1218, y=512)

        self.Mainfest_Download_Options = ["Mainfest BP & Manifest RP", "Mainfest BP", "Manifest RP"]
        self.Selected_Manifest_Download = tk.StringVar()
        self.Selected_Manifest_Download.set(self.Mainfest_Download_Options[0])

        self.Color_Dropdown = tk.OptionMenu(self, self.Selected_Manifest_Download, *self.Mainfest_Download_Options)
        self.Color_Dropdown.place(x=1218, y=550)

    def On_Enter(self, event, Button, state):
        if state == 'default':
            Button.config(image=self.Button_Images['hover'])

    def On_Leave(self, event, Button, state):
        if state == 'default':
            Button.config(image=self.Button_Images['default'])

    # A Function To Close This Window And Return To MasterCraft UI
    def Return(self):
        self.destroy()
        ReturnSequence()

    def Text_Entries(self):
        
        Font = TkFont.Font(family="Arial", size=12)

        self.Manifest_Title_Label = tk.Label(self, text="Addon Title:", font=Font)
        self.Manifest_Title_Label.place(x=10, y=30)       

        self.Text_Entry_Title = tk.Text(self, font=Font, height=1, width=50)
        self.Text_Entry_Title.place(x=10, y=60)

        self.Manifest_Description_Label = tk.Label(self, text="Addon Description:", font=Font)
        self.Manifest_Description_Label.place(x=10, y=100)

        self.Text_Entry_Description = tk.Text(self, font=Font, height=2, width=100)
        self.Text_Entry_Description.place(x=10, y=130)

        self.Manifest_Author_Label = tk.Label(self, text="Addon Author(s):", font=Font)
        self.Manifest_Author_Label.place(x=10, y=190)

        self.Text_Entry_Author = tk.Text(self, font=Font, height=1, width=100)
        self.Text_Entry_Author.place(x=10, y=220)

        self.Manifest_Minecraft_Server_Label = tk.Label(self, text="@minecraft/server Version:", font=Font)
        self.Manifest_Minecraft_Server_Label.place(x=10, y=260)

        self.Text_Entry_Minecraft_Server = tk.Text(self, font=Font, height=1, width=20)
        self.Text_Entry_Minecraft_Server.place(x=10, y=290)

        self.Manifest_Minecraft_Server_UI_Label = tk.Label(self, text="@minecraft/server-ui Version:", font=Font)
        self.Manifest_Minecraft_Server_UI_Label.place(x=10, y=330)

        self.Text_Entry_Minecraft_Server_UI = tk.Text(self, font=Font, height=1, width=20)
        self.Text_Entry_Minecraft_Server_UI.place(x=10, y=360)
    
    def Download(self):
        
        Manifest_Dropdown_Selected = self.Selected_Manifest_Download.get()

        Title = self.Text_Entry_Title.get("1.0", "end-1c")
        Description = self.Text_Entry_Description.get("1.0", "end-1c")
        Authors = self.Text_Entry_Author.get("1.0", "end-1c").split(',')
        Minecraft_Server = self.Text_Entry_Minecraft_Server.get("1.0", "end-1c") or CURRENT_MINECRAFT_SERVER_STABLE_VERSION
        Minecraft_Server_UI = self.Text_Entry_Minecraft_Server_UI.get("1.0", "end-1c") or CURRENT_MINECRAFT_SERVER_UI_STABLE_VERSION

        UUIDBPRPConnector = self.UUID_Genator()

        UUIDBP1 = self.UUID_Genator()
        UUIDBP2 = self.UUID_Genator()
        UUIDBP3 = self.UUID_Genator()

        UUIDRP1 = self.UUID_Genator()
        UUIDRP2 = self.UUID_Genator()

        Manifest_Data_BP = None
        Manifest_Data_RP = None

        if Manifest_Dropdown_Selected == "Mainfest BP & Manifest RP" or Manifest_Dropdown_Selected == "Mainfest BP":

            Manifest_Data_BP = {
                "format_version": 2,
                "metadata": {
                    "authors": Authors,
                },
                "header": {
                    "name": Title,
                    "description": Description,
                    "min_engine_version": [1, 21, 0],
                    "uuid": f'{UUIDBP1}',
                    "version": [1, 0, 0]
                },
                "modules": [
                    {
                        "type": "data",
                        "uuid": f'{UUIDBP2}',
                        "version": [1, 0, 0]
                    },
                    {
                        "type": "script",
                        "language": "javascript",
                        "uuid": f'{UUIDBP3}',
                        "entry": "scripts/main.js",
                        "version": [1, 0, 0]
                    }
                ],
                "dependencies": [
                    {
                        "uuid": f'{UUIDBPRPConnector}',
                        "version": [1, 0, 0]
                    },
                    {
                        "module_name": "@minecraft/server",
                        "version": Minecraft_Server
                    },
                    {
                        "module_name": "@minecraft/server-ui",
                        "version": Minecraft_Server_UI
                    }
                ]
            }

        if Manifest_Dropdown_Selected == "Mainfest BP & Manifest RP" or Manifest_Dropdown_Selected == "Mainfest RP":

            Manifest_Data_RP = {
                "format_version": 2,
                "metadata": {
                    "authors": Authors,
                },
                "header": {
                    "name": Title,
                    "description": Description,
                    "min_engine_version": [1, 21, 0],
                    "uuid": f'{UUIDRP1}',
                    "version": [1, 0, 0]
                },
                "modules": [
                    {
                        "type": "resources",
                        "uuid": f'{UUIDRP2}',
                        "version": [
                            1,
                            0,
                            0
                        ]
                    }
                ],
                "dependencies": [
                    {
                        "uuid": f'{UUIDBPRPConnector}',
                        "version": [1, 0, 0]
                    }
                ]
            }

        Downloads_Path = os.path.join(self.User_Home, "Downloads")
        Manifest_Folder_Path = os.path.join(Downloads_Path, "Manifest")
        os.makedirs(Manifest_Folder_Path, exist_ok=True)

        if Manifest_Data_BP is not None:

            Manifest_BP_Folder_Path = os.path.join(Downloads_Path, "Manifest", "BP")
            os.makedirs(Manifest_BP_Folder_Path, exist_ok=True)

            Manifest_BP_File_Path = os.path.join(Manifest_BP_Folder_Path, 'manifest.json')
            with open(Manifest_BP_File_Path, 'w') as f:
                json.dump(Manifest_Data_BP, f, indent=4)

        if Manifest_Data_RP is not None:

            Manifest_RP_Folder_Path = os.path.join(Downloads_Path, "Manifest", "RP")
            os.makedirs(Manifest_RP_Folder_Path, exist_ok=True)

            Manifest_RP_File_Path = os.path.join(Manifest_RP_Folder_Path, 'manifest.json')
            with open(Manifest_RP_File_Path, 'w') as f:
                json.dump(Manifest_Data_RP, f, indent=4)

    # Generates A Random UUID
    def UUID_Genator(self):

        return uuid.uuid4()
    
def ReturnSequence():

    # Getting User Pathway
    User_Home = os.path.expanduser("~")
    InitialDirectory = '/'
    DirectoryName = 'MasterCraft'

    def SearchDirectory():

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

    MasterCraftCurrentDirectory = os.path.normpath(SearchDirectory()[0])

    Script_Path = os.path.join(MasterCraftCurrentDirectory, "ScriptAPI", "MasterCraft_UI.py")
    call(["python", Script_Path])

def Main():
    App = ManifestGenerator()
    App.mainloop()

if __name__ == "__main__":
    Main()
