import tkinter as tk
import tkinter.font as TkFont
from tkinter import messagebox
from tkextrafont import Font
from PIL import ImageTk, Image
import json
import os
import subprocess
import time
import pygame

# Recipe Generator Screen
class RecipeGenerator(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Maximizes The Window
        self.state("zoomed")

        # Getting User Pathway
        self.User_Home = os.path.expanduser("~")
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = os.path.normpath(f"{self.SearchDirectory()}")[2: -2]

        # Setting The Current Setting To None
        self.Enable_Panorama_Setting = None
        self.Panorama_Background_Setting = None
        self.Panorama_Rotation_Setting = None

        # Loads The Recipe Settings
        self.Load_Recipe_Menu_Settings()

        # Set Initial Button Array
        self.Buttons = []
        self.Text_Data = []
        
        # Stores The Current Station Used
        self.Current_Station = None

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Creating Minecraft UI 
        self.Create_UI()
        
        # Crafting Station Dictionaries

        self.Input_Fields = {}
        
        # Crafting Table
        self.Crafting_Labels = {}
        self.Crafting_Grid_Frame = {}
        
        # Furnace
        self.Furnace_Labels = {}
        self.Furnace_UI_Labels = {}
        self.Furnace_TextBoxes = {}

        # Brewing Stand
        self.BrewingStand_Labels = {}
        self.BrewingStand_UI_Labels = {}
        self.Brewing_Stand_TextBoxes = {}

        # Smithing Table Armor Trim
        self.Smithing_Table_Armor_Trim_Labels = {}
        self.Smithing_Table_Armor_Trim_UI_Labels = {}
        self.Smithing_Table_Armor_Trim_TextBoxes = {}

        # Smithing Table Transformation
        self.Smithing_Table_Transformation_Labels = {}
        self.Smithing_Table_Transformation_UI_Labels = {}
        self.Smithing_Table_Transformation_TextBoxes = {}

    def Load_Recipe_Menu_Settings(self):

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
        
        def Read_Recipe_Menu_Settings():

            Recipe_Settings = self.Current_Settings.get("Recipe Menu", {})

            Enable_Panorama_Setting = Recipe_Settings["Enable Panorama Background"]
            Panorama_Background_Setting = Recipe_Settings["Default Panorama Background"]
            Panorama_Rotation_Speed_Setting = Recipe_Settings["Default Panorama Rotation Speed"]

            return Enable_Panorama_Setting, Panorama_Background_Setting, Panorama_Rotation_Speed_Setting

        self.Enable_Panorama_Setting, self.Panorama_Background_Setting, self.Panorama_Rotation_Setting = Read_Recipe_Menu_Settings()

    def Load_Custom_Fonts(self):

        self.Custom_Fonts = {}
        Font_Directory = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Fonts")
        
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

        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Setting"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Generate Recipe"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back"),
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)

        if Sound:
            Sound.play()

    def Create_UI(self):

        # Set The Title Of The Window
        self.title("MasterCraft - Recipe Generator")

        # Set The Main Window Color
        self.configure(bg='#1E1E1E')
        
        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Image_Path)

        self.Create_Header_Frame()

        # Create Main Frame
        self.Main_Frame = tk.Frame(self, bg='#1E1E1E')
        self.Main_Frame.pack(fill=tk.BOTH, expand=True)

        # Create Content Frame
        Content_Frame = tk.Frame(self.Main_Frame, bg='#1E1E1E')
        Content_Frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create Left Frame For Input Fields
        self.Left_Frame = tk.Frame(Content_Frame, bg='#2D2D2D', width=400)
        self.Left_Frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.Left_Frame.pack_propagate(False)

        # Create Right Frame For Station Inputs And Images
        self.Right_Frame = tk.Frame(Content_Frame, bg='#2D2D2D')
        self.Right_Frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create Buttons Frame
        self.Buttons_Frame = tk.Frame(self.Main_Frame, bg='#2D2D2D')
        self.Buttons_Frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        # Add Generate Dropdown Selection, Recipe, and Back Button
        self.Create_Dropdown(self.Buttons_Frame, ["Crafting Table", "Furnace", "Brewing Stand", "Smithing Table Armor Trim","Smithing Table Transformation"])
        self.Create_Buttons()

    def Create_Header_Frame(self):

        Header_Frame = tk.Frame(self, bg='#4C4C4C')
        Header_Frame.pack(fill=tk.X)

        Font_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Recipe_Generator.png")
        Font_Icon = ImageTk.PhotoImage(Image.open(Font_Icon_Path).resize((32, 32)))

        Icon_Label = tk.Label(Header_Frame, image=Font_Icon, bg='#4C4C4C')
        Icon_Label.image = Font_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="RECIPE GENERATOR", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    # A Function To Setup The Dropdown Menu
    def Create_Dropdown(self, Parent, List):

        DropDown_Labels = List

        Selected_Table = tk.StringVar()
        Selected_Table.set(DropDown_Labels[0])
        
        Selection_Dropdown = tk.OptionMenu(Parent, Selected_Table, *DropDown_Labels, command=lambda selection: self.CraftingStation(selection))
        Selection_Dropdown.config(bg="#2B2B2B", fg='white', font=self.Custom_Fonts["Minecraft Ten v2"], highlightbackground="#2B2B2B", activebackground="#4C4C4C")
        Selection_Dropdown["menu"].config(bg="#2B2B2B", fg='white', font=self.Custom_Fonts["Minecraft Ten v2"], activebackground="#4C4C4C")
        Selection_Dropdown.pack(side=tk.LEFT, padx=5)

    # Function To Setup The Buttons
    def Create_Buttons(self):

        Buttons = [
            ("Generate Recipe", self.CraftingMake, "#2D2D2D", "#4C4C4C", "#2D2D2D"),
            ("Back", self.Show_MasterCraftMainScreen, "#2D2D2D", "#4C4C4C", "#6C6C6C")
        ]

        for Text, Function, Color, Highlight_Color, Pressed_Color in Buttons:
            self.Add_Button(self.Buttons_Frame, Text, Function, Color, Highlight_Color, Pressed_Color)

    def Add_Button(self, Parent, Text, Function, Color, Highlight_Color, Pressed_Color):

        Button = tk.Button(Parent, text=Text, command=Function, bg=Color, fg='white', activebackground=Pressed_Color, font=self.Custom_Fonts["Minecraft Ten v2"], relief=tk.FLAT)

        if Text == "Generate Recipe":
            Button.pack(side=tk.LEFT, padx=5)

        if Text == "Back":
            Button.pack(side=tk.LEFT, padx=5)

        Button.bind("<Enter>", lambda e: Button.config(bg=Highlight_Color))
        Button.bind("<Leave>", lambda e: Button.config(bg=Color))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)

    # A List Of Functions For Each Crafting Station
    def CraftingStation(self, Selection):
        
        self.Current_Station = Selection

        self.Text_Data = []

        if Selection == "Crafting Table":
            self.CraftingTable()

        if Selection == "Furnace":
            self.Furnace()

        if Selection == "Brewing Stand":
            self.BrewingStand()

        if Selection == "Smithing Table Armor Trim":
            self.SmithingTableTrim()

        if Selection == "Smithing Table Transformation":
            self.SmithingTableTransformation()

    # A Function To Create Recipe Files
    def CraftingMake(self):

        if self.Current_Station is None:
            return messagebox.askokcancel(title="MasterCraft Error Menu", message="Error- Encounter Script Error. Cannot Find Current Station Being Used. Please Select A Station To Resolve This Error")

        self.Station = self.Current_Station

        self.RecipeId = None
        self.Pattern = None
        self.Key = None
        self.ItemId = None
        self.ItemAmount = None
        self.Input = None
        self.Output = None
        self.Reagent = None
        self.Base = None
        self.Template = None
        self.Addition = None

        Downloads_Folder = os.path.join(os.path.expanduser("~"), "Downloads")

        if self.Station == "Crafting Table":
            
            self.RecipeId = self.Input_Fields.get("recipe_id", tk.Entry()).get().strip() or " "
            self.ItemId = self.Input_Fields.get("item_id", tk.Entry()).get().strip() or " "
            self.ItemAmount = self.Input_Fields.get("item_amount", tk.Entry()).get().strip() or " " 
            self.Pattern = ["".join([self.Text_Data[i+j].get("1.0", tk.END).strip() or " " for j in range(3)]) for i in range(0, 9, 3)]   
            self.Key = {self.Text_Data[i+1].get("1.0", tk.END).strip(): {"item": self.Text_Data[i].get("1.0", tk.END).strip()} for i in range(9, 27, 2) if self.Text_Data[i].get("1.0", tk.END).strip() != "" and self.Text_Data[i+1].get("1.0", tk.END).strip() != ""}

            # Checks If The ItemAmount Is A Valid Number
            if self.ItemAmount.isdigit() == False:
                self.ItemAmount = 0

            CraftingData = {
                "format_version": "1.20.10",
                "minecraft:recipe_shaped": {
                    "description": {
                        "identifier": self.RecipeId
                    },
                    "tags": [
                        "crafting_table"
                    ],
                    "priority": 0,
                    "pattern": self.Pattern,
                    "key": self.Key,
                    "unlock": [
                        {
                            "context": "AlwaysUnlocked"
                        }
                    ],
                    "result": {
                        "item": self.ItemId,
                        "count": int(self.ItemAmount)
                    }
                }
            }

            FixedFileName = self.RecipeId.replace(":", "_")
            Json_Data = json.dumps(CraftingData, indent=4)
            FileName = os.path.join(Downloads_Folder, f"{FixedFileName}.json")

            # Write JSON Data To A File
            with open(FileName, 'w') as f:
                f.write(Json_Data)
        
        if self.Station == "Furnace":
            
            self.RecipeId = self.Input_Fields.get("recipe_id", tk.Entry()).get().strip() or " "
            self.Input = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Output = self.Text_Data[1].get("1.0", tk.END).strip() or " "

            FuranceData = {
                "format_version": "1.20.10",
                "minecraft:recipe_furnace": {
                    "description": {
                        "identifier": self.RecipeId
                    },
                    "tags": [
                        "furnace"
                    ],
                    "input": self.Input,
                    "output": self.Output,
                }
            }

            FixedFileName = self.RecipeId.replace(":", "_")
            Json_Data = json.dumps(FuranceData, indent=4)
            FileName = os.path.join(Downloads_Folder, f"{FixedFileName}.json")

            # Write JSON Data To A File
            with open(FileName, 'w') as f:
                f.write(Json_Data)
        
        if self.Station == "Brewing Stand":

            self.RecipeId = self.Input_Fields.get("recipe_id", tk.Entry()).get().strip() or " "
            self.Reagent = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Input = self.Text_Data[1].get("1.0", tk.END).strip() or " "
            self.Output = self.Text_Data[2].get("1.0", tk.END).strip() or " "

            BrewingStandData = {
                "format_version": "1.20.10",
                "minecraft:recipe_brewing_container": {
                    "description": {
                        "identifier": self.RecipeId
                    },
                    "tags": [
                        "brewing_stand"
                    ],
                    "reagent": self.Reagent,
                    "input": self.Input,
                    "output": self.Output,
                }
            }
            
            FixedFileName = self.RecipeId.replace(":", "_")
            Json_Data = json.dumps(BrewingStandData, indent=4)
            FileName = os.path.join(Downloads_Folder, f"{FixedFileName}.json")

            # Write JSON Data To A File
            with open(FileName, 'w') as f:
                f.write(Json_Data)

        if self.Current_Station == "Smithing Table Armor Trim":

            self.RecipeId = self.Input_Fields.get("recipe_id", tk.Entry()).get().strip() or " "
            self.Template = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Base = self.Text_Data[1].get("1.0", tk.END).strip() or " "
            self.Addition = self.Text_Data[2].get("1.0", tk.END).strip() or " "
        
            SmithingTableData = {
                "format_version": "1.20.10",
                "minecraft:recipe_smithing_trim": {
                    "description": {
                        "identifier": self.RecipeId
                    },
                    "tags": [
                        "smithing_table"
                    ],
                    "template": self.Template,
                    "base": self.Base,
                    "addition": self.Addition,
                }
            }

            FixedFileName = self.RecipeId.replace(":", "_")
            Json_Data = json.dumps(SmithingTableData, indent=4)
            FileName = os.path.join(Downloads_Folder, f"{FixedFileName}.json")

            # Write JSON Data To A File
            with open(FileName, 'w') as f:
                f.write(Json_Data)

        if self.Current_Station == "Smithing Table Transformation":

            self.RecipeId = self.Input_Fields.get("recipe_id", tk.Entry()).get().strip() or " "
            self.ItemId = self.Input_Fields.get("item_id", tk.Entry()).get().strip() or " "
            self.Template = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Base = self.Text_Data[1].get("1.0", tk.END).strip() or " "
        
            SmithingTableData = {
                "format_version": "1.20.10",
                "minecraft:recipe_smithing_transform": {
                    "description": {
                        "identifier": self.RecipeId
                    },
                    "tags": [
                        "smithing_table"
                    ],
                    "template": self.Template,
                    "base": self.Base,
                    "addition": "minecraft:netherite_ingot",
                    "result": {
                            "item": self.ItemId,
                        }
                    }
                }

            FixedFileName = self.RecipeId.replace(":", "_")
            Json_Data = json.dumps(SmithingTableData, indent=4)
            FileName = os.path.join(Downloads_Folder, f"{FixedFileName}.json")

            # Write JSON Data To A File
            with open(FileName, 'w') as f:
                f.write(Json_Data)

    def Add_Input_Fields(self, Labels):

        # Clear Previous Content
        for Widget in self.Left_Frame.winfo_children():
            Widget.destroy()

        # Clear Existing Input Fields
        self.Input_Fields.clear()

        for Label_Text in Labels:
            
            Box_Frame = tk.Frame(self.Left_Frame, bg="#1E1E1E", border=10, relief=tk.RIDGE)
            Box_Frame.pack(fill="x", padx=10, pady=5)

            Label = tk.Label(Box_Frame, text=Label_Text, bg='#1E1E1E', fg='white', font=self.Custom_Fonts["Minecraft Ten v2"])
            Label.pack(anchor='w', pady=(5, 0))

            Text_Box = tk.Entry(Box_Frame, bg="white", fg="black", font=self.Custom_Fonts["Minecraft Seven v2"])
            Text_Box.pack(fill="x", pady=(0, 5), ipady=3)
            
            # Store the Text_Box in the input_fields dictionary
            self.Input_Fields[Label_Text.lower().replace(" ", "_").replace(":", "")] = Text_Box

    # Function To Setup The Crafting Table Data
    def CraftingTable(self):

        # Clear Previous Content
        for Widget in self.Right_Frame.winfo_children():
            Widget.destroy()

        # Crafting Table Image
        self.Crafting_Table_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Crafting_Table.png")).resize((400, 400))
        self.Crafting_Table_Image = ImageTk.PhotoImage(self.Crafting_Table_File)

        self.Crafting_Table_Label = tk.Label(self.Right_Frame, image=self.Crafting_Table_Image, bg="#2D2D2D")
        self.Crafting_Table_Label.pack(pady=20)

        self.Crafting_Labels["Crafting Table"] = self.Crafting_Table_Label
    
        # Create Crafting Grid
        Grid_Frame = tk.Frame(self.Right_Frame, bg="#53351F", padx=10, pady=10)
        Grid_Frame.pack()

        for Row in range(3):
            for Column in range(3):

                Text_Box = tk.Text(Grid_Frame, wrap=tk.WORD, width=9, height=4, bg="#B07548", font=self.Custom_Fonts["Minecraft Seven v2"])
                Text_Box.grid(row=Row, column=Column, padx=5, pady=5)
                self.Text_Data.append(Text_Box)

        # Add Input Fields To Left_Frame
        self.Add_Input_Fields(["Recipe ID:", "Item ID:", "Item Amount:"])

        Inventory_Outer_Frame = tk.Frame(self.Left_Frame, bg="#4F4F4F", padx=3, pady=3)  # Light gray outer frame
        Inventory_Outer_Frame.pack(pady=10)

        Inventory_Frame = tk.Frame(Inventory_Outer_Frame, bg="#C5C5C5", padx=6, pady=6)  # Darker inner frame
        Inventory_Frame.pack()

        for Row in range(9):
            for Column in range(2):

                Text_Box = tk.Text(Inventory_Frame, wrap=tk.WORD, width=5, height=3, bg="#8B8B8B", font=self.Custom_Fonts["Minecraft Seven v2"])
                Text_Box.grid(row=Row, column=Column, padx=1, pady=2)
                self.Text_Data.append(Text_Box)

    # Function To Setup The Furnace Data
    def Furnace(self):
        
        # Clear Previous Content
        for Widget in self.Right_Frame.winfo_children():
            Widget.destroy()

        # Furance Image
        self.Furnace_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Furnace.png")).resize((400, 400))
        self.Furnace_Image = ImageTk.PhotoImage(self.Furnace_File)
    
        self.Furnace_Label = tk.Label(self.Right_Frame, image=self.Furnace_Image, bg="black")
        self.Furnace_Label.pack(pady=20)

        # Furnace UI Image
        self.Furnace_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Furance_UI.png")).resize((500, 300))
        self.Furnace_UI_Image = ImageTk.PhotoImage(self.Furnace_UI_File)

        self.Furnace_UI_Label = tk.Label(self.Right_Frame, image=self.Furnace_UI_Image, bg="black",)
        self.Furnace_UI_Label.pack(pady=20)

        self.Furnace_Labels["Furnace"] = self.Furnace_Label
        self.Furnace_UI_Labels["Furnace UI"] = self.Furnace_UI_Label

        # Add Input Fields To Left_Frame
        self.Add_Input_Fields(["Recipe ID:"])

        Text_Box = tk.Text(self.Right_Frame, wrap=tk.WORD, width=8, height=4, bg="#8D8D8D")
        Text_Box.place(x=self.Screen_Width - 1400, y=162)
        self.Text_Data.append(Text_Box)

        Text_Box_2 = tk.Text(self.Right_Frame, wrap=tk.WORD, width=11, height=5.5, bg="#8D8D8D")
        Text_Box_2.place(x=self.Screen_Width - 1179, y=216)
        self.Text_Data.append(Text_Box_2)

        self.Furnace_TextBoxes["Textbox 1"] = Text_Box
        self.Furnace_TextBoxes["Textbox 2"] = Text_Box_2
    
    # Function To Setup The Brewing Stand Data
    def BrewingStand(self):
        
        # Clear Previous Content
        for Widget in self.Right_Frame.winfo_children():
            Widget.destroy()

        self.BrewingStand_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Brewing_Stand.png")).resize((400, 400))
        self.BrewingStand_Image = ImageTk.PhotoImage(self.BrewingStand_File)
    
        self.BrewingStand_Label = tk.Label(self.Right_Frame, image=self.BrewingStand_Image, bg="#2D2D2D")
        self.BrewingStand_Label.pack(pady=20)
        
        # Brewing Stand UI Image
        self.BrewingStand_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Brewing_Stand_UI.png")).resize((550, 300))
        self.BrewingStand_UI_Image = ImageTk.PhotoImage(self.BrewingStand_UI_File)

        self.BrewingStand_UI_Label = tk.Label(self.Right_Frame, image=self.BrewingStand_UI_Image, bg="#2D2D2D")
        self.BrewingStand_UI_Label.pack(pady=20)

        # Add to the dictionary
        self.BrewingStand_Labels["Brewing Stand"] = self.BrewingStand_Label
        self.BrewingStand_UI_Labels["Brewing Stand UI"] = self.BrewingStand_UI_Label

        # Add Input Fields To Left_Frame
        self.Add_Input_Fields(["Recipe ID:"])
     
        Text_Box = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box.place(x=self.Screen_Width - 1250, y=165)
        self.Text_Data.append(Text_Box)

        Text_Box_2 = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box_2.place(x=self.Screen_Width - 1475, y=275)
        self.Text_Data.append(Text_Box_2)

        Text_Box_3 = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box_3.place(x=self.Screen_Width - 1035, y=275)
        self.Text_Data.append(Text_Box_3)
        
        self.Brewing_Stand_TextBoxes["Textbox 1"] = Text_Box
        self.Brewing_Stand_TextBoxes["Textbox 2"] = Text_Box_2
        self.Brewing_Stand_TextBoxes["Textbox 3"] = Text_Box_3
   
    # Function To Setup The Smithing Table Trim Data 
    def SmithingTableTrim(self):

        # Clear Previous Content
        for Widget in self.Right_Frame.winfo_children():
            Widget.destroy()

        self.SmithingTableTrim_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Smithing_Table.png")).resize((400, 400))
        self.SmithingTableTrim_Image = ImageTk.PhotoImage(self.SmithingTableTrim_File)
    
        self.SmithingTableTrim_Label = tk.Label(self.Right_Frame, image=self.SmithingTableTrim_Image, bg="black")
        self.SmithingTableTrim_Label.pack(pady=20)

        # Smithing Table Trim UI Image
        self.SmithingTableTrim_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Smithing_Table_Trim_UI.png")).resize((600, 300))
        self.SmithingTableTrim_UI_Image = ImageTk.PhotoImage(self.SmithingTableTrim_UI_File)

        self.SmithingTableTrim_UI_Label = tk.Label(self.Right_Frame, image=self.SmithingTableTrim_UI_Image, bg="black")
        self.SmithingTableTrim_UI_Label.pack(pady=20)

        self.Smithing_Table_Armor_Trim_Labels["Smithing Table Trim"] = self.SmithingTableTrim_Label
        self.Smithing_Table_Armor_Trim_UI_Labels["Smithing Table Trim UI"] = self.SmithingTableTrim_UI_Label

        # Add Input Fields To Left_Frame
        self.Add_Input_Fields(["Recipe ID:"])

        Text_Box = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box.place(x=self.Screen_Width - 1495, y=265)
        self.Text_Data.append(Text_Box)

        Text_Box_2 = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box_2.place(x=self.Screen_Width - 1433, y=265)
        self.Text_Data.append(Text_Box_2)

        Text_Box_3 = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box_3.place(x=self.Screen_Width - 1371, y=265)
        self.Text_Data.append(Text_Box_3)
        
        self.Smithing_Table_Armor_Trim_TextBoxes["Textbox 1"] = Text_Box
        self.Smithing_Table_Armor_Trim_TextBoxes["Textbox 2"] = Text_Box_2
        self.Smithing_Table_Armor_Trim_TextBoxes["Textbox 3"] = Text_Box_3

    # Function To Setup The Smithing Table Transformation Data 
    def SmithingTableTransformation(self):

        # Clear Previous Content
        for Widget in self.Right_Frame.winfo_children():
            Widget.destroy()

        self.SmithingTableTransformation_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Smithing_Table.png")).resize((400, 400))
        self.SmithingTableTransformation_Image = ImageTk.PhotoImage(self.SmithingTableTransformation_File)
    
        self.SmithingTableTransformation_Label = tk.Label(self.Right_Frame, image=self.SmithingTableTransformation_Image, bg="black")
        self.SmithingTableTransformation_Label.pack(pady=20)

        # Smithing Table Transformation UI Image
        self.SmithingTableTransformation_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "App_Recipe_Generator_Textures", "Smithing_Table_Transformation_UI.png")).resize((600, 300))
        self.SmithingTableTransformation_UI_Image = ImageTk.PhotoImage(self.SmithingTableTransformation_UI_File)

        self.SmithingTableTransformation_UI_Label = tk.Label(self.Right_Frame, image=self.SmithingTableTransformation_UI_Image, bg="black")
        self.SmithingTableTransformation_UI_Label.pack(pady=20)

        self.Smithing_Table_Transformation_Labels["Smithing Table Transformation"] = self.SmithingTableTransformation_Label
        self.Smithing_Table_Transformation_UI_Labels["Smithing Table Transformation UI"] = self.SmithingTableTransformation_UI_Label

        # Add Input Fields To Left_Frame
        self.Add_Input_Fields(["Recipe ID:", "Item ID:"])

        Text_Box = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box.place(x=self.Screen_Width - 1495, y=265)
        self.Text_Data.append(Text_Box)

        Text_Box_2 = tk.Text(self.Right_Frame, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
        Text_Box_2.place(x=self.Screen_Width - 1433, y=265)
        self.Text_Data.append(Text_Box_2)
        
        self.Smithing_Table_Transformation_TextBoxes["Textbox 1"] = Text_Box
        self.Smithing_Table_Transformation_TextBoxes["Textbox 2"] = Text_Box_2

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

def Main():
    App = RecipeGenerator()
    App.mainloop()

if __name__ == "__main__":
    Main()