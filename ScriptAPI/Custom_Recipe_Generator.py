import tkinter as tk
import tkinter.font as TkFont
from tkinter import messagebox
from PIL import ImageTk, Image
from subprocess import call
import json
import os
import ctypes as ct

# Constants
MINIMUM_WINDOW_WIDTH = 600
MINIMUM_WINDOW_HEIGHT = 400

# Recipe Generator Screen
class RecipeGenerator(tk.Tk):
    
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

        # Set Initial Button Array
        self.Buttons = []

        self.Text_Data = []

        # Set The Title Of The Window
        self.title("MasterCraft - Recipe Generator")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "IconImage.ico")
        self.iconbitmap(Icon_Image_Path)

        # Load The Initial Background Image
        BG_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Background.png")
        self.BG_Image = Image.open(BG_Image_Path)
        
        # Create A Label For The Background Image
        self.Background_Label = tk.Label(self)
        self.Background_Label.pack(fill="both", expand=True)
        
        # Stores The Current Station Used
        self.Current_Station = None

        # Creates A Button
        self.Create_Buttons()

        # Creates A Dropdown Menu
        self.Create_DropDown()

        # Creates Title Bar Background
        self.Dark_Title_Bar()

        # Create The Background Mosaic
        self.Create_Background_Mosaic()
        
        # Bind Window Resize Event
        self.bind("<Configure>", self.Resize_Elements)
        
        # Crafting Station Dictionaries

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

    # A Function To Change Title Bar Color To Black
    def Dark_Title_Bar(self):

        self.update()

        Set_Window_Attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        Get_Parent = ct.windll.user32.GetParent
        Hwnd = Get_Parent(self.winfo_id())
        Value = 2
        Value = ct.c_int(Value)
        Set_Window_Attribute(Hwnd, 20, ct.byref(Value), 4)
    
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

    # A Function That Handles UI Resizing
    def Resize_Elements(self, event=None):

        def Resize():

            Current_Width = self.winfo_width()
            Current_Height = self.winfo_height()
            
            if Current_Width < MINIMUM_WINDOW_WIDTH:
                Current_Width = MINIMUM_WINDOW_WIDTH

            if Current_Height < MINIMUM_WINDOW_HEIGHT:
                Current_Height = MINIMUM_WINDOW_HEIGHT

        if hasattr(self, "after_id"):
            self.after_cancel(self.after_id)
        self.after_id = self.after(200, Resize)

    # A Function To Setup The Buttons
    def TextField_Boxes(self):

        self.Text_Frame = tk.Frame(self, bg="#53351F")
        self.Text_Frame.pack()

        Font = TkFont.Font(family="HP Simplified Jpan", size=9)

        if self.Current_Station == "Crafting Table":

            for Row in range(9):
                for Column in range(2):
                    Text_Box = tk.Text(self.Text_Frame, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
                    Text_Box.grid(row=Row, column=Column)
                    self.Text_Data.append(Text_Box)

            self.RecipeIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.RecipeIdTextBox.place(x=200, y=250)
            self.Text_Data.append(self.RecipeIdTextBox)

            self.ItemIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.ItemIdTextBox.place(x=200, y=350)
            self.Text_Data.append(self.ItemIdTextBox)

            self.ItemAmountTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.ItemAmountTextBox.place(x=200, y=450)
            self.Text_Data.append(self.ItemAmountTextBox)

            self.Text_Frame.place(x=10, y=100)

        if self.Current_Station == "Furnace":

            self.RecipeIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.RecipeIdTextBox.place(x=225, y=450)
            self.Text_Data.append(self.RecipeIdTextBox)

            self.ItemIdTextBox = None
            self.ItemAmountTextBox = None

        if self.Current_Station == "Brewing Stand":
            
            self.RecipeIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.RecipeIdTextBox.place(x=280, y=450)
            self.Text_Data.append(self.RecipeIdTextBox)

            self.ItemIdTextBox = None
            self.ItemAmountTextBox = None

        if self.Current_Station == "Smithing Table Armor Trim":

            self.RecipeIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.RecipeIdTextBox.place(x=280, y=450)
            self.Text_Data.append(self.RecipeIdTextBox)

            self.ItemIdTextBox = None
            self.ItemAmountTextBox = None

        if self.Current_Station == "Smithing Table Transformation":

            self.RecipeIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.RecipeIdTextBox.place(x=180, y=450)
            self.Text_Data.append(self.RecipeIdTextBox)

            self.ItemIdTextBox = tk.Text(self, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
            self.ItemIdTextBox.place(x=380, y=450)
            self.Text_Data.append(self.ItemIdTextBox)

            self.ItemAmountTextBox = None

    # A Function To Setup The Dropdown Menu
    def Create_DropDown(self):

        DropDown_Labels = [
            "Crafting Table",
            "Furnace",
            "Brewing Stand",
            "Smithing Table Armor Trim",
            "Smithing Table Transformation"
        ]

        Font = TkFont.Font(family="HP Simplified Jpan", size=13)
        Dropdown_Selection_Label = tk.Label(self, text="Select Table Type:", font=Font)
        Dropdown_Selection_Label.config()  
        Dropdown_Selection_Label.place(x=10, y=10)

        Selected_Table = tk.StringVar()
        Selected_Table.set(DropDown_Labels[0])
        
        selection_dropdown = tk.OptionMenu(self, Selected_Table, *DropDown_Labels, command=lambda selection: self.CraftingStation(selection))
        selection_dropdown.place(x=10, y=40)

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
        RecipeButton = tk.Button(self, text="Generate Recipe", image=self.Button_Images['default'], command=self.CraftingMake, compound="center", wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font=Font)
        RecipeButton.place(x=self.Screen_Width - Button_Width - 10, y=self.Screen_Height - 260)
        self.Buttons.append(RecipeButton)

        BackButton = tk.Button(self, text="Back", image=self.Button_Images['default'], command=self.Return, compound="center", wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font=Font)
        BackButton.place(x=self.Screen_Width - Button_Width - 10, y=self.Screen_Height - 160)

        RecipeButton.bind("<Enter>", lambda event, b=RecipeButton: self.On_Enter(event, b, 'default'))
        RecipeButton.bind("<Leave>", lambda event, b=RecipeButton: self.On_Leave(event, b, 'default'))

        BackButton.bind("<Enter>", lambda event, b=BackButton: self.On_Enter(event, b, 'default'))
        BackButton.bind("<Leave>", lambda event, b=BackButton: self.On_Leave(event, b, 'default'))

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

    def Destroy_TextFieldBoxes(self):

        if hasattr(self, 'Text_Frame') and self.Text_Frame:

            if self.Text_Frame:
                self.Text_Frame.place_forget()

            if self.RecipeIdTextBox:
                self.RecipeIdTextBox.place_forget()

            if self.ItemIdTextBox:
                self.ItemIdTextBox.place_forget()

            if self.ItemAmountTextBox:
                self.ItemAmountTextBox.place_forget()

            self.Text_Frame = None

    # A List Of Functions For Each Crafting Station
    def CraftingStation(self, Selection):
        
        self.Current_Station = Selection

        # Removes TectField Boxes
        self.Destroy_TextFieldBoxes()

        self.Text_Data = []
        
        # Creates TextField Boxes
        self.TextField_Boxes()

        # Remove All Other Crafting Stations If Not Selected
        self.CraftingStationRemove(Selection)

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
            return messagebox.askokcancel(title="MasterCraft Error Menu", message="Error- Encounter Script Error. Cannonot Find Current Station Being Used. Please Select A Station To Resolve This Error")

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

            self.RecipeId = self.Text_Data[18].get("1.0", tk.END).strip() or " "
            self.Pattern = ["".join([self.Text_Data[i].get("1.0", tk.END).strip() or " " for i in range(Start, Start + 3)]) for Start in range(21, 30, 3)]       
            self.Key = {self.Text_Data[i+1].get("1.0", tk.END).strip(): {"item": self.Text_Data[i].get("1.0", tk.END).strip()} for i in range(0, len(self.Text_Data)-12, 2) if self.Text_Data[i].get("1.0", tk.END).strip() != "" and self.Text_Data[i+1].get("1.0", tk.END).strip() != ""}
            self.ItemId = self.Text_Data[19].get("1.0", tk.END).strip() or " "
            self.ItemAmount = self.Text_Data[20].get("1.0", tk.END).strip() or " "

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
            
            self.RecipeId = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Input = self.Text_Data[1].get("1.0", tk.END).strip() or " "
            self.Output = self.Text_Data[2].get("1.0", tk.END).strip() or " "

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

            self.RecipeId = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Reagent = self.Text_Data[1].get("1.0", tk.END).strip() or " "
            self.Input = self.Text_Data[2].get("1.0", tk.END).strip() or " "
            self.Output = self.Text_Data[3].get("1.0", tk.END).strip() or " "

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

            self.RecipeId = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.Template = self.Text_Data[1].get("1.0", tk.END).strip() or " "
            self.Base = self.Text_Data[2].get("1.0", tk.END).strip() or " "
            self.Addition = self.Text_Data[3].get("1.0", tk.END).strip() or " "
        
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

            self.RecipeId = self.Text_Data[0].get("1.0", tk.END).strip() or " "
            self.ItemId = self.Text_Data[1].get("1.0", tk.END).strip() or " "
            self.Template = self.Text_Data[2].get("1.0", tk.END).strip() or " "
            self.Base = self.Text_Data[3].get("1.0", tk.END).strip() or " "
        
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
  
    # A Function To Remove Crafting Station Assets
    def CraftingStationRemove(self, Current_Station):

        for Station, Label in self.Crafting_Labels.items():

            if Station != Current_Station:
                if Label:
                    Label.place_forget()

            if self.Crafting_Grid_Frame:
                self.Crafting_Grid_Frame.place_forget()

        for Station, Label in self.Furnace_Labels.items():

            if Station != Current_Station:
                if Label:
                    Label.place_forget()

            for Station, Label in self.Furnace_UI_Labels.items():
                if Station != Current_Station:
                    if Label:
                        Label.place_forget()

            if self.Furnace_TextBoxes:
                for TextBoxes in self.Furnace_TextBoxes.values():
                    TextBoxes.place_forget()

        for Station, Label in self.BrewingStand_Labels.items():

            if Station != Current_Station:
                if Label:
                    Label.place_forget()

            for Station, Label in self.BrewingStand_UI_Labels.items():
                if Station != Current_Station:
                    if Label:
                        Label.place_forget()
            
            if self.Brewing_Stand_TextBoxes:
                for TextBoxes in self.Brewing_Stand_TextBoxes.values():
                    TextBoxes.place_forget()

        
        for Station, Label in self.Smithing_Table_Armor_Trim_Labels.items():

            if Station != Current_Station:
                if Label:
                    Label.place_forget()

            for Station, Label in self.Smithing_Table_Armor_Trim_UI_Labels.items():
                if Station != Current_Station:
                    if Label:
                        Label.place_forget()
            
            if self.Smithing_Table_Armor_Trim_TextBoxes:
                for TextBoxes in self.Smithing_Table_Armor_Trim_TextBoxes.values():
                    TextBoxes.place_forget()

        for Station, Label in self.Smithing_Table_Transformation_Labels.items():

            if Station != Current_Station:
                if Label:
                    Label.place_forget()

            for Station, Label in self.Smithing_Table_Transformation_UI_Labels.items():
                if Station != Current_Station:
                    if Label:
                        Label.place_forget()
            
            if self.Smithing_Table_Transformation_TextBoxes:
                for TextBoxes in self.Smithing_Table_Transformation_TextBoxes.values():
                    TextBoxes.place_forget()

    # Function To Setup The Crafting Table Data
    def CraftingTable(self):

        self.Crafting_Table_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Crafting_Table.png")).resize((600, 600))
        self.Crafting_Table_Image = ImageTk.PhotoImage(self.Crafting_Table_File)

        self.Crafting_Table_Label = tk.Label(self, image=self.Crafting_Table_Image, bg="black")
        self.Crafting_Table_Label.place(x=self.Screen_Width - 600, y=0)

        self.Crafting_Labels["Crafting Table"] = self.Crafting_Table_Label
        
        # A Function That Creates Crafting Table Grid
        def Crafting_Grid():

            self.Crafting_Grid_Frame = tk.Frame(self, bg="#53351F")
            self.Crafting_Grid_Frame.pack()

            for Row in range(3):
                for Column in range(3):
                    Text_Box = tk.Text(self.Crafting_Grid_Frame, wrap=tk.WORD, width=10, height=5, bg="#AE8E57")
                    Text_Box.grid(row=Row, column=Column, padx=10, pady=10)
                    self.Text_Data.append(Text_Box)

            self.Crafting_Grid_Frame.place(x=self.Screen_Width - 455, y=145)
        
        Crafting_Grid()

    # Function To Setup The Furnace Data
    def Furnace(self):
        
        # Furance Image
        self.Furnace_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Furnace.png")).resize((600, 600))
        self.Furnace_Image = ImageTk.PhotoImage(self.Furnace_File)
    
        self.Furnace_Label = tk.Label(self, image=self.Furnace_Image, bg="black")
        self.Furnace_Label.place(x=self.Screen_Width - 600, y=0)

        # Furnace UI Image
        self.Furnace_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Furance_UI.png")).resize((500, 300))
        self.Furnace_UI_Image = ImageTk.PhotoImage(self.Furnace_UI_File)

        self.Furnace_UI_Label = tk.Label(self, image=self.Furnace_UI_Image, bg="black")
        self.Furnace_UI_Label.place(x=self.Screen_Width - 1524, y=100)

        self.Furnace_Labels["Furnace"] = self.Furnace_Label
        self.Furnace_UI_Labels["Furnace UI"] = self.Furnace_UI_Label

        # Function to create furnace grid
        def Furnace_Grid():

            Text_Box = tk.Text(self, wrap=tk.WORD, width=8, height=4, bg="#8D8D8D")
            Text_Box.place(x=self.Screen_Width - 1400, y=162)
            self.Text_Data.append(Text_Box)

            Text_Box_2 = tk.Text(self, wrap=tk.WORD, width=11, height=5.5, bg="#8D8D8D")
            Text_Box_2.place(x=self.Screen_Width - 1179, y=216)
            self.Text_Data.append(Text_Box_2)

            self.Furnace_TextBoxes["Textbox 1"] = Text_Box
            self.Furnace_TextBoxes["Textbox 2"] = Text_Box_2

        Furnace_Grid()
    
    # Function To Setup The Brewing Stand Data
    def BrewingStand(self):
        
        self.BrewingStand_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Brewing_Stand.png")).resize((600, 600))
        self.BrewingStand_Image = ImageTk.PhotoImage(self.BrewingStand_File)
    
        self.BrewingStand_Label = tk.Label(self, image=self.BrewingStand_Image, bg="black")
        self.BrewingStand_Label.place(x=self.Screen_Width - 600, y=0)
        
        # Brewing Stand UI Image
        self.BrewingStand_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Brewing_Stand_UI.png")).resize((600, 300))
        self.BrewingStand_UI_Image = ImageTk.PhotoImage(self.BrewingStand_UI_File)

        self.BrewingStand_UI_Label = tk.Label(self, image=self.BrewingStand_UI_Image, bg="black")
        self.BrewingStand_UI_Label.place(x=self.Screen_Width - 1524, y=100)

        # Add to the dictionary
        self.BrewingStand_Labels["Brewing Stand"] = self.BrewingStand_Label
        self.BrewingStand_UI_Labels["Brewing Stand UI"] = self.BrewingStand_UI_Label

        def Brewing_Stand_Grid():
            
            Text_Box = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box.place(x=self.Screen_Width - 1250, y=165)
            self.Text_Data.append(Text_Box)

            Text_Box_2 = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box_2.place(x=self.Screen_Width - 1475, y=275)
            self.Text_Data.append(Text_Box_2)

            Text_Box_3 = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box_3.place(x=self.Screen_Width - 1035, y=275)
            self.Text_Data.append(Text_Box_3)
            
            self.Brewing_Stand_TextBoxes["Textbox 1"] = Text_Box
            self.Brewing_Stand_TextBoxes["Textbox 2"] = Text_Box_2
            self.Brewing_Stand_TextBoxes["Textbox 3"] = Text_Box_3

        Brewing_Stand_Grid()
    
    # Function To Setup The Smithing Table Trim Data 
    def SmithingTableTrim(self):

        self.SmithingTableTrim_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Smithing_Table.png")).resize((600, 600))
        self.SmithingTableTrim_Image = ImageTk.PhotoImage(self.SmithingTableTrim_File)
    
        self.SmithingTableTrim_Label = tk.Label(self, image=self.SmithingTableTrim_Image, bg="black")
        self.SmithingTableTrim_Label.place(x=self.Screen_Width - 600, y=0)

        # Smithing Table Trim UI Image
        self.SmithingTableTrim_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Smithing_Table_Trim_UI.png")).resize((600, 300))
        self.SmithingTableTrim_UI_Image = ImageTk.PhotoImage(self.SmithingTableTrim_UI_File)

        self.SmithingTableTrim_UI_Label = tk.Label(self, image=self.SmithingTableTrim_UI_Image, bg="black")
        self.SmithingTableTrim_UI_Label.place(x=self.Screen_Width - 1524, y=100)

        # Add to the dictionary
        self.Smithing_Table_Armor_Trim_Labels["Smithing Table Trim"] = self.SmithingTableTrim_Label
        self.Smithing_Table_Armor_Trim_UI_Labels["Smithing Table Trim UI"] = self.SmithingTableTrim_UI_Label

        def Smithing_Table_Trim_Grid():
            
            Text_Box = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box.place(x=self.Screen_Width - 1495, y=265)
            self.Text_Data.append(Text_Box)

            Text_Box_2 = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box_2.place(x=self.Screen_Width - 1433, y=265)
            self.Text_Data.append(Text_Box_2)

            Text_Box_3 = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box_3.place(x=self.Screen_Width - 1371, y=265)
            self.Text_Data.append(Text_Box_3)
            
            self.Smithing_Table_Armor_Trim_TextBoxes["Textbox 1"] = Text_Box
            self.Smithing_Table_Armor_Trim_TextBoxes["Textbox 2"] = Text_Box_2
            self.Smithing_Table_Armor_Trim_TextBoxes["Textbox 3"] = Text_Box_3

        Smithing_Table_Trim_Grid()

    # Function To Setup The Smithing Table Transformation Data 
    def SmithingTableTransformation(self):
        
        self.SmithingTableTransformation_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Smithing_Table.png")).resize((600, 600))
        self.SmithingTableTransformation_Image = ImageTk.PhotoImage(self.SmithingTableTransformation_File)
    
        self.SmithingTableTransformation_Label = tk.Label(self, image=self.SmithingTableTransformation_Image, bg="black")
        self.SmithingTableTransformation_Label.place(x=self.Screen_Width - 600, y=0)

        # Smithing Table Transformation UI Image
        self.SmithingTableTransformation_UI_File = Image.open(os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Smithing_Table_Transformation_UI.png")).resize((600, 300))
        self.SmithingTableTransformation_UI_Image = ImageTk.PhotoImage(self.SmithingTableTransformation_UI_File)

        self.SmithingTableTransformation_UI_Label = tk.Label(self, image=self.SmithingTableTransformation_UI_Image, bg="black")
        self.SmithingTableTransformation_UI_Label.place(x=self.Screen_Width - 1524, y=100)

        # Add to the dictionary
        self.Smithing_Table_Transformation_Labels["Smithing Table Transformation"] = self.SmithingTableTransformation_Label
        self.Smithing_Table_Transformation_UI_Labels["Smithing Table Transformation UI"] = self.SmithingTableTransformation_UI_Label

        def Smithing_Table_Transformation_Grid():
            
            Text_Box = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box.place(x=self.Screen_Width - 1495, y=265)
            self.Text_Data.append(Text_Box)

            Text_Box_2 = tk.Text(self, wrap=tk.WORD, width=6, height=3, bg="#8D8D8D")
            Text_Box_2.place(x=self.Screen_Width - 1433, y=265)
            self.Text_Data.append(Text_Box_2)
            
            self.Smithing_Table_Transformation_TextBoxes["Textbox 1"] = Text_Box
            self.Smithing_Table_Transformation_TextBoxes["Textbox 2"] = Text_Box_2

        Smithing_Table_Transformation_Grid()

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
    App = RecipeGenerator()
    App.mainloop()

if __name__ == "__main__":
    Main()