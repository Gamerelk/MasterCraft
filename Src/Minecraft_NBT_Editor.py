import os
import tkinter as tk
import tkinter.font as TkFont
from tkinter import filedialog
from tkextrafont import Font
from PIL import ImageTk, Image
import subprocess
import time
import pygame
import json
import struct
    
class CustomNBTInterpreter:

    def __init__(self, File_Path):
        self.File_Path = File_Path

    def Read_NBT_Data(self):

        with open(self.File_Path, 'rb') as File:

            # Skip The Bedrock NBT Header (First 8 Bytes)
            File.read(8)
            return self.Parse_NBT(File)
        
    # Function To Parse NBT Structure
    def Parse_NBT(self, File):

        Tags = {}

        while True:

            # Read The Tag Type (1 Byte)
            Tag_Type = File.read(1)

            # End Of File Reached
            if len(Tag_Type) == 0:
                break

            # End Of Compound Tag
            if Tag_Type == b'\x00':
                break
            
            try:

                # Parse The Name Of The Tag (String With Length Prefix)
                Name_Length_Bytes = File.read(2)

                if len(Name_Length_Bytes) < 2:
                    break

                # Little-Endian Short
                Name_Length = struct.unpack('<H', Name_Length_Bytes)[0]
                Name = File.read(Name_Length).decode('utf-8')

            except struct.error as e:
                break
            
            # Parse The Tag Value Based On Its Type
            try:

                Value = self.Parse_Tag(Tag_Type, File)
                Tags[Name] = Value

            except Exception as e:
                break

        return Tags

    # Function To Parse Individual Tags Based On Tag Type And Return In A JSON-Like Structure
    def Parse_Tag(self, Tag_Type, File):

        # TAG_Byte (Read 1 Byte As A Signed Integer)
        if Tag_Type == b'\x01':  
            return struct.unpack('<b', File.read(1))[0] 
        
        # TAG_Short (Read 2 Bytes As Little-Endian Short)
        elif Tag_Type == b'\x02':
            return struct.unpack('<h', File.read(2))[0]
        
        # TAG_Int (Read 4 Bytes As Little-Endian Int)
        elif Tag_Type == b'\x03': 
            return struct.unpack('<i', File.read(4))[0]
        
        # TAG_Long (Read 8 Bytes As Little-Endian Long)
        elif Tag_Type == b'\x04':
            return struct.unpack('<q', File.read(8))[0]  
        
        # TAG_Float (Read 4 Bytes As Little-Endian Float)
        elif Tag_Type == b'\x05': 
            return struct.unpack('<f', File.read(4))[0]
        
        # TAG_Double (Read 8 Bytes As Little-Endian Double)
        elif Tag_Type == b'\x06':
            return struct.unpack('<d', File.read(8))[0]
        
        # TAG_String (Little-Endian Short For String Length)
        elif Tag_Type == b'\x08':

            Length = struct.unpack('<H', File.read(2))[0]  
            return File.read(Length).decode('utf-8')
        
        # TAG_List (Little-Endian Int For List Length)
        elif Tag_Type == b'\x09':  

            List_Type = File.read(1)  
            Length = struct.unpack('<i', File.read(4))[0] 
            return [self.Parse_Tag(List_Type, File) for _ in range(Length)] 

        # TAG_Compound (Recursively Parse Compound Tags)
        elif Tag_Type == b'\x0A':
            return self.Parse_NBT(File)
        
        # TAG_Int_Array (Little-Endian Int For Array Length)
        elif Tag_Type == b'\x0B':

            Length = struct.unpack('<i', File.read(4))[0] 
            return [struct.unpack('<i', File.read(4))[0] for _ in range(Length)]
        
        # TAG_Long_Array (Little-Endian Int For Array Length)
        elif Tag_Type == b'\x0C':  
            
            Length = struct.unpack('<i', File.read(4))[0] 
            return [struct.unpack('<q', File.read(8))[0] for _ in range(Length)]
        
        else:
            raise ValueError(f"Unknown Tag Type: {Tag_Type}")

class NBTEditorApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Maximizes The Window
        self.state("zoomed")
        
        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Creating Minecraft UI  
        self.Create_UI()

    def Load_Custom_Fonts(self):

        self.Custom_Fonts = {}
        Font_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Fonts")
        
        # List Of Custom Fonts
        Font_Paths = [
            (os.path.join(Font_Directory, "MinecraftTen.ttf"), "Minecraft Ten v2"),
            (os.path.join(Font_Directory, "MinecraftSeven.ttf"), "Minecraft Seven v2"),
        ]
        
        for Font_Path, Font_Name in Font_Paths:
            
            if Font_Name not in TkFont.families():

                Custom_Font = Font(file=Font_Path, family=Font_Name)
                self.Custom_Fonts[Font_Name] = Custom_Font

    def Load_Sounds(self):

        # Load In Pygames Library
        pygame.mixer.init()

        self.Sounds = {}
        Sound_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Sounds")

        # List Of Custom Counds
        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Setting"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Upload NBT Data"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back")
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)
        
        if Sound:
            Sound.play()
    
    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Minecraft NBT Editor")

        # Set The Main Window Color
        self.configure(bg="#3C3F41")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Image_Path)

        # Creates The Header Frame
        self.Create_Header_Frame()

        # Creates The Main Frame
        self.Main_Frame = tk.Frame(self, bg="#3C3F41")
        self.Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Buttons
        self.Create_Buttons()

    def Create_Header_Frame(self):

        Server_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "NBT_Editor.png")
        Server_Icon = ImageTk.PhotoImage(Image.open(Server_Icon_Path).resize((32, 32)))

        Header_Frame = tk.Frame(self, bg='#4C4C4C') 
        Header_Frame.pack(fill=tk.X)

        Icon_Label = tk.Label(Header_Frame, image=Server_Icon, bg='#4C4C4C')
        Icon_Label.image = Server_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="Minecraft NBT Editor", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Buttons(self):

        self.Button_Frame = tk.Frame(self.Main_Frame, bg="#1E1E1E", bd=2, relief=tk.GROOVE)
        self.Button_Frame.pack(fill="x", padx=10, pady=10)

        Buttons = [
            ("Upload NBT Data", self.ReadBedrockNBTData, "#1D6E02", "#2ca903", "#FFFFFF"),
            ("Back", self.Show_MasterCraftMainScreen, "#4C4C4C", "#2B2B2B", "#6C6C6C")
        ]

        for Text, Function, Color, Highlight_Color, Pressed_Color in Buttons:
            self.Add_Button(self.Button_Frame, Text, Function, Color, Highlight_Color, Pressed_Color)

    def Add_Button(self, Parent, Text, Function, Color, Highlight_Color, Pressed_Color):

        Button = tk.Button(Parent, text=Text, command=Function, bg=Color, fg='white', activebackground=Pressed_Color, font=self.Custom_Fonts["Minecraft Seven v2"])

        if Text == "Upload NBT Data":
            Button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        if Text == "Back":
            Button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        Button.bind("<Enter>", lambda e: Button.config(bg=Highlight_Color))
        Button.bind("<Leave>", lambda e: Button.config(bg=Color))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)

    def ReadBedrockNBTData(self):

        FilePath = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select A NBT File", filetypes=(("NBT Files", "*.nbt"), ("NBT Files", "*.dat"), ("NBT Files", "*.dat_old"), ("all files", "*.*")))

        if FilePath: 
            Parsed_NBT = CustomNBTInterpreter(FilePath).Read_NBT_Data()
            print(json.dumps(Parsed_NBT, indent=4))

    # A Function That Interacts With The Program Settings
    def Setting(self):

        self.Play_Sound("Setting")

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Setting.py")
        subprocess.Popen(["python", Script_Path])
        
    # A Function To Close This Window And Return To MasterCraft Main Screen
    def Show_MasterCraftMainScreen(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "MasterCraft_MainScreen.py")
        subprocess.Popen(["python", Script_Path])

        time.sleep(0.2)
        self.destroy()
        
    # Function That Finds MasterCraft Folder
    def SearchDirectory(self):

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
    App = NBTEditorApp()
    App.mainloop()

if __name__ == "__main__":
    Main()