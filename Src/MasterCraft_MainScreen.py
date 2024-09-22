import os
import tkinter as tk
import tkinter.font as TkFont
from tkextrafont import Font
from PIL import ImageTk, Image
import subprocess
import time
import pygame
import json

class MasterCraftApp(tk.Tk):

    def __init__(self):
        super().__init__()

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

        # Loads The Main Screen Settings
        self.Load_Main_Menu_Settings()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Icons
        self.Load_Icons()

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

    def Load_Main_Menu_Settings(self):

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
        
        def Read_Main_Menu_Settings():

            MainScreen_Settings = self.Current_Settings.get("Main Menu", {})

            Enable_Panorama_Setting = MainScreen_Settings["Enable Panorama Background"]
            Panorama_Background_Setting = MainScreen_Settings["Default Panorama Background"]
            Panorama_Rotation_Speed_Setting = MainScreen_Settings["Default Panorama Rotation Speed"]

            return Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting

        self.Enable_Panorama_Setting, self.Panorama_Background_Setting, self.Panorama_Rotation_Setting = Read_Main_Menu_Settings()

    def Load_Icons(self):

        self.Icons = {}
        Icon_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons")
        
        # List Of Custom Icons
        Icon_Paths = [
            (os.path.join(Icon_Directory, "Recipe_Generator.png"), "Recipe Generator"),
            (os.path.join(Icon_Directory, "Font_Generator.png"), "Font Generator"),
            (os.path.join(Icon_Directory, "Title_Generator.png"), "Title Generator"),
            (os.path.join(Icon_Directory, "System.png"), "Manifest Generator"),
            (os.path.join(Icon_Directory, "Minecraft_Calculator.png"), "Minecraft Calculator"),
            (os.path.join(Icon_Directory, "Code_Builder.png"), "Code Block Builder"),
            (os.path.join(Icon_Directory, "Panorama_Creator.png"), "Panorama Creator"),
            (os.path.join(Icon_Directory, "Object_And _Json_Converter.png"), "Object To Json"),
            (os.path.join(Icon_Directory, "Object_And _Json_Converter.png"), "Json To Object"),
            (os.path.join(Icon_Directory, "NBT_Editor.png"), "NBT Editor"),
            (os.path.join(Icon_Directory, "Re_Enable_Achievements.png"), "Re-Enable World Achivements"),
            (os.path.join(Icon_Directory, "Host_Server.png"), "Host Server"),
            (os.path.join(Icon_Directory, "Versions.png"), "Version Swapper"),
            (os.path.join(Icon_Directory, "Object_Rendering.png"), "Object Live Rendering")
        ]
        
        for Icon_Path, Icon_Name in Icon_Paths:
            self.Icons[Icon_Name] = ImageTk.PhotoImage(Image.open(Icon_Path))

    def Load_Sounds(self):

        # Load In Pygames Library
        pygame.mixer.init()

        self.Sounds = {}
        Sound_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Sounds")

        # List Of Custom Counds
        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Setting"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Recipe Generator"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Font Generator"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Title Generator"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Manifest Generator"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Minecraft Calculator"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Code Block Builder"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Panorama Creator"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Object To Json"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Json To Object"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "NBT Editor"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Re-Enable World Achivements"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Host Server"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Version Swapper"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Object Live Rendering"),
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)

        if Sound:
            Sound.play()
        
    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Bedrock Tools")

        # Set The Main Window Color
        self.configure(bg="#2B2B2B")
        
        # Set Window Icon
        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Path)

        # Create Header Frame
        Header_Frame = tk.Frame(self, bg='#2B2B2B')
        Header_Frame.pack(fill=tk.X)

        # Create A Frame For The Icon And Title To Keep Them Together
        Title_Frame = tk.Frame(Header_Frame, bg='#2B2B2B')
        Title_Frame.pack(side=tk.LEFT, expand=True)

        # Load And Display The App icon Next To The Text
        App_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        App_Icon = ImageTk.PhotoImage(Image.open(App_Icon_Path).resize((32, 32)))

        Icon_Label = tk.Label(Title_Frame, image=App_Icon, bg='#2B2B2B')
        Icon_Label.image = App_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(0, 5))

        # Add "BEDROCK TOOLS" Text Right Next To The Icon
        Title_Label = tk.Label(Title_Frame, text="BEDROCK TOOLS", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#2B2B2B', fg='white')
        Title_Label.pack(side=tk.LEFT)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#2B2B2B', bd=0, highlightthickness=0, command=self.Setting, activebackground="#2B2B2B")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

        # Create Main Frame
        Main_Frame = tk.Frame(self, bg='#3C3F41')
        Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Top Row Of Category Frames
        Top_Row = tk.Frame(Main_Frame, bg='#3C3F3C')
        Top_Row.pack(fill=tk.X, pady=(0, 5))
        
        # Add-ons Frame
        self.Create_Category_Frame(Top_Row, "ADD-ONS", "Common Add-on Relate Uses", [
            "Recipe Generator",
            "Font Generator",
            "Title Generator"
        ])
        
        # Utilities Frame
        self.Create_Category_Frame(Top_Row, "UTILITIES", "Useful Tool Completion For Other Stuff", [
            "Manifest Generator",
            "Minecraft Calculator",
            "Code Block Builder"
        ])
        
        # Advanced Frame
        self.Create_Category_Frame(Top_Row, "ADVANCED", "Complex Functions And Generators", [
            "Panorama Creator",
            "Object To Json",
            "Json To Object",
            "NBT Editor"
        ])
        
        # Create Bottom Row Of Category Frames
        Bottom_Row = tk.Frame(Main_Frame, bg='#3C3F3C')
        Bottom_Row.pack(fill=tk.X, pady=(5, 0))
        
        # Bedrock Tools Frame
        self.Create_Category_Frame(Bottom_Row, "WORLD UTILITIES", "World And Structure Utilities", [
            "Re-Enable World Achivements",
        ])
        
        # Internal Tools Frame
        self.Create_Category_Frame(Bottom_Row, "INTERNAL TOOLS", "For Testing Purposes", [
            "Host Server",
            "Version Swapper",
            "Object Live Rendering"
        ])

    # A Function That Creates Frames
    def Create_Category_Frame(self, Parent, Title, Description, Button_Texts):
        
        Frame = tk.Frame(Parent, bg='#2B2B2B', bd=4, relief=tk.RAISED)
        Header_Frame = tk.Frame(Frame, bg='#4C4C4C')
        Header_Frame.pack(fill=tk.X)

        tk.Label(Header_Frame, text=Title, bg='#4C4C4C', fg='white', font=self.Custom_Fonts.get("Minecraft Ten v2", TkFont.Font())).pack(anchor='w', padx=5, pady=(5, 0))
        tk.Label(Header_Frame, text=Description, bg='#4C4C4C', fg='gray', font=self.Custom_Fonts.get("Minecraft Seven v2", TkFont.Font())).pack(anchor='w', padx=5, pady=(0, 5))
        
        # Add Buttons To The Frame
        for text in Button_Texts:
            self.Add_Button(Frame, text)
            
        Frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5) if Parent == self.winfo_children()[0] else 0)
        
        return Frame

    def Add_Button(self, Parent, Text):
        
        Icon = self.Icons.get(Text)

        Button = tk.Button(Parent, text=Text, bg='#2B2B2B', fg='white', relief=tk.FLAT, font=self.Custom_Fonts.get("Minecraft Ten v2", TkFont.Font()), image=Icon, compound='left', anchor='w', padx=10)
        Button.image = Icon 
        Button.pack(fill=tk.X, padx=5, pady=(5 if Parent.pack_slaves() == [] else 2))
        
        # Bind Hover Effects And Sounds Played For Button Pressed Event 
        Button.bind("<Enter>", lambda e: Button.config(bg='#4C4C4C'))
        Button.bind("<Leave>", lambda e: Button.config(bg='#2B2B2B'))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

        return Button
    
    # A Function That Runs Code When the Button Is Pressed
    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)
        
        if Button_Text == "Recipe Generator":
            self.Show_RecipeGenerator()

        if Button_Text == "Font Generator":
            self.Show_FontGenerator()

        if Button_Text == "Title Generator":
            self.Show_TitleGenerator()

        if Button_Text == "Manifest Generator":
            self.Show_ManifestGenerator()

        if Button_Text == "Minecraft Calculator":
            self.Show_MinecraftCalculator()

        if Button_Text == "Code Block Builder":
            self.Show_MinecraftCodeBuilder()

        if Button_Text == "Panorama Creator":
            self.Show_PanoramaCreator()

        if Button_Text == "Object To Json":
            self.Show_ObjectToJson()

        if Button_Text == "Json To Object":
            self.Show_JsonToObject()

        if Button_Text == "NBT Editor":
            self.Show_NBTEditor()

        if Button_Text == "Re-Enable World Achivements":
            self.Show_ReEnableWorldAchivements()

        if Button_Text == "Host Server":
            self.Show_Local_Server()

        if Button_Text == "Version Swapper":
            self.Show_Version_Swapper()
        
        if Button_Text == "Object Live Rendering":
            self.Show_Object_Renderer_Tool()

    # A Function That Interacts With The Program Settings
    def Setting(self):

        self.Play_Sound("Setting")

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Setting.py")
        subprocess.Popen(["python", Script_Path])
        
    # A Function That Opens Recipe Generator
    def Show_RecipeGenerator(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Recipe_Generator.py")
        subprocess.Popen(["python", Script_Path])

        time.sleep(0.2)
        self.destroy()

    # A Function That Opens Font Generator
    def Show_FontGenerator(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Font_Generator.py")
        subprocess.Popen(["python", Script_Path])

        time.sleep(0.2)
        self.destroy()

    # A Function That Opens Title Generator
    def Show_TitleGenerator(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Title_Generator.py")
        subprocess.Popen(["python", Script_Path])

        time.sleep(0.2)
        self.destroy()

    # A Function That Opens Manifest Generator
    def Show_ManifestGenerator(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Manifest_Generator.py")
        subprocess.Popen(["python", Script_Path])
        
        time.sleep(0.2)
        self.destroy()

    # A Function That Opens The Minecraft Calculator Tool
    def Show_MinecraftCalculator(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Calculator_Generator.py")
        subprocess.Popen(["python", Script_Path])
        
        time.sleep(0.2)
        self.destroy()

    # A Function That Opens The Minecraft Code Builder Tool
    def Show_MinecraftCodeBuilder(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Block_Code_Builder.py")
        subprocess.Popen(["python", Script_Path])
        
        time.sleep(0.2)
        self.destroy()

    # A Function That Opens Panorama Creator Tool
    def Show_PanoramaCreator(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Panorama_Creator.py")
        subprocess.Popen(["python", Script_Path])

        time.sleep(0.2)
        self.destroy()

    # A Function That Opens The Object To Json Converter Tool
    def Show_ObjectToJson(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_OBJ_To_JSON.py")
        subprocess.Popen(["python", Script_Path])

    # A Function That Opens The Json To Object Converter Tool
    def Show_JsonToObject(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_JSON_To_OBJ.py")
        subprocess.Popen(["python", Script_Path])

    # A Function That Opens The NBT Editor
    def Show_NBTEditor(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_NBT_Editor.py")
        subprocess.Popen(["python", Script_Path])

        time.sleep(0.2)
        self.destroy()

    # A Function That Opens Manifest Generator
    def Show_ReEnableWorldAchivements(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Re-Enable_Achivements_Function.py")
        subprocess.Popen(["python", Script_Path])

    # A Function That Hosts A Local Server
    def Show_Local_Server(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Host_Local_Server.py")
        subprocess.Popen(["python", Script_Path])
        
        time.sleep(0.2)
        self.destroy()

    # A Function That Swaps Minecraft Versions
    def Show_Version_Swapper(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Version_Swapper.py")
        subprocess.Popen(["python", Script_Path])
        
        time.sleep(0.2)
        self.destroy()
    
    # A Function That Shows Real Time Object Render
    def Show_Object_Renderer_Tool(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Src", "Minecraft_Object_Renderer_Tool.py")
        subprocess.Popen(["python", Script_Path])
        
        time.sleep(0.2)
        self.destroy()

    # A Function That Finds MasterCraft Folder
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
    App = MasterCraftApp()
    App.mainloop()

if __name__ == "__main__":
    Main()
