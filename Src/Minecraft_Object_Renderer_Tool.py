import os
import tkinter as tk
from tkinter import filedialog
import tkinter.font as TkFont
from tkextrafont import Font
from PIL import ImageTk, Image
import subprocess
import time
import pygame as pg
import numpy as np
import math
import sys
import keyboard

# Utility functions
def Any_Function(Array, A, B):
    return np.any((Array == A) | (Array == B))

# Classes
class Object_Utilities:

    def Translate(Position):

        Translate_X, Translate_Y, Translate_Z = Position
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [Translate_X, Translate_Y, Translate_Z, 1]])

    def Rotate_X(Angle):
        return np.array([[1, 0, 0, 0], [0, math.cos(Angle), math.sin(Angle), 0], [0, -math.sin(Angle), math.cos(Angle), 0], [0, 0, 0, 1]])

    def Rotate_Y(Angle):
        return np.array([[math.cos(Angle), 0, -math.sin(Angle), 0], [0, 1, 0, 0], [math.sin(Angle), 0, math.cos(Angle), 0], [0, 0, 0, 1]])

    def Rotate_Z(Angle): 
        return np.array([[math.cos(Angle), math.sin(Angle), 0, 0], [-math.sin(Angle), math.cos(Angle), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    def Scale(Value):
        return np.array([[Value, 0, 0, 0], [0, Value, 0, 0], [0, 0, Value, 0], [0, 0, 0, 1]])

class Object3D:

    def __init__(self, Render, Vertices, Faces, Color_Faces, Rotation):

        self.Render = Render
        self.Vertices = np.array([np.array(V) for V in Vertices])
        self.Faces = Faces
        self.Color_Faces = Color_Faces
        self.Font = pg.font.SysFont('Arial', 30, bold=True)
        self.Color_Faces = [(pg.Color('orange'), Face) for Face in self.Faces]
        self.Movement_Flag, self.Draw_Vertices = True, False
        self.Automatic_Rotation = Rotation
        self.Label = ''
        self.Transform_Matrix = np.eye(4)
        
    def Draw_Object_To_Display(self):

        self.Screen_Projection()
        self.Movement()

    def Update_Rotation(self, Rotation_State):
        self.Automatic_Rotation = Rotation_State

    def Movement(self):

        if self.Movement_Flag and self.Automatic_Rotation:
            self.Rotate_Y(-(pg.time.get_ticks() % 0.005))

    def Screen_Projection(self):

        Vertices = self.Vertices @ self.Transform_Matrix @ self.Render.Camera.Camera_Matrix()
        Vertices = Vertices @ self.Render.Projection.Projection_Matrix()
        Vertices /= Vertices[:, -1].reshape(-1, 1)
        Vertices[(Vertices > 2) | (Vertices < -2)] = 0
        Vertices = Vertices @ self.Render.Projection.To_Screen_Matrix
        Vertices = Vertices[:, :2]

        for Index, Color_Face in enumerate(self.Color_Faces):

            Color, Face = Color_Face
            Polygon = Vertices[Face]

            if not Any_Function(Polygon, self.Render.H_WIDTH, self.Render.H_HEIGHT):

                pg.draw.polygon(self.Render.Screen, Color, Polygon, 1)

                if self.Label:

                    Text = self.Font.render(self.Label[Index], True, pg.Color('white'))
                    self.Render.Screen.blit(Text, Polygon[-1])

        if self.Draw_Vertices:

            for Vertex in Vertices:

                if not Any_Function(Vertex, self.Render.H_WIDTH, self.Render.H_HEIGHT):
                    pg.draw.circle(self.Render.Screen, pg.Color('white'), Vertex, 2)

    def Translate(self, Position):
        self.Transform_Matrix = self.Transform_Matrix @ Object_Utilities.Translate(Position)

    def Scale(self, Value):
        self.Transform_Matrix = self.Transform_Matrix @ Object_Utilities.Scale(Value)

    def Rotate_X(self, Angle):
        self.Transform_Matrix = self.Transform_Matrix @ Object_Utilities.Rotate_X(Angle)

    def Rotate_Y(self, Angle):
        self.Transform_Matrix = self.Transform_Matrix @ Object_Utilities.Rotate_Y(Angle)

    def Rotate_Z(self, Angle):
        self.Transform_Matrix = self.Transform_Matrix @ Object_Utilities.Rotate_Z(Angle)

class Camera:

    def __init__(self, Render, Position):

        self.Render = Render
        self.Position = np.array([*Position, 1.0])
        self.Forward = np.array([0, 0, 1, 1])
        self.Backward = np.array([0, 0, 1, 1])
        self.Up = np.array([0, 1, 0, 1])
        self.Right = np.array([1, 0, 0, 1])
        self.Horizontal_Field_Of_View = math.pi / 3
        self.Vertical_Field_Of_View = self.Horizontal_Field_Of_View * (Render.HEIGHT / Render.WIDTH)
        self.Near_Plane = 0.1
        self.Far_Plane = 100
        self.Moving_Speed = 0.3
        self.Rotation_Speed = 0.015
        self.Zoom_Speed = 0.1
        self.Zoom_Factor = 1.0
        self.Min_Zoom = 0.1
        self.Max_Zoom = 5.0
        self.Minimum_Zoom_Limit = 0
        self.Maximum_Zoom_Limit = 20
        self.Zoom_Current = 5

        self.Angle_Pitch = 0
        self.Angle_Yaw = 0
        self.Angle_Roll = 0

        self.Dragging = False
        self.Last_Mouse_Position = None
        
    def Control(self):

        if keyboard.is_pressed('a'):  self.Position -= self.Right * self.Moving_Speed
        if keyboard.is_pressed('d'): self.Position += self.Right * self.Moving_Speed
        if keyboard.is_pressed('w'): self.Position += self.Backward * self.Moving_Speed
        if keyboard.is_pressed('s'): self.Position -= self.Forward * self.Moving_Speed
        if keyboard.is_pressed('space_bar'): self.Position += self.Up * self.Moving_Speed
        if keyboard.is_pressed('shift'): self.Position -= self.Up * self.Moving_Speed
        if keyboard.is_pressed('left'): self.Camera_Yaw(-self.Rotation_Speed)
        if keyboard.is_pressed('right'): self.Camera_Yaw(self.Rotation_Speed)
        if keyboard.is_pressed('up'): self.Camera_Pitch(-self.Rotation_Speed)
        if keyboard.is_pressed('down'): self.Camera_Pitch(self.Rotation_Speed)
        
        for Event in pg.event.get():

            if Event.type == pg.MOUSEWHEEL:
                
                Mouse = Event.y
                Mouse_Wheel = 0

                if Mouse >= 0 and self.Zoom_Current < self.Maximum_Zoom_Limit:

                    Mouse_Wheel = -1
                    self.Zoom_Current = self.Zoom_Current + 1
                
                if Mouse <= 0 and self.Zoom_Current > self.Minimum_Zoom_Limit:

                    Mouse_Wheel = 1
                    self.Zoom_Current = self.Zoom_Current - 1

                self.Zoom(Mouse_Wheel * self.Zoom_Speed)

        Mouse_Position = pg.mouse.get_pos()

        if pg.mouse.get_pressed()[0]:

            if not self.Dragging:
                self.Dragging = True
                self.Last_Mouse_Position = Mouse_Position

            else:
                X, Y = Mouse_Position[0] - self.Last_Mouse_Position[0], Mouse_Position[1] - self.Last_Mouse_Position[1]
                self.Camera_Yaw(-X * 0.003)
                self.Camera_Pitch(-Y * 0.003)
                self.Last_Mouse_Position = Mouse_Position

        else:
            self.Dragging = False
            self.Last_Mouse_Position = None

    def Zoom(self, amount):

        self.Zoom_Factor = max(self.Min_Zoom, min(self.Max_Zoom, self.Zoom_Factor - amount))
        self.Update_Projection()

    def Camera_Yaw(self, angle):
        self.Angle_Yaw += angle

    def Camera_Pitch(self, angle):
        self.Angle_Pitch += angle

    def AxisIdentity(self):

        self.Forward = np.array([0, 0, 1, 1])
        self.Up = np.array([0, 1, 0, 1])
        self.Right = np.array([1, 0, 0, 1])

    def Camera_Update_Axis(self):

        Rotate = Object_Utilities.Rotate_X(self.Angle_Pitch) @ Object_Utilities.Rotate_Y(self.Angle_Yaw)
        self.AxisIdentity()
        self.Forward = self.Forward @ Rotate
        self.Right = self.Right @ Rotate
        self.Up = self.Up @ Rotate

    def Update_Projection(self):

        self.Horizontal_Field_Of_View = (math.pi / 3) / self.Zoom_Factor
        self.Vertical_Field_Of_View = self.Horizontal_Field_Of_View * (self.Render.HEIGHT / self.Render.WIDTH)
        self.Near_Plane = 0.1
        self.Far_Plane = 100
        self.Render.Projection = Projection(self.Render)

    def Camera_Matrix(self):

        self.Camera_Update_Axis()
        return self.Translate_Matrix() @ self.Rotate_Matrix()

    def Translate_Matrix(self):

        X, Y, Z, W = self.Position
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-X, -Y, -Z, 1]])

    def Rotate_Matrix(self):

        Right_X, Right_Y, Right_Z, W = self.Right
        Forward_X, Forward_Y, Forward_Z, W = self.Forward
        Up_X, Up_Y, Up_Z, W = self.Up

        return np.array([[Right_X, Up_X, Forward_X, 0], [Right_Y, Up_Y, Forward_Y, 0], [Right_Z, Up_Z, Forward_Z, 0], [0, 0, 0, 1]])

