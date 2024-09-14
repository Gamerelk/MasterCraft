import os
import tkinter as tk
import tkinter.font as TkFont
from tkextrafont import Font
from PIL import ImageTk, Image
import pygame
import json

class SettingsApp(tk.Tk):
        
    def __init__(self):
        super().__init__()

        # Maximizes The Window
        self.state("zoomed")
        
        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Setting The Current Setting To None
        self.MasterCraft_Enable_Panorama_Setting = None
        self.MasterCraft_Panorama_Background_Setting = None
        self.MasterCraft_Panorama_Rotation_Setting = None

        self.Recipe_Enable_Panorama_Setting = None
        self.Recipe_Panorama_Background_Setting = None
        self.Recipe_Panorama_Rotation_Setting = None

        self.Font_Enable_Panorama_Setting = None
        self.Font_Panorama_Background_Setting = None
        self.Font_Panorama_Rotation_Setting = None

        self.Manifest_Enable_Panorama_Setting = None
        self.Manifest_Panorama_Background_Setting = None
        self.Manifest_Panorama_Rotation_Setting = None
        self.Manifest_Default_Manifest_Setting = None
        self.Manifest_Default_Layout_Setting = None
        self.Manifest_Text_Header_Color_Setting = None
        self.Manifest_Text_Color_Setting = None
        self.Manifest_Text_Special_Character_Color_Setting = None

        self.Code_Builder_Default_Text_Color_Setting = None
        self.Code_Builder_Default_Import_Color_Setting = None
        self.Code_Builder_Default_Control_Color_Setting = None
        self.Code_Builder_Default_World_Color_Setting = None
        self.Code_Builder_Default_Player_Color_Setting = None
        self.Code_Builder_Default_Dimension_Color_Setting = None
        self.Code_Builder_Default_Entity_Color_Setting = None
        self.Code_Builder_Default_Custom_Color_Setting = None

        self.Panorama_Enable_Minecraft_Overlay_Setting = None
        self.Panorama_Enable_Vsync_Setting = None
        self.Panorama_Default_Rotation_Speed_Setting = None

        # Stores Data Change In The Settings App
        self.Settings_Data = {}

        # Loads The Current Settings
        self.Load_Current_Settings_Json_File()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Loads The Checkbox Images
        self.Load_Checkbox_Images()

        # Creating Minecraft UI  
        self.Create_UI()

    def Load_Current_Settings_Json_File(self):

        Current_Settings_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Current_Settings.json")
        Default_Settings_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Default_Settings.json")
        self.AllSettings = []
        
        with open(Current_Settings_Path, "r") as Current_File:
            
            self.Current_Settings = json.load(Current_File)

            if self.Current_Settings == {}:
                
                with open(Default_Settings_Path, "r") as Default_File:
                    self.Default_Settings = json.load(Default_File)

                    self.Current_Settings = self.Default_Settings
                    
                    with open(Current_Settings_Path, "w") as Updated_File:
                        json.dump(self.Current_Settings, Updated_File, indent=4)

        def Read_Settings():
            
            Settings = ["Main Menu", "Font Menu", "Recipe Menu", "Manifest Menu", "Code Builder Menu", "Panorama Creator Menu"]

            for Setting in Settings:
                
                Menu_Settings = self.Current_Settings[Setting]

                if Setting == "Main Menu":
                    
                    Enable_Panorama_Setting = Menu_Settings["Enable Panorama Background"]
                    Panorama_Background_Setting = Menu_Settings["Default Panorama Background"]
                    Panorama_Rotation_Speed_Setting = Menu_Settings["Default Panorama Rotation Speed"]
                    
                    self.AllSettings.append([Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting])

                if Setting == "Font Menu":

                    Enable_Panorama_Setting = Menu_Settings["Enable Panorama Background"]
                    Panorama_Background_Setting = Menu_Settings["Default Panorama Background"]
                    Panorama_Rotation_Speed_Setting = Menu_Settings["Default Panorama Rotation Speed"]

                    self.AllSettings.append([Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting])

                if Setting == "Recipe Menu":

                    Enable_Panorama_Setting = Menu_Settings["Enable Panorama Background"]
                    Panorama_Background_Setting = Menu_Settings["Default Panorama Background"]
                    Panorama_Rotation_Speed_Setting = Menu_Settings["Default Panorama Rotation Speed"]

                    self.AllSettings.append([Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting])

                if Setting == "Manifest Menu":

                    Enable_Panorama_Setting = Menu_Settings["Enable Panorama Background"]
                    Panorama_Background_Setting = Menu_Settings["Default Panorama Background"]
                    Panorama_Rotation_Speed_Setting = Menu_Settings["Default Panorama Rotation Speed"]
                    Default_Manifest_Type = Menu_Settings["Default Manifest Type"]
                    Default_Layout = Menu_Settings["Default Layout"]
                    Default_Header_Color = Menu_Settings["Default Text Header Color"]
                    Default_Text_Color = Menu_Settings["Default Text Color"]
                    Default_Special_Character_Color = Menu_Settings["Default Text Special Characters"]

                    self.AllSettings.append([Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting, Default_Manifest_Type, Default_Layout, Default_Header_Color, Default_Text_Color, Default_Special_Character_Color])

                if Setting == "Code Builder Menu":

                    Default_Text_Color = Menu_Settings["Default Text Color"]
                    Default_Import_Color = Menu_Settings["Default Import Color"]
                    Default_Control_Color = Menu_Settings["Default Control Color"]
                    Default_World_Color = Menu_Settings["Default World Color"]
                    Default_Player_Color = Menu_Settings["Default Player Color"]
                    Default_Dimension_Color = Menu_Settings["Default Dimension Color"]
                    Default_Entity_Color = Menu_Settings["Default Entity Color"]
                    Default_Custom_Color = Menu_Settings["Default Custom Color"]

                    self.AllSettings.append([Default_Text_Color, Default_Import_Color, Default_Control_Color, Default_World_Color, Default_Player_Color, Default_Dimension_Color, Default_Entity_Color, Default_Custom_Color])

                if Setting == "Panorama Creator Menu":

                    Enable_Minecraft_Overlay_Setting = Menu_Settings["Enable Minecraft Overlay"]
                    Enable_Vsync_Setting = Menu_Settings["Enable Vsync"]
                    Panorama_Rotation_Speed_Setting = Menu_Settings["Default Rotation Speed"]

                    self.AllSettings.append([Enable_Minecraft_Overlay_Setting, Enable_Vsync_Setting, Panorama_Rotation_Speed_Setting])

        Read_Settings()

        self.MasterCraft_Enable_Panorama_Setting = self.AllSettings[0][0]
        self.MasterCraft_Panorama_Background_Setting = self.AllSettings[0][1]
        self.MasterCraft_Panorama_Rotation_Setting = self.AllSettings[0][2]

        self.Recipe_Enable_Panorama_Setting = self.AllSettings[1][0]
        self.Recipe_Panorama_Background_Setting = self.AllSettings[1][1]
        self.Recipe_Panorama_Rotation_Setting = self.AllSettings[1][2]

        self.Font_Enable_Panorama_Setting = self.AllSettings[2][0]
        self.Font_Panorama_Background_Setting = self.AllSettings[2][1]
        self.Font_Panorama_Rotation_Setting = self.AllSettings[2][2]

        self.Manifest_Enable_Panorama_Setting = self.AllSettings[3][0]
        self.Manifest_Panorama_Background_Setting = self.AllSettings[3][1]
        self.Manifest_Panorama_Rotation_Setting = self.AllSettings[3][2]
        self.Manifest_Default_Manifest_Setting = self.AllSettings[3][3]
        self.Manifest_Default_Layout_Setting = self.AllSettings[3][4]
        self.Manifest_Text_Header_Color_Setting = self.AllSettings[3][5]
        self.Manifest_Text_Color_Setting = self.AllSettings[3][6]
        self.Manifest_Text_Special_Character_Color_Setting = self.AllSettings[3][7]

        self.Code_Builder_Default_Text_Color_Setting = self.AllSettings[4][0]
        self.Code_Builder_Default_Import_Color_Setting = self.AllSettings[4][1]
        self.Code_Builder_Default_Control_Color_Setting = self.AllSettings[4][2]
        self.Code_Builder_Default_World_Color_Setting = self.AllSettings[4][3]
        self.Code_Builder_Default_Player_Color_Setting = self.AllSettings[4][4]
        self.Code_Builder_Default_Dimension_Color_Setting = self.AllSettings[4][5]
        self.Code_Builder_Default_Entity_Color_Setting = self.AllSettings[4][6]
        self.Code_Builder_Default_Custom_Color_Setting = self.AllSettings[4][7]

        self.Panorama_Enable_Minecraft_Overlay_Setting = self.AllSettings[5][0]
        self.Panorama_Enable_Vsync_Setting = self.AllSettings[5][1]
        self.Panorama_Default_Rotation_Speed_Setting = self.AllSettings[5][2]
    
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
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Run"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Stop"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back")
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

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
        self.title("MasterCraft - Minecraft Host Server")

        # Set The Main Window Color
        self.configure(bg="#3C3F41")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Image_Path)

        # Creates The Header Frame
        self.Create_Header_Frame()

        # Create A Canvas
        self.Canvas = tk.Canvas(self, bg="#3C3F41")
        self.Canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add A Scrollbar To The Canvas
        self.Scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.Canvas.yview)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure The Canvas
        self.Canvas.configure(yscrollcommand=self.Scrollbar.set)
        self.Canvas.bind('<Configure>', self.On_Canvas_Configure)

        # Create The Main Frame Inside The Canvas
        self.Main_Frame = tk.Frame(self.Canvas, bg="#3C3F41")
        self.Canvas_Window = self.Canvas.create_window((0, 0), window=self.Main_Frame, anchor="nw")

        # Bind The Frame To Configure Event
        self.Main_Frame.bind("<Configure>", self.On_Frame_Configure)

        # Bind Mouse Wheel Event To The Canvas
        self.Canvas.bind("<MouseWheel>", self.On_Mouse_Wheel)
        
        # Bind Mouse Wheel Event To All Widgets Inside The Main Frame
        self.Main_Frame.bind_all("<MouseWheel>", self.On_Mouse_Wheel)

        # Create Settings Sections
        self.Create_Settings_Sections()

    def Create_Header_Frame(self):

        Setting_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings.png")
        Setting_Icon = ImageTk.PhotoImage(Image.open(Setting_Icon_Path).resize((32, 32)))

        Header_Frame = tk.Frame(self, bg='#2B2B2B') 
        Header_Frame.pack(fill=tk.X)

        # Create A Frame For The Icon And Title To Keep Them Together
        Title_Frame = tk.Frame(Header_Frame, bg='#2B2B2B')
        Title_Frame.pack(side=tk.LEFT, expand=True)

        Icon_Label = tk.Label(Title_Frame, image=Setting_Icon, bg='#2B2B2B')
        Icon_Label.image = Setting_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(0, 5))

        Title_Label = tk.Label(Title_Frame, text="MasterCraft Settings", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#2B2B2B', fg='white')
        Title_Label.pack(side=tk.TOP, pady=5)

    def Create_Checkboxes(self, Parent, Text, Variable):

        Checkbox_Frame = tk.Frame(Parent, bg="#2B2B2B")
        Checkbox_Frame.pack(fill="x", pady=(5, 5))

        tk.Label(Checkbox_Frame, text="", width=2, bg="#2B2B2B").pack(side=tk.LEFT)

        Checkbox_Label = tk.Label(Checkbox_Frame, image=self.Unchecked_Image, bg="#2B2B2B")
        Checkbox_Label.pack(side=tk.LEFT)

        tk.Label(Checkbox_Frame, text=Text, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#2B2B2B", fg="white").pack(side=tk.LEFT, padx=(5, 0))

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

    def Create_Settings_Sections(self):

        # Main Menu Settings Section
        self.Create_Section("Main Menu Settings", [
            ("Enable Panorama Background", "Checkbox", self.MasterCraft_Enable_Panorama_Setting),
            ("Default Panorama Background", "Dropdown", self.Get_Panorama_Cubemap_Options(), self.MasterCraft_Panorama_Background_Setting),
            ("Default Panorama Rotation Speed", "Slider", (0, 1, 0.05), self.MasterCraft_Panorama_Rotation_Setting)
        ])

        # Font Menu Settings Section
        self.Create_Section("Font Menu Settings", [
            ("Enable Panorama Background", "Checkbox", self.Font_Enable_Panorama_Setting),
            ("Default Panorama Background", "Dropdown", self.Get_Panorama_Cubemap_Options(), self.Font_Panorama_Background_Setting),
            ("Default Panorama Rotation Speed", "Slider", (0, 1, 0.05), self.Font_Panorama_Rotation_Setting)
        ])

        # Recipe Menu Settings Section
        self.Create_Section("Recipe Menu Settings", [
            ("Enable Panorama Background", "Checkbox", self.Recipe_Enable_Panorama_Setting),
            ("Default Panorama Background", "Dropdown", self.Get_Panorama_Cubemap_Options(), self.Recipe_Panorama_Background_Setting),
            ("Default Panorama Rotation Speed", "Slider", (0, 1, 0.05), self.Recipe_Panorama_Rotation_Setting)
        ])

        # Manifest Menu Settings Section
        self.Create_Section("Manifest Menu Settings", [
            ("Enable Panorama Background", "Checkbox", self.Manifest_Enable_Panorama_Setting),
            ("Default Panorama Background", "Dropdown", self.Get_Panorama_Cubemap_Options(), self.Manifest_Panorama_Background_Setting),
            ("Default Panorama Rotation Speed", "Slider", (0, 1, 0.05), self.Manifest_Panorama_Rotation_Setting),
            ("Default Manifest Type", "Dropdown", ["Behavior And Resource Manifest","Behaviour Manifest", "Resource Manifest", "World Manifest"], self.Manifest_Default_Manifest_Setting),
            ("Default Layout", "Dropdown", ["Beautified", "Minified"], self.Manifest_Default_Layout_Setting),
            ("Default Text Header Color", "Entry", self.Manifest_Text_Header_Color_Setting),
            ("Default Text Color", "Entry", self.Manifest_Text_Color_Setting),
            ("Default Text Special Characters", "Entry", self.Manifest_Text_Special_Character_Color_Setting)
        ])

        # Code Builder Menu Settings Section
        self.Create_Section("Code Builder Menu Settings", [
            ("Default Text Color", "Entry", self.Code_Builder_Default_Text_Color_Setting),
            ("Default Import Color", "Entry", self.Code_Builder_Default_Import_Color_Setting),
            ("Default Control Color", "Entry", self.Code_Builder_Default_Control_Color_Setting),
            ("Default World Color", "Entry", self.Code_Builder_Default_World_Color_Setting),
            ("Default Player Color", "Entry", self.Code_Builder_Default_Player_Color_Setting),
            ("Default Dimension Color", "Entry", self.Code_Builder_Default_Dimension_Color_Setting),
            ("Default Entity Color", "Entry", self.Code_Builder_Default_Entity_Color_Setting),
            ("Default Custom Color", "Entry", self.Code_Builder_Default_Custom_Color_Setting)
        ])

        # Panorama Creator Menu Settings Section
        self.Create_Section("Panorama Creator Menu Settings", [
            ("Enable Minecraft Overlay", "Checkbox", self.Panorama_Enable_Minecraft_Overlay_Setting),
            ("Enable Vsync", "Checkbox", self.Panorama_Enable_Vsync_Setting),
            ("Default Rotation Speed", "Slider", (0, 1, 0.05), self.Panorama_Default_Rotation_Speed_Setting)
        ])

    def On_Mouse_Wheel(self, event):

        self.Canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def On_Canvas_Configure(self, event):

        self.Canvas.configure(scrollregion=self.Canvas.bbox("all"))

        # Set The Width Of The Main Frame To Match The Canvas
        self.Canvas.itemconfig(self.Canvas_Window, width=event.width)

    def On_Frame_Configure(self, event):

        # Reset The Scroll Region To Encompass The Inner Frame
        self.Canvas.configure(scrollregion=self.Canvas.bbox("all"))

    def Get_Panorama_Cubemap_Options(self):

        Panorama_Folder = os.path.join(self.MasterCraftCurrentDirectory, "App_Panorama_Cubemaps")
        return [File for File in os.listdir(Panorama_Folder) if os.path.isdir(os.path.join(Panorama_Folder, File))]
    
    def Create_Section(self, Title, Settings):

        Section_Frame = tk.Frame(self.Main_Frame, bg="#2B2B2B", bd=2, relief=tk.GROOVE)
        Section_Frame.pack(fill="x", padx=10, pady=10)

        # Section Title
        Title_Label = tk.Label(Section_Frame, text=Title, font=self.Custom_Fonts["Minecraft Ten v2"], bg="#2B2B2B", fg="white")
        Title_Label.pack(pady=(10, 5), padx=10, anchor="w")

        # Settings
        for Setting in Settings:

            Setting_Name, Setting_Type, *Setting_Args = Setting
            Setting_Default = Setting_Args[-1]

            Setting_Frame = tk.Frame(Section_Frame, bg="#2B2B2B")
            Setting_Frame.pack(fill="x", padx=20, pady=5)

            Label = tk.Label(Setting_Frame, text=Setting_Name, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#2B2B2B", fg="white")
            Label.pack(side=tk.LEFT, padx=(0, 10))

            if Setting_Type == "Dropdown":

                Var = tk.StringVar(value=Setting_Default)
                Options = Setting_Args[0]
                Dropdown = tk.OptionMenu(Setting_Frame, Var, *Options)
                Dropdown.config(bg="#3C3F41", fg="white", font=self.Custom_Fonts["Minecraft Seven v2"], highlightbackground="#2B2B2B")
                Dropdown["menu"].config(bg="#3C3F41", fg="white", font=self.Custom_Fonts["Minecraft Seven v2"], activebackground="#4C4C4C")
                Dropdown.pack(side=tk.LEFT)

            elif Setting_Type == "Checkbox":
                
                Var = tk.BooleanVar(value=Setting_Default)
                self.Create_Checkboxes(Setting_Frame, "", Var)

            elif Setting_Type == "Slider":
                
                Slider_Range = Setting_Args[0]
                Var = tk.DoubleVar(value=Setting_Default)
                Slider = tk.Scale(Setting_Frame, from_=Slider_Range[0], to=Slider_Range[1], resolution=Slider_Range[2], orient=tk.HORIZONTAL, variable=Var, bg="#3C3F41", fg="white", troughcolor="#1E1E1E", highlightbackground="#2B2B2B", font=self.Custom_Fonts["Minecraft Seven v2"])
                Slider.pack(side=tk.LEFT)

            elif Setting_Type == "Entry":

                Var = tk.StringVar(value=Setting_Default)
                Entry = tk.Entry(Setting_Frame, textvariable=Var, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#3C3F41", fg="white", insertbackground="white")
                Entry.pack(side=tk.LEFT)

            self.Settings_Data[f"{Title}:{Setting_Name}"] = Var

        # Save Button
        Save_Button = tk.Button(Section_Frame, text="Save Settings", font=self.Custom_Fonts["Minecraft Seven v2"], bg="#4CAF50", fg="white", command=lambda: self.Save_Settings())
        Save_Button.pack(pady=(10, 20))

    def Save_Settings(self):

        self.Play_Sound("Setting")

        # Get The Current Settings
        with open(os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Current_Settings.json"), "r") as file:
            Current_Settings = json.load(file)

        # Update The Settings Based On The Section
        for Setting_Key, Variable in self.Settings_Data.items():

            Section_Name, Setting_Name = Setting_Key.split(':', 1)
            Section_Name = str(Section_Name).replace(" Settings", "")

            Current_Settings[Section_Name][Setting_Name] = Variable.get()

        # Save The Updated Settings
        with open(os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Current_Settings.json"), "w") as file:
            json.dump(Current_Settings, file, indent=4)

    # A Function That Interacts With The Program Settings
    def Setting(self):

        self.Play_Sound("Setting")

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
    App = SettingsApp()
    App.mainloop()

if __name__ == "__main__":
    Main()