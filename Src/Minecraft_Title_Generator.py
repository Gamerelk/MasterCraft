import os
import tkinter as tk
import tkinter.font as TkFont
from tkextrafont import Font
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageFilter
import subprocess
import time
import pygame
import json
import sys
import math

# Initialize Pygame
pygame.init()

class TitleGenerator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Maximizes The Window
        self.state("zoomed")
        
        # Getting User Pathway
        self.User_Home = os.path.expanduser("~")
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Setting The Current Setting To None
        self.Enable_Panorama_Setting = None
        self.Panorama_Background_Setting = None
        self.Panorama_Rotation_Setting = None

        # Loads The Font Settings
        self.Load_Font_Menu_Settings()

        # Load Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Initialize Variables
        self.Initialize_Variables()

        # Create UI
        self.Create_UI()

        self.Initialize_Pygame_Display()

    def Initialize_Variables(self):

        self.Selected_Font = tk.StringVar(value="Minecraft Regular")
        self.Selected_Color = tk.StringVar(value="Black")
        self.Selected_Border_Color = tk.StringVar(value="Black")
        self.Size_Entry = tk.StringVar(value="24")
        self.Border_Size_Entry = tk.StringVar(value="0")
        self.Z_Depth_Entry = tk.StringVar(value="10")
        self.Z_Depth_Direction = tk.StringVar(value="Down")
        self.X_Rotation = tk.DoubleVar(value=0)
        self.Y_Rotation = tk.DoubleVar(value=0)
        self.Z_Rotation = tk.DoubleVar(value=0)

    def Initialize_Pygame_Display(self):

        pygame.display.init()
        self.Pygame_Screen = pygame.display.set_mode((self.Preview_Canvas.winfo_width(), self.Preview_Canvas.winfo_height()), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.Update_Pygame()
        
    def Load_Font_Menu_Settings(self):

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
        
        def Read_Font_Menu_Settings():

            Font_Settings = self.Current_Settings.get("Font Menu", {})

            Enable_Panorama_Setting = Font_Settings["Enable Panorama Background"]
            Panorama_Background_Setting = Font_Settings["Default Panorama Background"]
            Panorama_Rotation_Speed_Setting = Font_Settings["Default Panorama Rotation Speed"]

            return Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting

        self.Enable_Panorama_Setting, self.Panorama_Background_Setting, self.Panorama_Rotation_Setting = Read_Font_Menu_Settings()

    def Load_Custom_Fonts(self):

        self.Custom_Fonts = {}
        self.Font_Paths = {} 
        Font_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_Generator_Fonts")
        
        Font_Paths = [
            (os.path.join(Font_Directory, "MinecraftRegular-Bmg3.ttf"), "Minecraft Regular"),
            (os.path.join(Font_Directory, "Minecraft Evenings.ttf"), "Minecraft Evenings"),
            (os.path.join(Font_Directory, "enchantment-proper.ttf"), "Enchantment Proper"),
            (os.path.join(Font_Directory, "Minecrafter.Reg.ttf"), "Minecrafter"),
            (os.path.join(Font_Directory, "Minecrafter.Alt.ttf"), "Minecrafter Alt"),
            (os.path.join(Font_Directory, "MinecraftSeven.ttf"), "Minecraft Seven v2"),
            (os.path.join(Font_Directory, "MinecraftTen.ttf"), "Minecraft Ten v2"),
        ]
        
        for Font_Path, Font_Name in Font_Paths:

            if Font_Name not in TkFont.families():

                Custom_Font = Font(file=Font_Path, family=Font_Name)

                self.Custom_Fonts[Font_Name] = Custom_Font
                self.Font_Paths[Font_Name] = Font_Path 

    def Load_Sounds(self):

        # Load In Pygames Library
        pygame.mixer.init()

        self.Sounds = {}
        Sound_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Sounds")

        # List Of Custom Sounds
        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Setting"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Update Preview"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Download"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Convert Font"),
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
        self.title("MasterCraft - Title Generator")

        # Set The Main Window Color
        self.configure(bg="#2B2B2B")

        # Set Window Icon
        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Path)

        # Functions To Load The Rest Of The UI
        self.Create_Header_Frame()
        self.Create_Main_Frame()
        self.Create_Font_Options()
        self.Create_Preview_Area()
        self.Create_Buttons()

    def Create_Header_Frame(self):

        Header_Frame = tk.Frame(self, bg='#4C4C4C')
        Header_Frame.pack(fill=tk.X)

        Font_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Title_Generator.png")
        Font_Icon = ImageTk.PhotoImage(Image.open(Font_Icon_Path).resize((32, 32)))

        Icon_Label = tk.Label(Header_Frame, image=Font_Icon, bg='#4C4C4C')
        Icon_Label.image = Font_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="TITLE GENERATOR", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Main_Frame(self):

        Main_Frame = tk.Frame(self, bg='#3C3F41')
        Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        Left_Panel = tk.Frame(Main_Frame, bg='#2B2B2B', bd=4, relief=tk.RAISED)
        Left_Panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        Right_Panel = tk.Frame(Main_Frame, bg='#2B2B2B', bd=4, relief=tk.RAISED)
        Right_Panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.Left_Panel = Left_Panel
        self.Right_Panel = Right_Panel

    def Create_Font_Options(self):

        Font_Options = [
            ("Font Type", self.Selected_Font, self.Custom_Fonts.keys()),
            ("Font Color", self.Selected_Color, ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple"]),
            ("Border Color", self.Selected_Border_Color, ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Brown", "Pink", "White", "Gray", "Magenta"]),
            ("Z-Depth Direction", self.Z_Depth_Direction, ["Up", "Down", "Left", "Right"])
        ]

        for Text, Variable, Values in Font_Options:

            Frame = tk.Frame(self.Left_Panel, bg='#2B2B2B')
            Frame.pack(fill=tk.X, padx=5, pady=5)

            Label = tk.Label(Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#2B2B2B', fg='white')
            Label.pack(anchor='w')

            Dropdown = tk.OptionMenu(Frame, Variable, *Values)
            Dropdown.config(bg="#2B2B2B", fg='white', font=self.Custom_Fonts["Minecraft Seven v2"], highlightbackground="#2B2B2B", activebackground="#4C4C4C")
            Dropdown["menu"].config(bg="#2B2B2B", fg='white', font=self.Custom_Fonts["Minecraft Seven v2"], activebackground="#4C4C4C")
            Dropdown.pack(fill=tk.X)

        Entries = [
            ("Font Size", self.Size_Entry),
            ("Border Size", self.Border_Size_Entry),
            ("Z-Depth", self.Z_Depth_Entry)
        ]

        for Text, Entry in Entries:
            
            Frame = tk.Frame(self.Left_Panel, bg='#2B2B2B')
            Frame.pack(fill=tk.X, padx=5, pady=5)

            Label = tk.Label(Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#2B2B2B', fg='white')
            Label.pack(anchor='w')

            Entry_Widget = tk.Entry(Frame, textvariable=Entry, bg='#4C4C4C', fg='white')
            Entry_Widget.pack(fill=tk.X)

        Sliders = [
            ("X Rotation", self.X_Rotation, (-180, 180, 1)),
            ("Y Rotation", self.Y_Rotation, (-180, 180, 1)),
            ("Z Rotation", self.Z_Rotation, (-180, 180, 1))
        ]

        for Text, Variable, Range in Sliders:

            Frame = tk.Frame(self.Left_Panel, bg='#2B2B2B')
            Frame.pack(fill=tk.X, padx=5, pady=5)

            Label = tk.Label(Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#2B2B2B', fg='white')
            Label.pack(anchor='w')

            Slider = tk.Scale(Frame, from_=Range[0], to=Range[1], resolution=Range[2], orient=tk.HORIZONTAL, variable=Variable, bg="#3C3F41", fg="white", troughcolor="#1E1E1E", highlightbackground="#2B2B2B", font=self.Custom_Fonts["Minecraft Seven v2"])
            Slider.pack(fill=tk.X)

    def Create_Preview_Area(self):

        Preview_Label = tk.Label(self.Right_Panel, text="Preview", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#2B2B2B', fg='white')
        Preview_Label.pack(pady=10)

        self.Preview_Canvas = tk.Canvas(self.Right_Panel, bg='#3C3F41', highlightthickness=0)
        self.Preview_Canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pygame Embedding
        os.environ['SDL_WINDOWID'] = str(self.Preview_Canvas.winfo_id())
        
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'


        self.Text_Entry = tk.Entry(self.Right_Panel, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white')
        self.Text_Entry.pack(fill=tk.X, padx=10, pady=10)

    def Create_Buttons(self):

        Buttons = [
            ("Download", self.Download_Image),
            ("Back", self.Show_MasterCraftMainScreen)
        ]

        for Text, Function in Buttons:
            self.Add_Button(self.Left_Panel, Text, Function)

    def Add_Button(self, Parent, Text, Function):

        Button = tk.Button(Parent, text=Text, command=Function, bg='#4C4C4C', fg='white', activebackground='#6C6C6C', activeforeground='white', font=self.Custom_Fonts["Minecraft Seven v2"])
        Button.pack(fill=tk.X, padx=5, pady=5)
        
        Button.bind("<Enter>", lambda e: Button.config(bg='#2B2B2B'))
        Button.bind("<Leave>", lambda e: Button.config(bg='#4C4C4C'))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))
    
    # A Function That Runs Code When the Button Is Pressed
    def On_Button_Click(self, Button_Text):
        
        self.Play_Sound(Button_Text)

    def Update_Pygame(self):

        Font_Path = self.Font_Paths.get(self.Selected_Font.get())
        Font_Size = int(self.Size_Entry.get()) if self.Size_Entry.get().isdigit() and int(self.Size_Entry.get()) > 1 else 1
        Font_Border_Size = int(self.Border_Size_Entry.get()) if self.Border_Size_Entry.get().isdigit() and int(self.Border_Size_Entry.get()) > 1 else 1
        Font_Color = self.Selected_Color.get()
        Font_Border_Color = self.Selected_Border_Color.get()
        Z_Depth = int(self.Z_Depth_Entry.get()) if self.Z_Depth_Entry.get().isdigit() and int(self.Z_Depth_Entry.get()) > 0 else 0

        Font = pygame.font.Font(Font_Path, Font_Size)

        # Clear The Screen
        self.Pygame_Screen.fill((255, 255, 255))

        # Render Text
        User_Text = self.Text_Entry.get()
        Text_Surface = Font.render(User_Text, True, pygame.Color(Font_Color))
        Text_Rotated_Surface = self.Rotate_Surface(Text_Surface, self.X_Rotation.get(), self.Y_Rotation.get(), self.Z_Rotation.get())
        Text_Rectangle = Text_Rotated_Surface.get_rect(center=(self.Pygame_Screen.get_width() // 2, self.Pygame_Screen.get_height() // 2))
        self.Pygame_Screen.blit(Text_Rotated_Surface, Text_Rectangle)

        # Render The 3D Effect
        for Z in range(Z_Depth):

            # Calculate The Shade Of The Border Color Based On The Current Depth Layer
            Depth_Value = int(Z * (200 / Z_Depth))
            Depth_Color = (Depth_Value, Depth_Value, Depth_Value)

            # Create the text surface with the current shade
            Depth_Surface = Font.render(User_Text, True, Depth_Color)
            Depth_Rotated_Surface = self.Rotate_Surface(Depth_Surface, self.X_Rotation.get(), self.Y_Rotation.get(), self.Z_Rotation.get())

            if self.Z_Depth_Direction.get() == "Up":
                Offset_X, Offset_Y = Z, -Z
            
            elif self.Z_Depth_Direction.get() == "Down":
                Offset_X, Offset_Y = Z, Z

            elif self.Z_Depth_Direction.get() == "Left":
                Offset_X, Offset_Y = -Z, 0

            elif self.Z_Depth_Direction.get() == "Right":
                Offset_X, Offset_Y = Z, 0

            Depth_Rectangle = Depth_Rotated_Surface.get_rect(center=(self.Pygame_Screen.get_width() // 2 + Offset_X, self.Pygame_Screen.get_height() // 2 + Offset_Y))
            
            # Blit The Current Layer
            self.Pygame_Screen.blit(Depth_Rotated_Surface, Depth_Rectangle)
            
        # Draw Border If Specified
        if Font_Border_Size > 0:

            if Font_Border_Size > 50:
                Font_Border_Size = 50
            
            Border_Surface = Font.render(User_Text, True, pygame.Color(Font_Border_Color))
            Border_Rotated_Surface = self.Rotate_Surface(Border_Surface, self.X_Rotation.get(), self.Y_Rotation.get(), self.Z_Rotation.get())

            for DX in range(-Font_Border_Size, Font_Border_Size + 1):
                for DY in range(-Font_Border_Size, Font_Border_Size + 1):

                    if DX != 0 or DY != 0:
                        self.Pygame_Screen.blit(Border_Rotated_Surface, Text_Rectangle.move(DX, DY))

        self.Pygame_Screen.blit(Text_Rotated_Surface, Text_Rectangle)

        pygame.display.flip() 
        self.after(40, self.Update_Pygame)

    def Rotate_Surface(self, Surface, X_Angle, Y_Angle, Z_Angle):
            
            # Convert Angles To Radians
            X_Radian = math.radians(X_Angle)
            Y_Radian = math.radians(Y_Angle)
            Z_Radian = math.radians(Z_Angle)

            # Get The Original Dimensions
            Width, Height = Surface.get_size()

            # Create A New Surface With An Alpha Channel
            Rotated = pygame.Surface((Width * 2, Height * 2), pygame.SRCALPHA)

            # Rotation Matrices
            def Rotate_X(X, Y, Z):
                return X, Y * math.cos(X_Radian) - Z * math.sin(X_Radian), Y * math.sin(X_Radian) + Z * math.cos(X_Radian)

            def Rotate_Y(X, Y, Z):
                return Z * math.sin(Y_Radian) + X * math.cos(Y_Radian), Y, Z * math.cos(Y_Radian) - X * math.sin(Y_Radian)

            def Rotate_Z(X, Y, Z):
                return X * math.cos(Z_Radian) - Y * math.sin(Z_Radian), X * math.sin(Z_Radian) + Y * math.cos(Z_Radian), Z

            # Apply Rotation To Each Pixel
            for X in range(Width):
                for Y in range(Height):

                    RX, RY, RZ = Rotate_X(X - Width / 2, Y - Height / 2, 0)
                    RX, RY, RZ = Rotate_Y(RX, RY, RZ)
                    RX, RY, RZ = Rotate_Z(RX, RY, RZ)
                    
                    RX, RY = int(RX + Width), int(RY + Height)
                    
                    if 0 <= RX < Width * 2 and 0 <= RY < Height * 2:
                        Rotated.set_at((RX, RY), Surface.get_at((X, Y)))

            return Rotated

    def Download_Image(self):

        User_Text = self.Text_Entry.get()
        Selected_Font = self.Selected_Font.get()
        
        try:
            Selected_Size = int(self.Size_Entry.get())
        except ValueError:
            Selected_Size = 24
        
        Selected_Color = self.Selected_Color.get().lower()
        
        try:
            Border_Size = int(self.Border_Size_Entry.get())
        except ValueError:
            Border_Size = 0
        
        Border_Color = self.Selected_Border_Color.get().lower()

        # Use The Stored Font Path
        Font_Path = self.Font_Paths.get(Selected_Font)

        if not Font_Path:
            return

        # Create A Temporary Font To Measure Text Dimensions
        Temporary_Font = ImageFont.truetype(Font_Path, Selected_Size)
        
        # Get The Text And Use The Bounding Box Function
        Left, Top, Right, Bottom = Temporary_Font.getbbox(User_Text)
        Text_Width = Right - Left
        Text_Height = Bottom - Top

        # Create A New Image With RGBA Mode
        Image_Width = Text_Width + 2 * Border_Size + 4
        Image_Height = Text_Height + 2 * Border_Size + 4
        Download_Image = Image.new("RGBA", (Image_Width, Image_Height), (255, 255, 255, 0))
        
        # Create A Drawing Of The Image
        Draw = ImageDraw.Draw(Download_Image)

        # Draw The Border
        if Border_Size > 0:

            for DX in range(-Border_Size, Border_Size + 1):

                for DY in range(-Border_Size, Border_Size + 1):

                    if DX != 0 or DY != 0:
                        Draw.text((Border_Size + 2 + DX, Border_Size + 2 + DY), User_Text, font=Temporary_Font, fill=Border_Color)

        # Draw The Main Text
        Draw.text((Border_Size + 2, Border_Size + 2), User_Text, font=Temporary_Font, fill=Selected_Color)

        # Save The Image
        Downloads_Folder = os.path.join(self.User_Home, "Downloads")
        Output_Image_Path = os.path.join(Downloads_Folder, "Font_Preview.png")
        Download_Image.save(Output_Image_Path)

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
    app = TitleGenerator()
    app.mainloop()

if __name__ == "__main__":
    Main()