class Axes(Object3D):

    def __init__(self, Render):
        super().__init__(Render)

        self.Vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.Faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.Colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.Color_Faces = [(Color, Face) for Color, Face in zip(self.Colors, self.Faces)]
        self.Draw_Vertices = False
        self.Label = 'XYZ'

class Projection:

    def __init__(self, Render):

        self.Render = Render
        NEAR = self.Render.Camera.Near_Plane
        FAR = self.Render.Camera.Far_Plane
        RIGHT = math.tan(self.Render.Camera.Horizontal_Field_Of_View / 2)
        LEFT = -RIGHT
        TOP = math.tan(self.Render.Camera.Vertical_Field_Of_View / 2)
        BOTTOM = -TOP

        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)

        self.Projection_Matrix_Value = np.array([[m00, 0, 0, 0], [0, m11, 0, 0], [0, 0, m22, 1], [0, 0, m32, 0]])

        HW, HH = Render.H_WIDTH, Render.H_HEIGHT
        self.To_Screen_Matrix = np.array([[HW, 0, 0, 0], [0, -HH, 0, 0], [0, 0, 1, 0], [HW, HH, 0, 1]])

    def Projection_Matrix(self):
        return self.Projection_Matrix_Value
    
class SoftwareRender:

    def __init__(self, Width, Height, Vsync):

        pg.init()

        self.RESOLUTION = self.WIDTH, self.HEIGHT = Width, Height
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.Screen = pg.display.set_mode(self.RESOLUTION, vsync=Vsync)
        self.Clock = pg.time.Clock()
        self.Create_Objects()
        self.FPS = 0
        self.FPS_Font = pg.font.SysFont('Arial', 20)
        self.Frame_Count = 0
        self.Last_Time = time.time()

    def Import_Object(self, File):
        self.Object = self.Get_Object_From_File(File)

    def Create_Objects(self):
        
        self.Automatic_Rotation = False
        self.Rotation_X = 0
        self.Rotation_Y = 0
        self.Rotation_Z = 0
        self.Camera = Camera(self, [-5, 6, -55])
        self.Projection = Projection(self)
        self.Object = None

        if self.Object == None:
            return
        
        if self.Automatic_Rotation == True:
            self.Object.Rotate_Y(-math.pi / 4)

    def Get_Object_From_File(self, Filename):

        Vertex, Faces = [], []

        with open(Filename) as File:

            for Line in File:

                if Line.startswith('v '):
                    Vertex.append([float(I) for I in Line.split()[1:]] + [1])

                elif Line.startswith('f'):
                    Object_Faces = Line.split()[1:]
                    Faces.append([int(Face.split('/')[0]) - 1 for Face in Object_Faces])

        return Object3D(self, Vertex, Faces, "Orange", self.Automatic_Rotation)

    def Update_Rotation(self, Rotation_State):

        self.Automatic_Rotation = Rotation_State

        if self.Object:
            self.Object.Update_Rotation(Rotation_State)

    def Draw(self):

        if self.Object == None:
            return

        self.Screen.fill(pg.Color('darkslategray'))
        self.Object.Draw_Object_To_Display()

        self.Frame_Count += 1
        Current_Time = time.time()

        if Current_Time - self.Last_Time > 1:

            self.FPS = self.Frame_Count / (Current_Time - self.Last_Time)
            self.Frame_Count = 0
            self.Last_Time = Current_Time

        FPS_text = self.FPS_Font.render(f'FPS: {round(self.FPS, 2)}', True, pg.Color('white'))
        self.Screen.blit(FPS_text, (10, 10))

    def Run(self):

        while True:
            
            self.Draw()
            self.Camera.Control()
            [exit() for I in pg.event.get() if I.type == pg.QUIT]
            pg.display.flip()
            self.Clock.tick(self.FPS)

