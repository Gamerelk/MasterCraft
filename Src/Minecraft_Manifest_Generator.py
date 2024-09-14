import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as TkFont
from tkinter import filedialog
from tkextrafont import Font
from PIL import Image, ImageTk
import subprocess
import time
import pygame
import json
import uuid
import re

MinecraftServerStable = "1.13.0"
MinecraftServerUIStable = "1.1.0"
MinecraftCommonStable = "1.2.0"
MinecraftServerAdminStable = "NA"
MinecraftServerGameTestStable = "NA"
MinecraftServerDebugStable = "NA"

MinecraftServerBeta = "1.14.0-beta"
MinecraftServerUIBeta = "1.2.0-beta"
MinecraftCommonBeta = "NA"
MinecraftServerAdminBeta = "1.0.0-beta"
MinecraftServerGameTestBeta = "1.0.0-beta"
MinecraftServerDebugBeta = "1.0.0-beta"

class ManifestGenerator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Maximizes The Window
        self.state("zoomed")

        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Setting The Current Setting To None
        self.Enable_Panorama_Setting = None
        self.Panorama_Background_Setting = None
        self.Panorama_Rotation_Setting = None
        self.Default_Manifest_Setting = None
        self.Default_Layout_Setting = None
        self.Text_Header_Color_Setting = None
        self.Text_Color_Setting = None
        self.Text_Special_Character_Color_Setting = None

        # Loads The Manifest Settings
        self.Load_Manifest_Menu_Settings()

        self.Module_Versions = {
            "@minecraft/server": {"stable": MinecraftServerStable, "beta": MinecraftServerBeta},
            "@minecraft/server-ui": {"stable": MinecraftServerUIStable, "beta": MinecraftServerUIBeta},
            "@minecraft/common": {"stable": MinecraftCommonStable, "beta": MinecraftCommonBeta},
            "@minecraft/server-admin": {"stable": MinecraftServerAdminStable, "beta": MinecraftServerAdminBeta},
            "@minecraft/server-gametest": {"stable": MinecraftServerGameTestStable, "beta": MinecraftServerGameTestBeta},
            "@minecraft/debug-utilities": {"stable": MinecraftServerDebugStable, "beta": MinecraftServerDebugBeta}
        }

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()
        
        # Loads The Checkbox Images
        self.Load_Checkbox_Images()

        # Creating Minecraft UI  
        self.Create_UI()

    def Load_Manifest_Menu_Settings(self):

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
        
        def Read_Manifest_Menu_Settings():

            Manifest_Settings = self.Current_Settings.get("Manifest Menu", {})

            Enable_Panorama_Setting = Manifest_Settings["Enable Panorama Background"]
            Panorama_Background_Setting = Manifest_Settings["Default Panorama Background"]
            Panorama_Rotation_Speed_Setting = Manifest_Settings["Default Panorama Rotation Speed"]
            Default_Manifest_Type = Manifest_Settings["Default Manifest Type"]
            Default_Layout = Manifest_Settings["Default Layout"]
            Default_Header_Color = Manifest_Settings["Default Text Header Color"]
            Default_Text_Color = Manifest_Settings["Default Text Color"]
            Default_Special_Character_Color = Manifest_Settings["Default Text Special Characters"]

            return Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting, Default_Manifest_Type, Default_Layout, Default_Header_Color, Default_Text_Color, Default_Special_Character_Color

        self.Enable_Panorama_Setting, self.Panorama_Background_Setting, self.Panorama_Rotation_Setting, self.Default_Manifest_Setting, self.Default_Layout_Setting, self.Text_Header_Color_Setting, self.Text_Color_Setting, self.Text_Special_Character_Color_Setting = Read_Manifest_Menu_Settings()

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
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "CheckBox_Press"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Switch"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Generate Manifest"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Download"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back"),
            (os.path.join(Sound_Directory, "UI_Notification_Recieved.ogg"), "Notify Recieve"),
            (os.path.join(Sound_Directory, "UI_Notification_Removed.ogg"), "Notify Remove")
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

    def Notify(self, Message):

        # Create A New Toplevel Window
        Notification = tk.Toplevel(self)
        Notification.overrideredirect(True)
        Notification.attributes("-topmost", True)

        # Load Notification Image
        Notification_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Advancement.png")
        Notification_Image = Image.open(Notification_Image_Path)
        Notification_Image = Notification_Image.resize((360, 80))
        self.Notification_Image = ImageTk.PhotoImage(Notification_Image)

        # Create Canvas And Add Notification Image
        Canvas = tk.Canvas(Notification, width=360, height=80, highlightthickness=0)
        Canvas.pack()
        Canvas.create_image(0, 0, anchor=tk.NW, image=self.Notification_Image)

        # Add Text
        Canvas.create_text(180, 40, text=Message, fill="white", font=self.Custom_Fonts["Minecraft Seven v2"], width=320, anchor=tk.CENTER)

        # Position The Window
        Screen_Width = self.winfo_screenwidth()
        X = int((Screen_Width / 2) - (360 / 2))
        Y_Start = -100
        Y_End  = 20
        AnimationSpeed = 2
        Notification.geometry(f"360x80+{X}+{Y_Start}")

        self.Play_Sound("Notify Recieve")

        # Animate Notification Slide Down
        def Slide_Down(Current_Y):

            if Current_Y < Y_End:

                Notification.geometry(f"360x80+{X}+{Current_Y}")
                Notification.after(10, Slide_Down, Current_Y + AnimationSpeed) 

            else:
                Notification.geometry(f"360x80+{X}+{Y_End}")
                Notification.after(3000, Slide_Up, Y_End)

        # Animate Notification Slide Up
        def Slide_Up(Current_Y):

            if Current_Y > Y_Start:
                Notification.geometry(f"360x80+{X}+{Current_Y}")
                Notification.after(10, Slide_Up, Current_Y - AnimationSpeed)

                if Current_Y == 0:
                    self.Play_Sound("Notify Remove")
                    
            else:
                Notification.destroy()

        Slide_Down(Y_Start)

    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Manifest Generator")

        # Set The Main Window Color
        self.configure(bg="#3C3F41")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Image_Path)

        self.Create_Header_Frame()

        # Creates The Main Frame
        self.Main_Frame = tk.Frame(self, bg="#3C3F41")
        self.Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Creates The Left Panel For Inputs
        self.Left_Panel = tk.Frame(self.Main_Frame, bg="#2B2B2B", width=500)
        self.Left_Panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Creates The Right Panel For Output Code
        self.Right_Panel = tk.Frame(self.Main_Frame, bg="#2B2B2B", width=500)
        self.Right_Panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Create Input Fields
        self.Create_Input_Fields()

        # Create Output Area
        self.Create_Output_Area()

        # Create Button
        self.Create_Buttons()

    def Create_Header_Frame(self):

        Manifiest_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Font_Generator.png")
        Manifiest_Icon = ImageTk.PhotoImage(Image.open(Manifiest_Icon_Path).resize((32, 32)))

        Header_Frame = tk.Frame(self, bg='#4C4C4C') 
        Header_Frame.pack(fill=tk.X)

        Icon_Label = tk.Label(Header_Frame, image=Manifiest_Icon, bg='#4C4C4C')
        Icon_Label.image = Manifiest_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="Manifest Generator", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Buttons(self):

        self.Button_Frame = tk.Frame(self.Left_Panel, bg="#1E1E1E", bd=2, relief=tk.GROOVE)
        self.Button_Frame.pack(ipadx=0, padx=10, pady=10)

        Buttons = [
            ("Generate Manifest", self.Generate_Manifest, "#007ACC", "#0095fa", "#FFFFFF"),
            ("Download", self.Download, "#1D6E02", "#2ca903", "#FFFFFF"),
            ("Back", self.Show_MasterCraftMainScreen, "#4C4C4C", "#2B2B2B", "#6C6C6C")
        ]

        for Text, Function, Color, Highlight_Color, Pressed_Color in Buttons:
            self.Add_Button(self.Button_Frame, Text, Function, Color, Highlight_Color, Pressed_Color)

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

    def Create_Input_Fields(self):

        Box_Frame = tk.Frame(self.Left_Panel, bg="#1E1E1E", bd=2, relief=tk.GROOVE)
        Box_Frame.pack(fill="x", padx=10, pady=10)

        # Manifest Type Section
        tk.Label(Box_Frame, text="Manifest Type:", font=self.Custom_Fonts["Minecraft Ten v2"], bg="#1E1E1E", fg="white").pack(anchor="w", padx=10, pady=(10, 5))
        self.Manifest_Type = ttk.Combobox(Box_Frame, values=["Behavior And Resource Manifest","Behaviour Manifest", "Resource Manifest", "World Manifest"], font=self.Custom_Fonts["Minecraft Seven v2"], state="readonly")
        self.Manifest_Type.pack(fill="x", padx=10, pady=(0, 10))
        self.Manifest_Type.set(self.Default_Manifest_Setting)

        # Name Section
        tk.Label(Box_Frame, text="Name:", font=self.Custom_Fonts["Minecraft Ten v2"], bg="#1E1E1E", fg="white").pack(anchor="w", padx=10, pady=(10, 5))
        self.Name_Entry = tk.Entry(Box_Frame, font=self.Custom_Fonts["Minecraft Seven v2"])
        self.Name_Entry.pack(fill="x", padx=10, pady=(0, 10))

        # Description Section
        tk.Label(Box_Frame, text="Description:", font=self.Custom_Fonts["Minecraft Ten v2"], bg="#1E1E1E", fg="white").pack(anchor="w", padx=10, pady=(10, 5))
        self.Description_Entry = tk.Entry(Box_Frame, font=self.Custom_Fonts["Minecraft Seven v2"])
        self.Description_Entry.pack(fill="x", padx=10, pady=(0, 10))

        # Layout Section
        tk.Label(Box_Frame, text="Layout:", font=self.Custom_Fonts["Minecraft Ten v2"], bg="#1E1E1E", fg="white").pack(anchor="w", padx=10, pady=(10, 5))
        self.Layout = ttk.Combobox(Box_Frame, values=["Beautified", "Minified"], font=self.Custom_Fonts["Minecraft Seven v2"], state="readonly")
        self.Layout.pack(fill="x", padx=10, pady=(0, 10))
        self.Layout.set(self.Default_Layout_Setting)

        self.Script_API_Boolean = tk.BooleanVar(value=False)
        self.Beta_Boolean = tk.BooleanVar(value=False)
        
        self.Create_Checkboxes(self.Left_Panel, "Script API", self.Script_API_Boolean)
        tk.Label(self.Left_Panel, text="Enables Script API", font=self.Custom_Fonts["Minecraft Seven v2"], bg="#2B2B2B", fg="white").pack(anchor="w", padx=(45, 0))

        self.Create_Checkboxes(self.Left_Panel, "Beta", self.Beta_Boolean)
        tk.Label(self.Left_Panel, text="Enable Beta Modules In The Script API", font=self.Custom_Fonts["Minecraft Seven v2"], bg="#2B2B2B", fg="white").pack(anchor="w", padx=(45, 0))

        # Modules
        tk.Label(self.Left_Panel, text="MODULES", font=self.Custom_Fonts["Minecraft Ten v2"], bg="#2B2B2B", fg="white").pack(anchor="w", pady=(10, 5), padx=(20, 0))
        
        self.Module_Data = {}
        Modules = ["@minecraft/server", "@minecraft/server-ui", "@minecraft/common", "@minecraft/server-admin", "@minecraft/server-gametest", "@minecraft/debug-utilities"]
        
        for Module in Modules:

            Boolean = tk.BooleanVar(value=False)
            self.Module_Data[Module] = Boolean
            self.Create_Checkboxes(self.Left_Panel, Module, Boolean)

    def Create_Output_Area(self):

        self.Output_Frame = tk.Frame(self.Right_Panel, bg="#2B2B2B")
        self.Output_Frame.pack(fill=tk.BOTH, expand=True)

        # Create Text Widgets
        self.Output_Text_Main = tk.Text(self.Output_Frame, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#1E1E1E", fg=self.Text_Color_Setting, wrap=tk.NONE)
        self.Output_Text_Secondary = tk.Text(self.Output_Frame, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#1E1E1E", fg=self.Text_Color_Setting, wrap=tk.NONE)

        # Create Scrollbars
        Y_Scrollbar = tk.Scrollbar(self.Output_Frame, orient=tk.VERTICAL)
        X_Scrollbar = tk.Scrollbar(self.Output_Frame, orient=tk.HORIZONTAL)

        # Configure Text Widgets With Scrollbars
        self.Output_Text_Main.config(yscrollcommand=Y_Scrollbar.set, xscrollcommand=X_Scrollbar.set)
        self.Output_Text_Secondary.config(yscrollcommand=Y_Scrollbar.set, xscrollcommand=X_Scrollbar.set)

        Y_Scrollbar.config(command=self.Y_View_Both)
        X_Scrollbar.config(command=self.X_View_Both)

        # Pack Scrollbars
        Y_Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        X_Scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initially Pack Only The First Text Widget
        self.Output_Text_Main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure Text Tags
        for Text_Widget in [self.Output_Text_Main, self.Output_Text_Secondary]:

            Text_Widget.tag_configure("Special_Characters", foreground=self.Text_Special_Character_Color_Setting)
            Text_Widget.tag_configure("Highlight_Words", foreground=self.Text_Header_Color_Setting)
            Text_Widget.config(state=tk.DISABLED)

        # Create Switch Button (Initially Hidden)
        self.Switch_Button = tk.Button(self.Right_Panel, text="Switch View", command=self.Toggle_Output, bg="#007ACC", fg="white", font=self.Custom_Fonts["Minecraft Seven v2"])

        # Bind The Manifest type selection to update the view
        self.Manifest_Type.bind("<<ComboboxSelected>>", self.Update_Output_View)

    def Add_Button(self, Parent, Text, Function, Color, Highlight_Color, Pressed_Color):

        Button = tk.Button(Parent, text=Text, command=Function, bg=Color, fg='white', activebackground=Pressed_Color, font=self.Custom_Fonts["Minecraft Seven v2"])
        Button.pack(side=tk.LEFT)

        if Text == "Download":
            Button.configure(width=17)

        if Text == "Back":
            Button.configure(width=17)
        
        Button.bind("<Enter>", lambda e: Button.config(bg=Highlight_Color))
        Button.bind("<Leave>", lambda e: Button.config(bg=Color))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)

    def Y_View_Both(self, *args):

        self.Output_Text_Main.yview_moveto(args[0])
        self.Output_Text_Secondary.yview_moveto(args[0])

    def X_View_Both(self, *args):

        self.Output_Text_Main.xview_moveto(args[0])
        self.Output_Text_Secondary.xview_moveto(args[0])

    def Toggle_Output(self):

        self.Play_Sound("Switch")

        if self.Output_Text_Main.winfo_viewable():

            self.Output_Text_Main.pack_forget()
            self.Output_Text_Secondary.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:

            self.Output_Text_Secondary.pack_forget()
            self.Output_Text_Main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def Update_Output_View(self, event=None):

        if self.Manifest_Type.get() == "Behavior And Resource Manifest":

            self.Switch_Button.pack(before=self.Output_Frame, pady=5)
        else:

            self.Switch_Button.pack_forget()
            self.Output_Text_Secondary.pack_forget()
            self.Output_Text_Main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def Generate_Manifest(self):

        Manifest_Type = self.Manifest_Type.get()
        Layout = self.Layout.get()
        
        if Manifest_Type == "Behavior And Resource Manifest":
            Manifest_Data_BP, Manifest_Data_RP = self.Generate_Behavior_And_Resource_Manifest()

        elif Manifest_Type == "Behaviour Manifest":
            Manifest_Data = self.Generate_Behavior_Manifest()

        elif Manifest_Type == "Resource Manifest":
            Manifest_Data = self.Generate_Resource_Manifest()

        elif Manifest_Type == "World Manifest":
            Manifest_Data = self.Generate_World_Manifest()

        else:
            return

        # Make Output Boxes Editable
        self.Output_Text_Main.config(state=tk.NORMAL)
        self.Output_Text_Secondary.config(state=tk.NORMAL)

        # Clear All Text In Output
        self.Output_Text_Main.delete("1.0", tk.END)
        self.Output_Text_Secondary.delete("1.0", tk.END)

        self.Highlight_Words = [
            "format_version", "header", "description", "min_engine_version", "modules", 
            "type", "language", "entry", "module_name", "dependencies", "name", 
            "metadata", "authors", "license", "url", "base_game_version", 
            "lock_template_options", "capabilities", "subpacks", "folder_name", "memory_tier",
            "uuid", "version"
        ]

        self.Special_Characters = ["{", "}", "[", "]", ":", ","]

        if Manifest_Type == "Behavior And Resource Manifest":

            if Layout == "Beautified":

                self.Process_Json_Beautified(Manifest_Data_BP, self.Output_Text_Main)
                self.Process_Json_Beautified(Manifest_Data_RP, self.Output_Text_Secondary)

            else:

                self.Process_Json_Minified(Manifest_Data_BP, self.Output_Text_Main)
                self.Process_Json_Minified(Manifest_Data_RP, self.Output_Text_Secondary)

        else:

            if Layout == "Beautified":
                self.Process_Json_Beautified(Manifest_Data, self.Output_Text_Main)

            else:

                self.Process_Json_Minified(Manifest_Data, self.Output_Text_Main)
            self.Output_Text_Secondary.insert(tk.END, "No Second Manifest Has Been Generated. Whatever You Previously Generated Remains In The First Text Output. If You See This Text, Please Click On The Manifest Generate Button To Update Both Text Outputs.")
        
        # Disable Output Boxes From Being Edited
        self.Output_Text_Main.config(state=tk.DISABLED)
        self.Output_Text_Secondary.config(state=tk.DISABLED)

        # Update The View Based On The Current Manifest Type
        self.Update_Output_View()

    def Process_Json_Beautified(self, Data, Text_Widget, Indent=''):
        
        if isinstance(Data, dict):

            Text_Widget.insert(tk.END, "{", "Special_Characters")
            Text_Widget.insert(tk.END, "\n")
            Last_Key = list(Data.keys())[-1]

            for Key, Value in Data.items():

                Text_Widget.insert(tk.END, Indent + "    ")
                Text_Widget.insert(tk.END, f'"{Key}"', "Highlight_Words")
                Text_Widget.insert(tk.END, ": ", "Special_Characters")

                self.Process_Json_Beautified(Value, Text_Widget, Indent + "    ")

                if Key != Last_Key:
                    Text_Widget.insert(tk.END, ",", "Special_Characters")

                Text_Widget.insert(tk.END, "\n")

            Text_Widget.insert(tk.END, Indent + "}", "Special_Characters")

        elif isinstance(Data, list):

            Text_Widget.insert(tk.END, "[", "Special_Characters")
            Text_Widget.insert(tk.END, "\n")

            for I, Item in enumerate(Data):

                Text_Widget.insert(tk.END, Indent + "    ")
                self.Process_Json_Beautified(Item, Text_Widget, Indent + "    ")

                if I < len(Data) - 1:
                    Text_Widget.insert(tk.END, ",", "Special_Characters")

                Text_Widget.insert(tk.END, "\n")

            Text_Widget.insert(tk.END, Indent + "]", "Special_Characters")

        else:
            if isinstance(Data, str):

                Text_Widget.insert(tk.END, f'"{Data}"')
            else:

                Text_Widget.insert(tk.END, str(Data))

    def Process_Json_Minified(self, Data, Text_Widget):

        Json_String = json.dumps(Data, separators=(',', ':'))
        Text_Widget.insert(tk.END, Json_String)
        
        Special_Chars_Pattern = re.escape(''.join(self.Special_Characters))
        Pattern = f'[{Special_Chars_Pattern}]'
        
        Start = '1.0'

        while True:

            Match = Text_Widget.search(Pattern, Start, tk.END, regexp=True)

            if not Match:
                break

            End = f"{Match}+1c"
            Text_Widget.tag_add("Special_Characters", Match, End)
            Start = End

        for Word in self.Highlight_Words:

            Start = '1.0'

            while True:

                Start = Text_Widget.search(f'"{Word}"', Start, tk.END)

                if not Start:
                    break
                
                End = f"{Start}+{len(Word)+2}c"
                Text_Widget.tag_add("Highlight_Words", Start, End)
                Start = End

    def Generate_Behavior_And_Resource_Manifest(self):
        
        ResourceManifestUUID = str(uuid.uuid4())
        BehaviorManifestUUID = str(uuid.uuid4())

        Manifest_Data_BP = {
            "format_version": 2,
            "header": {
                "description": self.Description_Entry.get(),
                "name": self.Name_Entry.get(),
                "uuid": BehaviorManifestUUID,
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 0]
            },
            "modules": [
                {
                    "type": "data",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ],
            "dependencies": [
                {
                    "uuid": ResourceManifestUUID,
                    "version": [1, 0, 0]
                }
            ]
        }
        
        Manifest_Data_RP = {
            "format_version": 2,
            "header": {
                "description": self.Description_Entry.get(),
                "name": self.Name_Entry.get(),
                "uuid": ResourceManifestUUID,
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 0]
            },
            "modules": [
                {
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ],
            "dependencies": [
                {
                    "uuid": BehaviorManifestUUID,
                    "version": [1, 0, 0]
                }
            ]
        }
        
        if self.Script_API_Boolean.get():

            Manifest_Data_BP["modules"].append({
                "type": "script",
                "language": "javascript",
                "entry": "scripts/main.js",
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0]
            })
        
        self.Add_Dependencies(Manifest_Data_BP)
        return Manifest_Data_BP, Manifest_Data_RP

    def Generate_Behavior_Manifest(self):

        Manifest_Data = {
            "format_version": 2,
            "header": {
                "description": self.Description_Entry.get(),
                "name": self.Name_Entry.get(),
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 0]
            },
            "modules": [
                {
                    "type": "data",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ],
            "dependencies": [
                {
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ]
        }

        if self.Script_API_Boolean.get():

            Manifest_Data["modules"].append({
                "type": "script",
                "language": "javascript",
                "entry": "scripts/main.js",
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0]
            })

        self.Add_Dependencies(Manifest_Data)
        return Manifest_Data

    def Generate_Resource_Manifest(self):

        Manifest_Data = {
            "format_version": 2,
            "header": {
                "description": self.Description_Entry.get(),
                "name": self.Name_Entry.get(),
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 0]
            },
            "modules": [
                {
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ],
            "dependencies": [
                {
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ]
        }
        
        return Manifest_Data

    def Generate_World_Manifest(self):

        Manifest_Data = {
            "format_version": 2,
            "header": {
                "name": self.Name_Entry.get(),
                "description": self.Description_Entry.get(),
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 0]
            },
            "modules": [
                {
                    "type": "world_template",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ],
            "dependencies": [
                {
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                }
            ]
        }

        return Manifest_Data

    def Add_Dependencies(self, Manifest_Data):

        for Module, Versions in self.Module_Data.items():

            if Versions.get():

                Version_Type = "beta" if self.Beta_Boolean.get() else "stable"
                Version = self.Module_Versions[Module][Version_Type]
                
                if Version != "NA":
                    Manifest_Data["dependencies"].append({
                        "module_name": Module,
                        "version": Version,
                    })

    def Download(self):

        File_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

        if File_path:

            Manifest_Text_Main = self.Output_Text_Main.get(1.0, tk.END).strip()
            Manifest_Text_Secondary = self.Output_Text_Main.get(1.0, tk.END).strip()

            if Manifest_Text_Main:
                with open(File_path, 'w') as file:
                    file.write(Manifest_Text_Main)

            if Manifest_Text_Secondary:
                with open(File_path, 'w') as file:
                    file.write(Manifest_Text_Secondary)

            self.Notify("Manifest File Downloaded Successfully!")

    # A Function That Interacts With The Program Settings
    def Setting(self):

        self.Play_Sound("Setting")

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Setting.py")
        subprocess.Popen(["python", Script_Path])
        
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
    app = ManifestGenerator()
    app.mainloop()

if __name__ == "__main__":
    Main()