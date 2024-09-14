import os
import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from tkinter import filedialog
from tkextrafont import Font
from PIL import ImageTk, Image
import subprocess
import time
import pygame
import json
from pygame.locals import DOUBLEBUF, OPENGL, FULLSCREEN
from OpenGL.GL import glTranslatef, glRotatef, glClear, glBindTexture, glTexParameteri, glEnable, glBegin, glEnd, glDisable, glTexCoord2f, glPushMatrix, glPopMatrix, glLoadIdentity, glVertex3f, glBlendFunc, glTexImage2D, glGenTextures, glTexCoord2fv, glVertex3fv, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_RGB, GL_UNSIGNED_BYTE, GL_QUADS, GL_RGBA, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from OpenGL.GLU import gluPerspective

class PanoramaCreatorApp(tk.Tk):
        
    def __init__(self):
        super().__init__()

        # Maximizes The Window
        self.state("zoomed")
        
        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Setting The Current Setting To None
        self.Enable_Minecraft_Overlay_Setting = None
        self.Enable_Vsync_Setting = None
        self.Default_Rotation_Speed_Setting = None

        self.Vsync = None

        # Loads The Panorama Settings
        self.Load_Panorama_Menu_Settings()

        # Initialize Variables
        self.Initialize_Variables()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Loads The Checkbox Images
        self.Load_Checkbox_Images()

        # Creating Minecraft UI  
        self.Create_UI()

    def Initialize_Variables(self):

        self.Minecraft_Overlay_Variable = tk.BooleanVar(value=self.Enable_Minecraft_Overlay_Setting)
        self.Enable_Vsync_Variable = tk.BooleanVar(value=self.Enable_Vsync_Setting)
        self.Rotation_Speed_Entry = tk.StringVar(value=self.Default_Rotation_Speed_Setting)

    def Load_Panorama_Menu_Settings(self):

        Current_Settings_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Current_Settings.json")
        Default_Settings_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Default_Settings.json")

        with open(Current_Settings_Path, "r") as Current_File:
            self.Current_Settings = json.load(Current_File)

            if self.Current_Settings == {}:
                
                with open(Default_Settings_Path, "r") as Default_File:
                    self.Default_Settings = json.load(Default_File)

                    self.Current_Settings = self.Default_Settings
                    
                    with open(Current_Settings_Path, "w") as Updated_File:
                        json.dump(self.Current_Settings, Updated_File, indent=4)
        
        def Read_Panorama_Menu_Settings():

            Panorama_Settings = self.Current_Settings.get("Panorama Creator Menu", {})

            Enable_Minecraft_Overlay_Setting = Panorama_Settings["Enable Minecraft Overlay"]
            Enable_Vsync_Setting = Panorama_Settings["Enable Vsync"]
            Panorama_Rotation_Speed_Setting = Panorama_Settings["Default Rotation Speed"]

            return Enable_Minecraft_Overlay_Setting, Enable_Vsync_Setting, Panorama_Rotation_Speed_Setting

        self.Enable_Minecraft_Overlay_Setting, self.Enable_Vsync_Setting, self.Default_Rotation_Speed_Setting = Read_Panorama_Menu_Settings()

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
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Run Panorama"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Run Imported Minecraft Cubemap Panorama"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "CheckBox_Press"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back"),
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

    def Load_Checkbox_Images(self):
        
        Texture_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures")

        Checked_Image = Image.open(os.path.join(Texture_Directory, "CheckBox_Checked.png"))
        Unchecked_Image = Image.open(os.path.join(Texture_Directory, "CheckBox_Unchecked.png"))

        self.Checked_Image = ImageTk.PhotoImage(Checked_Image)
        self.Unchecked_Image = ImageTk.PhotoImage(Unchecked_Image)

    def Load_Overlay_Images(self, Image_Path):

        # Loads The Images And Perserves The Transparent Areas
        Image = pygame.image.load(Image_Path).convert_alpha()
        
        Image_Data = pygame.image.tostring(Image, "RGBA", 1)
        Width, Height = Image.get_size()

        Texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, Texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, Width, Height, 0, GL_RGBA, GL_UNSIGNED_BYTE, Image_Data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return Texture

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)
        
        if Sound:
            Sound.play()
    
    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Minecraft Panorama Creator")

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

        self.Frame = tk.Frame(self.Main_Frame, bg="#1E1E1E", bd=2, relief=tk.GROOVE)
        self.Frame.pack(fill="x", padx=10, pady=10)

        self.Create_Dropdown(self.Frame, self.Get_Panorama_Cubemap_Options())

        # Create Buttons
        self.Create_Buttons()

        # Create Input Text
        self.Create_Input_Fields()

    def Create_Header_Frame(self):

        Server_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Panorama_Creator.png")
        Server_Icon = ImageTk.PhotoImage(Image.open(Server_Icon_Path).resize((32, 32)))

        Header_Frame = tk.Frame(self, bg='#4C4C4C') 
        Header_Frame.pack(fill=tk.X)

        Icon_Label = tk.Label(Header_Frame, image=Server_Icon, bg='#4C4C4C')
        Icon_Label.image = Server_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="Minecraft Panorama Creator", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Checkboxes(self, Parent, Text, Variable, Identifer):

        Checkbox_Frame = tk.Frame(Parent, bg="#1E1E1E")
        Checkbox_Frame.pack(side=tk.LEFT)

        tk.Label(Checkbox_Frame, text="", width=2, bg="#1E1E1E").pack(side=tk.LEFT)

        Checkbox_Label = tk.Label(Checkbox_Frame, image=self.Unchecked_Image, bg="#1E1E1E")
        Checkbox_Label.pack(side=tk.LEFT)

        tk.Label(Checkbox_Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#1E1E1E", fg="white").pack(side=tk.LEFT)
    
        def Toggle_Checkbox():
            self.Play_Sound("CheckBox_Press")

            if Variable.get():

                Checkbox_Label.config(image=self.Unchecked_Image)
                Variable.set(False)
            else:

                Checkbox_Label.config(image=self.Checked_Image)
                Variable.set(True)

        def IntialLoad():
            
            if Variable.get():
                Checkbox_Label.config(image=self.Checked_Image)
            else:
                Checkbox_Label.config(image=self.Unchecked_Image)

        Checkbox_Frame.bind("<Button-1>", lambda e: Toggle_Checkbox())
        Checkbox_Label.bind("<Button-1>", lambda e: Toggle_Checkbox())

        # Set Initial State
        if Identifer == "Overlay":

            if self.Enable_Minecraft_Overlay_Setting:

                Variable.set(self.Enable_Minecraft_Overlay_Setting)
                Checkbox_Label.config(image=self.Checked_Image)
                IntialLoad()

            else:
                Variable.set(self.Enable_Minecraft_Overlay_Setting)
                Checkbox_Label.config(image=self.Unchecked_Image)
                IntialLoad()

        elif Identifer == "Vsync":
        
            if self.Enable_Vsync_Setting:
                print("s")
                Variable.set(self.Enable_Vsync_Setting)
                Checkbox_Label.config(image=self.Checked_Image)
                IntialLoad()

            else:
                Variable.set(self.Enable_Vsync_Setting)
                Checkbox_Label.config(image=self.Unchecked_Image)
                IntialLoad()

    # A Function To Setup The Dropdown Menu
    def Create_Dropdown(self, Parent, List):

        # Panorama Selection Dropdown
        self.Panorama_Var = tk.StringVar(value="Select A Panorama")
        Panorama_Options = List
        Panorama_Dropdown = tk.OptionMenu(Parent, self.Panorama_Var, *Panorama_Options)
        Panorama_Dropdown.config(bg="#2B2B2B", fg='white', font=self.Custom_Fonts["Minecraft Ten v2"], highlightbackground="#2B2B2B", activebackground="#4C4C4C")
        Panorama_Dropdown["menu"].config(bg="#2B2B2B", fg='white', font=self.Custom_Fonts["Minecraft Ten v2"], activebackground="#4C4C4C")
        Panorama_Dropdown.pack(side=tk.LEFT, padx=10, pady=10)

    def Create_Buttons(self):

        Buttons = [
            ("Run Panorama", self.Run_Panorama, "#1D6E02", "#2ca903", "#FFFFFF"),
            ("Run Imported Minecraft Cubemap Panorama", self.Run_Import_Panorama, "#1D6E02", "#2ca903", "#FFFFFF"),
            ("Back", self.Show_MasterCraftMainScreen, "#4C4C4C", "#2B2B2B", "#6C6C6C")
        ]
        
        for Text, Function, Color, Highlight_Color, Pressed_Color in Buttons:
            self.Add_Button(self.Frame, Text, Function, Color, Highlight_Color, Pressed_Color)

    def Create_Input_Fields(self):

        self.Create_Checkboxes(self.Frame, "Minecraft Overlay", self.Minecraft_Overlay_Variable, "Overlay")
        self.Create_Checkboxes(self.Frame, "Enable Vsync", self.Enable_Vsync_Variable, "Vsync")
        
        tk.Label(self.Frame, text="Rotation Speed:", font=self.Custom_Fonts["Minecraft Ten v2"], bg="#1E1E1E", fg="white").pack(anchor=tk.W, padx=60)
        self.Rotation_Speed_Entry = tk.Entry(self.Frame, textvariable=self.Rotation_Speed_Entry, font=self.Custom_Fonts["Minecraft Seven v2"], )
        self.Rotation_Speed_Entry.pack(side=tk.LEFT, padx=30)

    def Add_Button(self, Parent, Text, Function, Color, Highlight_Color, Pressed_Color):

        Button = tk.Button(Parent, text=Text, command=Function, bg=Color, fg='white', activebackground=Pressed_Color, font=self.Custom_Fonts["Minecraft Seven v2"])

        if Text == "Run Panorama":
            Button.pack(side=tk.LEFT, padx=5, pady=10)

        if Text == "Run Imported Minecraft Cubemap Panorama":
            Button.pack(side=tk.LEFT, padx=5, pady=10)

        if Text == "Back":
            Button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        Button.bind("<Enter>", lambda e: Button.config(bg=Highlight_Color))
        Button.bind("<Leave>", lambda e: Button.config(bg=Color))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)

    def Minecraft_Overlay(self):

        Minecraft_Logo_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Minecraft.png"))
        Minecraft_Play_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Play_Button.png"))
        Minecraft_Setting_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Button.png"))
        Minecraft_Marketplace_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Marketplace_Button.png"))
        Minecraft_Sign_In_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Sign_In_Button.png"))
        Minecraft_Achievement_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Achievement_Button.png"))
        Minecraft_Inbox_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Inbox_Button.png"))
        Minecraft_Dressing_Room_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Dressing_Room_Button.png"))
        Minecraft_Mojang_AB_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Mojang_AB.png"))
        Minecraft_Version_Texture = self.Load_Overlay_Images(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Version.png"))

        # Save The Current Matrix
        glPushMatrix()
        
        # Reset The Matrix To Identity (Cancel Out Any Rotations)
        glLoadIdentity()
        
        # Move Images Slightly In Front Of The Render Camera
        glTranslatef(0, 0, -1)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND) 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Render 2D Images
        def Image_Render(Image, LeftVertexCoordinate, RightVertexCoordinate, TopVertexCoordinate, BottomVertexCoordinate):

            glBindTexture(GL_TEXTURE_2D, Image)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex3f(LeftVertexCoordinate, TopVertexCoordinate, 0)     # Top Left
            glTexCoord2f(0, 0); glVertex3f(LeftVertexCoordinate, BottomVertexCoordinate, 0)  # Bottom Left
            glTexCoord2f(1, 0); glVertex3f(RightVertexCoordinate, BottomVertexCoordinate, 0) # Top Right
            glTexCoord2f(1, 1); glVertex3f(RightVertexCoordinate, TopVertexCoordinate, 0)    # Top Right
            glEnd()

        # Renders All The GUI Main Menu Images
        Image_Render(Minecraft_Logo_Texture, -0.555, 0.5475, 0.75, 0.25)
        Image_Render(Minecraft_Play_Texture, -0.307, 0.307, 0.1025, -0.1235)
        Image_Render(Minecraft_Setting_Texture, -0.307, 0.307, -0.1365, -0.3625)
        Image_Render(Minecraft_Marketplace_Texture, -0.307, 0.307, -0.3755, -0.6015)
        Image_Render(Minecraft_Sign_In_Texture, -0.98, -0.7975, -0.34125, -0.52875)
        Image_Render(Minecraft_Achievement_Texture, -0.98, -0.88, -0.595, -0.7725)
        Image_Render(Minecraft_Inbox_Texture, -0.851, -0.751, -0.595, -0.7725)
        Image_Render(Minecraft_Dressing_Room_Texture, 0.486, 0.829, -0.585, -0.7725)
        Image_Render(Minecraft_Mojang_AB_Texture, -1, -0.736, -0.91, -1)
        Image_Render(Minecraft_Version_Texture, 0.825, 1, -0.91, -1)

        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        # Restore The Original Matrix
        glPopMatrix()
      
    def Get_Panorama_Cubemap_Options(self):

        Panorama_Folder = os.path.join(self.MasterCraftCurrentDirectory, "App_Panorama_Cubemaps")
        return [File for File in os.listdir(Panorama_Folder) if os.path.isdir(os.path.join(Panorama_Folder, File))]

    def Run_Panorama(self):

        Selected_Panorama = self.Panorama_Var.get()

        if Selected_Panorama != "Select A Panorama":

            Panorama_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_Panorama_Cubemaps", Selected_Panorama)
            self.Display_Panorama(Panorama_Path)

            self.destroy()

    def Run_Import_Panorama(self):
        
        File_Path = filedialog.askdirectory()

        if not File_Path:
            return
        
        self.Display_Panorama(File_Path)

    def Display_Panorama(self, Panorama_Path):

        # Initialize Pygame
        pygame.init()

        # Get The User's Screen Resolution
        DisplayInfo = pygame.display.Info()
        Display = (DisplayInfo.current_w, DisplayInfo.current_h)

        # Load Images From The Provided Panorama Path
        Image_Files = [ImageFile for ImageFile in os.listdir(Panorama_Path) if ImageFile.startswith('panorama_') and ImageFile.endswith(('.png', '.jpg'))]
        Image_Files.sort()

        # Load Images From The Provided Panorama Path
        Images = [pygame.image.load(os.path.join(Panorama_Path, File)) for File in Image_Files]

        print(self.Enable_Vsync_Variable.get())
        if self.Enable_Vsync_Variable.get():
            self.Vsync = 1

        else:
            self.Vsync = 0

        # Set Up Display And Icon
        pygame.display.set_mode(Display, DOUBLEBUF | OPENGL | FULLSCREEN, vsync=int(self.Vsync))
        icon_path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        pygame.display.set_icon(pygame.image.load(icon_path))
        pygame.display.set_caption("Cubemap Panorama")

        # Set Up The Perspective With A Wider Field Of View For Panorama Effect
        gluPerspective(90, (Display[0] / Display[1]), 0.1, 100.0)

        # Place The Camera At The Center Of The Cube
        glTranslatef(0.0, 0.0, 0.0)

        # Rotate The Camera By 90 Degrees To Adjust The View
        glRotatef(90, 0, 1, 0)

        Textures = self.Load_Textures(Images)

        # Define The Rotation Speed
        Rotation_Speed = float(self.Rotation_Speed_Entry.get())

        if Rotation_Speed < 0:
            Rotation_Speed = 0

        Clock = pygame.time.Clock()

        while True:

            for Event in pygame.event.get():

                if Event.type == pygame.QUIT or (Event.type == pygame.KEYDOWN and Event.key == pygame.K_ESCAPE):  

                    Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "ScriptAPI", "MasterCraft_Panorama_Creator.py")
                    subprocess.Popen(["python", Script_Path])

                    time.sleep(0.2)
                    pygame.quit()
                    return

            # Rotates The Cube
            glRotatef(Rotation_Speed, 0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.Draw_Cube(Textures)

            if self.Minecraft_Overlay_Variable.get():
                self.Minecraft_Overlay()

            pygame.display.flip()
            Clock.tick(60)

    def Load_Textures(self, Images):

        Textures = []

        for Image in Images:

            Texture_Surface = pygame.image.tostring(Image, 'RGB', 1)
            Width, Height = Image.get_size()
            Texture = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, Texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Width, Height, 0, GL_RGB, GL_UNSIGNED_BYTE, Texture_Surface)
            Textures.append(Texture)

        return Textures

    def Draw_Cube(self, Textures):
        glEnable(GL_TEXTURE_2D)

        # Define Vertices For A Cube With Reversed Order For Inward Normals
        Vertices = [
            [ 1,  1, -1], [ 1, -1, -1], [ 1, -1,  1], [ 1,  1,  1],
            [-1,  1, -1], [-1, -1, -1], [-1, -1,  1], [-1,  1,  1]
        ]

        # Define Faces Using Vertices
        Faces = [
            (0, 1, 2, 3),  # Right
            (3, 2, 6, 7),  # Back
            (7, 6, 5, 4),  # Left
            (4, 5, 1, 0),  # Front
            (4, 0, 3, 7),  # Top
            (1, 5, 6, 2)   # Bottom
        ]

        # Define Texture Coordinates
        Texture_Coordinates = [
            (0, 1), (0, 0), (1, 0), (1, 1)
        ]

        for I, Face in enumerate(Faces):

            glBindTexture(GL_TEXTURE_2D, Textures[I])
            glBegin(GL_QUADS)

            for Coordinate, Vertex in enumerate(Face):

                glTexCoord2fv(Texture_Coordinates[Coordinate])
                glVertex3fv(Vertices[Vertex])

            glEnd()
        
        glDisable(GL_TEXTURE_2D)

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
    App = PanoramaCreatorApp()
    App.mainloop()

if __name__ == "__main__":
    Main()