class MinecraftObjectTool(tk.Tk):
    
    def __init__(self):
        super().__init__()

        # Maximizes The Window
        self.state("zoomed")
        
        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

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

        self.Initialize_Pygame_Display()

    def Initialize_Variables(self):

        self.Background_Color = '#131313'
        self.Canvas_Color = 'white'
        self.Common_X = 0.97
        self.Point_Color = '#131313'
        self.Line_Color = "#0000FF"
        self.Fill_Color = "#000000"
        self.Animation_Time = 1
        self.Defult_Object_Rotation = tk.StringVar(value="None")
        self.Object_Rotation_Speed_Entry = tk.StringVar(value="0.05")
        self.Automatic_Rotation = tk.BooleanVar(value=False)
        self.Vsync = 1

    def Initialize_Pygame_Display(self):

        pg.display.init()
        self.Pygame_Screen = pg.display.set_mode((self.Preview_Canvas.winfo_width(), self.Preview_Canvas.winfo_height()))
        self.Software_Render = SoftwareRender(self.Preview_Canvas.winfo_vrootwidth(), self.Preview_Canvas.winfo_vrootheight(), self.Vsync)
        self.Update_Pygame()
        
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
        pg.mixer.init()

        self.Sounds = {}
        Sound_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Sounds")

        # List Of Custom Counds
        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Setting"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Launch Version"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back")
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pg.mixer.Sound(Sound_File)

    def Load_Checkbox_Images(self):
        
        Texture_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures")

        Checked_Image = Image.open(os.path.join(Texture_Directory, "CheckBox_Checked.png"))
        Unchecked_Image = Image.open(os.path.join(Texture_Directory, "CheckBox_Unchecked.png"))

        self.Checked_Image = ImageTk.PhotoImage(Checked_Image)
        self.Unchecked_Image = ImageTk.PhotoImage(Unchecked_Image)

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)
        
        if Sound:
            Sound.play()
    
    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Minecraft Object Tool")

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

        # Create Buttons
        self.Create_Buttons()

        # Create The Preview Area
        self.Create_Preview_Area()

    def Create_Header_Frame(self):

        Server_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Object_Rendering.png")
        Server_Icon = ImageTk.PhotoImage(Image.open(Server_Icon_Path).resize((32, 32)))

        Header_Frame = tk.Frame(self, bg='#4C4C4C') 
        Header_Frame.pack(fill=tk.X)

        Icon_Label = tk.Label(Header_Frame, image=Server_Icon, bg='#4C4C4C')
        Icon_Label.image = Server_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="Minecraft Object Tool", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Checkboxes(self, Parent, Text, Variable):

        Checkbox_Frame = tk.Frame(Parent, bg="#252525")
        Checkbox_Frame.pack(fill="x", pady=(5, 5))

        tk.Label(Checkbox_Frame, text="", width=2, bg="#252525").pack(side=tk.LEFT)

        Checkbox_Label = tk.Label(Checkbox_Frame, image=self.Unchecked_Image, bg="#252525")
        Checkbox_Label.pack(side=tk.LEFT)

        tk.Label(Checkbox_Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#252525", fg="white").pack(side=tk.LEFT)

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

        # Set Initial State To Unchecked
        IntialLoad()

    def Create_Entry(self, Parent, Default_Text):

        Var = tk.StringVar(value=Default_Text)
        Entry = tk.Entry(Parent, textvariable=Var, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#3C3F41", fg="white", insertbackground="white")
        Entry.pack(side=tk.LEFT)
    
    def Create_Dropdown(self, Parent, Options, Default_Value):

        Var = tk.StringVar(value=Default_Value)
        Options = Options
        Dropdown = tk.OptionMenu(Parent, Var, *Options)
        Dropdown.config(bg="#3C3F41", fg="white", font=self.Custom_Fonts["Minecraft Seven v2"], highlightbackground="#2B2B2B")
        Dropdown["menu"].config(bg="#3C3F41", fg="white", font=self.Custom_Fonts["Minecraft Seven v2"], activebackground="#4C4C4C")
        Dropdown.pack(side=tk.LEFT, padx=10)
        
    def Create_Buttons(self):

        Buttons = [
            ("Import Object", self.Render_Object, "#1D6E02", "#2ca903", "#FFFFFF"),
            ("Back", self.Show_MasterCraftMainScreen, "#4C4C4C", "#2B2B2B", "#6C6C6C")
        ]

        for Text, Function, Color, Highlight_Color, Pressed_Color in Buttons:
            self.Add_Button(self.Frame, Text, Function, Color, Highlight_Color, Pressed_Color)

    def Create_Slider(self, Parent, Range, Default_Value):

        Slider_Range = Range
        Var = tk.DoubleVar(value=Default_Value)
        Slider = tk.Scale(Parent, from_=Slider_Range[0], to=Slider_Range[1], resolution=Slider_Range[2], orient=tk.HORIZONTAL, variable=Var, bg="#3C3F41", fg="white", troughcolor="#1E1E1E", highlightbackground="#2B2B2B", font=self.Custom_Fonts["Minecraft Seven v2"])
        Slider.pack(side=tk.LEFT)
    
    def Create_Preview_Area(self):

        # Preview Area
        self.Preview_Canvas = tk.Canvas(self.Main_Frame, bg='#252525', highlightthickness=0)
        self.Preview_Canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        # Pygame Embedding
        os.environ['SDL_WINDOWID'] = str(self.Preview_Canvas.winfo_id())
        
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        # Output Canvas Below the Preview Area
        self.Preview_Frame = tk.Canvas(self.Main_Frame, bg='#252525', height=100, highlightthickness=0)
        self.Preview_Frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=(5, 0))

        self.Create_Slider(self.Preview_Frame, (0, 360, 0.1), 0)
        self.Create_Slider(self.Preview_Frame, (0, 360, 0.1), 0)
        self.Create_Slider(self.Preview_Frame, (0, 360, 0.1), 0)
        self.Create_Dropdown(self.Preview_Frame, ["Rotate X", "Rotate Y", "Rotate Z", "Rotate XY", "Rotate XZ", "Rotate YZ", "Rotate XYZ"], self.Defult_Object_Rotation.get())
        self.Create_Checkboxes(self.Preview_Frame, "Automatic Rotation", self.Automatic_Rotation)
        
    def Add_Button(self, Parent, Text, Function, Color, Highlight_Color, Pressed_Color):

        Button = tk.Button(Parent, text=Text, command=Function, bg=Color, fg='white', activebackground=Pressed_Color, font=self.Custom_Fonts["Minecraft Seven v2"])

        if Text == "Import Object":
            Button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        if Text == "Back":
            Button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        Button.bind("<Enter>", lambda e: Button.config(bg=Highlight_Color))
        Button.bind("<Leave>", lambda e: Button.config(bg=Color))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)

    def Update_Rotation_State(self):
        
        if hasattr(self, 'Software_Render') and self.Software_Render.Object:

            Rotation_State = self.Automatic_Rotation.get()
            self.Software_Render.Update_Rotation(Rotation_State)

    def Update_Pygame(self):

        self.Update_Rotation_State()
        self.Software_Render.Draw()
        self.Software_Render.Camera.Control()
        pg.display.flip()
        self.after(1, self.Update_Pygame)
        self.update()

    def Render_Object(self):
        
        FilePath = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select an OBJ file", filetypes=(("OBJ files", "*.obj"), ("all files", "*.*")))
        self.Software_Render.Import_Object(FilePath)
        self.Software_Render.Draw() 

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
    App = MinecraftObjectTool()
    App.mainloop()

if __name__ == "__main__":
    Main()