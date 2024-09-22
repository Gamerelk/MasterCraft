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

class FontGenerator(tk.Tk):

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

    def Initialize_Variables(self):

        self.Selected_Font = tk.StringVar(value="Minecraft Regular")
        self.Selected_Color = tk.StringVar(value="Black")
        self.Selected_Border_Color = tk.StringVar(value="Black")
        self.Selected_Font_Sheet_Size = tk.StringVar(value="128x128")
        self.Selected_Font_Sheet_Filter = tk.StringVar(value="None")
        
        self.Size_Entry = tk.StringVar(value="24")
        self.Border_Size_Entry = tk.StringVar(value="0")

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
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back"),
            (os.path.join(Sound_Directory, "UI_Notification_Recieved.ogg"), "Notify Recieve"),
            (os.path.join(Sound_Directory, "UI_Notification_Removed.ogg"), "Notify Remove")
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)

        if Sound:
            Sound.play()

    def Notify(self, Message):

        # Create A Frame For The Notification
        Notification_Frame = tk.Frame(self)
        Notification_Frame.place(relx=0.5, y=-100, anchor='n', width=360, height=80)

        # Load Notification Image
        Notification_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Advancement.png")
        Notification_Image = Image.open(Notification_Image_Path)
        Notification_Image = Notification_Image.resize((360, 80), Image.Resampling.NEAREST)
        self.Notification_Image = ImageTk.PhotoImage(Notification_Image)

        # Create Label And Add Notification Image
        Label = tk.Label(Notification_Frame, image=self.Notification_Image)
        Label.place(relx=0.5, rely=0.5, anchor='center')

        # Add Text
        Label.config(compound=tk.CENTER, text=Message, fg="white", font=self.Custom_Fonts["Minecraft Seven v2"])

        self.Play_Sound("Notify Recieve")

        # Animate Notification Slide Down
        def Slide_Down(Current_Y):

            if Current_Y < 20:
                Notification_Frame.place(y=Current_Y)
                self.after(10, Slide_Down, Current_Y + 2)

            else:
                self.after(3000, Slide_Up, 20)

        # Animate Notification Slide Up
        def Slide_Up(Current_Y):

            if Current_Y > -100:
                Notification_Frame.place(y=Current_Y)
                self.after(10, Slide_Up, Current_Y - 2)

                if Current_Y == 0:
                    self.Play_Sound("Notify Remove")
            else:
                Notification_Frame.destroy()

        Slide_Down(-100)

    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Font Generator")

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

        Font_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Font_Generator.png")
        Font_Icon = ImageTk.PhotoImage(Image.open(Font_Icon_Path).resize((32, 32)))

        Icon_Label = tk.Label(Header_Frame, image=Font_Icon, bg='#4C4C4C')
        Icon_Label.image = Font_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="FONT GENERATOR", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
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
            ("Font Color", self.Selected_Color, ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Brown", "Pink", "White", "Gray", "Magenta"]),
            ("Border Color", self.Selected_Border_Color, ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Brown", "Pink", "White", "Gray", "Magenta"]),
            ("Glyph Size", self.Selected_Font_Sheet_Size, ["128x128", "256x256", "512x512", "1024x1024", "2048x2048"]),
            ("Glyph Filter", self.Selected_Font_Sheet_Filter, ["None", "Sharpen Edge", "Sharpen Edge More", "Detail"]),
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
        ]

        for Text, Entry in Entries:
            
            Frame = tk.Frame(self.Left_Panel, bg='#2B2B2B')
            Frame.pack(fill=tk.X, padx=5, pady=5)

            Label = tk.Label(Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#2B2B2B', fg='white')
            Label.pack(anchor='w')

            Entry_Widget = tk.Entry(Frame, textvariable=Entry, bg='#4C4C4C', fg='white')
            Entry_Widget.pack(fill=tk.X)

    def Create_Preview_Area(self):

        Preview_Label = tk.Label(self.Right_Panel, text="Preview", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#2B2B2B', fg='white')
        Preview_Label.pack(pady=10)

        self.Preview_Canvas = tk.Canvas(self.Right_Panel, bg='#3C3F41', highlightthickness=0)
        self.Preview_Canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.Text_Entry = tk.Entry(self.Right_Panel, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white')
        self.Text_Entry.pack(fill=tk.X, padx=10, pady=10)

    def Create_Buttons(self):

        Buttons = [
            ("Update Preview", self.Update_Preview),
            ("Download", self.Download_Image),
            ("Convert Font", self.Convert_Font),
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

    def Update_Preview(self):

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

        # Clear Previous Text
        self.Preview_Canvas.delete("all")

        # Create A Temporary Font To Measure Text Dimensions
        Temporary_Font = TkFont.Font(family=Selected_Font, size=Selected_Size)
        Text_Width = Temporary_Font.measure(User_Text)
        Text_Height = Temporary_Font.metrics("linespace")

        # Resize The Canvas To Fit The Text
        self.Preview_Canvas.config(width=Text_Width + 2 * Border_Size + 2, height=Text_Height + 2 * Border_Size + 2)

        # Draw The Border By Drawing Text Multiple Times
        X, Y = Border_Size + 2, Border_Size + 1

        for DX in range(-Border_Size, Border_Size + 1):

            for DY in range(-Border_Size, Border_Size + 1):

                if DX != 0 or DY != 0:
                    self.Preview_Canvas.create_text(X + DX, Y + DY, text=User_Text, font=Temporary_Font, fill=Border_Color, anchor='nw')

        # Draw The Main Text
        self.Preview_Canvas.create_text(X, Y, text=User_Text, font=Temporary_Font, fill=Selected_Color, anchor='nw')

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

        # Notify User
        self.Notify("Text Downloaded Successfully!")

        # Save The Image
        Downloads_Folder = os.path.join(self.User_Home, "Downloads")
        Output_Image_Path = os.path.join(Downloads_Folder, "Text.png")
        Download_Image.save(Output_Image_Path)

    def Convert_Font(self):

        FilePath = filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select an TTF file", filetypes=(("TTF files", "*.ttf"), ("all files", "*.*")))

        if not FilePath:
            return

        Downloads_Folder = os.path.join(os.path.expanduser("~"), "Downloads")
        Output_Font_Image_Path = os.path.join(Downloads_Folder, "default8.png")

        Image_Size = None
        Font_Size = None

        # Add Additional Font Sizes
        if self.Selected_Font_Sheet_Size.get() == "128x128":
            Image_Size = (128, 128)
            Font_Size = 8

        if self.Selected_Font_Sheet_Size.get() == "256x256":
            Image_Size = (256, 256)
            Font_Size = 16

        if self.Selected_Font_Sheet_Size.get() == "512x512":
            Image_Size = (512, 512)
            Font_Size = 32

        if self.Selected_Font_Sheet_Size.get() == "1024x1024":
            Image_Size = (1024, 1024)
            Font_Size = 64

        if self.Selected_Font_Sheet_Size.get() == "2048x2048":
            Image_Size = (2048, 2048)
            Font_Size = 128

        # Create A New Blank Image With RGBA Mode
        Glyph_Image = Image.new('RGBA', Image_Size, (0, 0, 0, 0))

        # Load The Font
        Font = ImageFont.truetype(FilePath, Font_Size)

        # Create A Drawing Of The Image
        Draw = ImageDraw.Draw(Glyph_Image)

        # Define The Characters To Include (16 Characters Per Line)
        CharactersBitMap = (
            'ÀÁÂÈÊËÍÓÔÕÚßãõğİ'
            '¹ŒœŞşŴŵžê§©     '
            ' !"#$%&\'()*+,-./'
            '0123456789:;<=>?'
            '@ABCDEFGHIJKLMNO'
            'PQRSTUVWXYZ[\\]^_'
            '`abcdefghijklmno'
            'pqrstuvwxyz{|}~⌂'
            'ÇüéâäàåçêëèïîìĂÅ'
            'ÈæÆôöòûùÿŎŰø£Ø¤ƒ'
            'áíóúñÑªº¿®¬½¼¡«»'
            '����������������'
            '����������������'
            '����������������'
            'αβΓπΣσμγϘθΩ ↀ ∈∩'
            '≡±≥≤⌠⌡÷≈ᵒ▪ √ⁿ²■'
        )

        # Define The Grid Layout (16 Rows x 16 Columns)
        GlyphRows, GlyphColumns = 16, 16

        Cell_Width = Image_Size[0] // GlyphColumns
        Cell_Height = Image_Size[1] // GlyphRows

        # Draw Each Character In The Appropriate Cell If It Has A Glyph
        for I, Characters in enumerate(CharactersBitMap):

            try:
                # Checks If The Character Has A Glyph
                Font.getmask(Characters)

                # Create
                Row = I // GlyphColumns
                Column = I % GlyphColumns

                X = Column * Cell_Width - 2
                Y = Row * Cell_Height


                Draw.text((X + Cell_Width // 4, Y), Characters, font=Font, fill=(255, 255, 255, 255))
            except:
                pass

        # Notify User
        self.Notify("Glyph Converted Successfully!")

        # Save The Glyph Image
        Glyph_Image.save(Output_Font_Image_Path)

        # Add Additional Font Filters
        if self.Selected_Font_Sheet_Filter.get() == "Sharpen Edge":

            FontImage = Image.open(Output_Font_Image_Path)

            Enhance = FontImage.filter(ImageFilter.EDGE_ENHANCE)
            Enhance.save(Output_Font_Image_Path)

        if self.Selected_Font_Sheet_Filter.get() == "Sharpen Edge More":
            
            FontImage = Image.open(Output_Font_Image_Path)

            Enhance = FontImage.filter(ImageFilter.EDGE_ENHANCE_MORE)
            Enhance.save(Output_Font_Image_Path)

        if self.Selected_Font_Sheet_Filter.get() == "Detail":
            
            FontImage = Image.open(Output_Font_Image_Path)

            Enhance = FontImage.filter(ImageFilter.DETAIL)
            Enhance.save(Output_Font_Image_Path)

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
    app = FontGenerator()
    app.mainloop()

if __name__ == "__main__":
    Main()
