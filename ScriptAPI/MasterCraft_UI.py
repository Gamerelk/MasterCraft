import tkinter as tk
import tkinter.font as TkFont
from PIL import ImageTk, Image
import os
from subprocess import call
import ctypes as ct

# Constants
MINIMUM_WINDOW_WIDTH = 600
MINIMUM_WINDOW_HEIGHT = 400
BUTTON_SPACING = 1.7
NUM_BUTTONS = 6

# MasterCraft Screen
class MasterCraftApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Getting User Pathway
        self.User_Home = os.path.expanduser("~")
        self.InitialDirectory = '/'
        self.DirectoryName ='MasterCraft'
        self.MasterCraftCurrentDirectory = os.path.normpath(f"{self.SearchDirectory()}")[2: -2]
        
        # Set Initial Window Size
        self.Screen_Width = self.winfo_screenwidth()
        self.Screen_Height = self.winfo_screenheight()
        self.geometry(f"{self.Screen_Width}x{self.Screen_Height}")

        # Set Initial Button Array
        self.Buttons = []

        # Set Selected Button Data
        self.SelectedButton = None

        # Set The Title Of The Window
        self.title("MasterCraft")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "IconImage.ico")
        self.iconbitmap(Icon_Image_Path)

        # Load The Initial Background Image
        BG_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Background.png")
        self.BG_Image = Image.open(BG_Image_Path)
        
        # Create A Label For The Background Image
        self.Background_Label = tk.Label(self)
        self.Background_Label.pack(fill="both", expand=True)
        
        # Create Buttons
        self.Create_Buttons()

        # Creates Title Bar Background
        self.Dark_Title_Bar()

        # Create The Background Mosaic
        self.Create_Background_Mosaic()
        
        # Bind Window Resize Event
        self.bind("<Configure>", self.Resize_Elements)
    
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
        Set_Window_Attribute(Hwnd, 20, ct.byref(Value),4)
    
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
            
            Button_Width_Ratio = int(Current_Width / 5)
            Button_Height_Ratio = int(Current_Height / 11)
            
            # Resize Buttons
            for i, Button in enumerate(self.Buttons):
                
                Button_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "ButtonBackground.png")
                Button_Image = Image.open(Button_Image_Path).resize((Button_Width_Ratio, Button_Height_Ratio))
                Button_Photo = ImageTk.PhotoImage(Button_Image)
                self.Button_Images['default'][i] = Button_Photo

                Button_Hover_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "SelectedBackground.png")
                Button_Hover_Image = Image.open(Button_Hover_Image_Path).resize((Button_Width_Ratio, Button_Height_Ratio))
                Button_Hover_Photo = ImageTk.PhotoImage(Button_Hover_Image)
                self.Button_Images['hover'][i] = Button_Hover_Photo

                Button.config(image=Button_Photo)
                Button.image = Button_Photo
                Button.config(width=Button_Width_Ratio, height=Button_Height_Ratio)

                Button.place(relx=0, rely=(i)/(NUM_BUTTONS * BUTTON_SPACING))

        if hasattr(self, "after_id"):
            self.after_cancel(self.after_id)
        self.after_id = self.after(200, Resize)

    # A Function To Setup The Buttons
    def Create_Buttons(self):

        Button_Actions = [
            self.OBJ_To_JSON_Converter,
            self.Recipe_Generator,
            self.Font_Generator,
            self.Manifest_Generator,
            self.Button_6,
            self.Vanilla_Templates
        ]

        Button_Labels = [
            "Object To Json Model Converter",
            "Recipe Generator",
            "Minecraft Font Generator",
            "Minecraft Manifest Generator",
            "Button 5 But Written As 6",
            "Minecraft Vanilla Templates"
        ]

        self.Button_Images = {
            'default': {},
            'hover': {}
        }
    
        Button_Width = int(self.Screen_Width / 5)
        Button_Height = int(self.Screen_Height / 11)

        for i in range(NUM_BUTTONS):

            Button_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "ButtonBackground.png")
            Button_Hover_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "SelectedBackground.png")

            Button_Image = Image.open(Button_Image_Path).resize((Button_Width, Button_Height))
            Button_Hover_Image = Image.open(Button_Hover_Image_Path).resize((Button_Width, Button_Height))

            Button_Photo = ImageTk.PhotoImage(Button_Image)
            Button_Hover_Photo = ImageTk.PhotoImage(Button_Hover_Image)

            self.Button_Images['default'][i] = Button_Photo
            self.Button_Images['hover'][i] = Button_Hover_Photo

            Font = TkFont.Font(family="HP Simplified Jpan" , size=16)
            Button = tk.Button(self, text=Button_Labels[i], image=Button_Photo, compound="center", command=Button_Actions[i], wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font = Font)
            Button.image = Button_Photo  # Keep a reference to avoid garbage collection
            self.Buttons.append(Button)
            Button.pack()
            Button.bind("<Enter>", lambda event, b=Button, i=i: self.On_Enter(event, b, i))
            Button.bind("<Leave>", lambda event, b=Button, i=i: self.On_Leave(event, b, i))

    # A List Of Functions For Each Button
    def OBJ_To_JSON_Converter(self):

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "ScriptAPI", "OBJ_To_JSON_Beta.py")
        call(["python", Script_Path])
        
    def Recipe_Generator(self):

        Selected = "Recipe Generator"
        self.destroy()
        ReturnSequence(Selected)

    def Font_Generator(self):
        
        Selected = "Font Generator"
        self.destroy()
        ReturnSequence(Selected)

    def Manifest_Generator(self):

        Selected = "Manifest Generator"
        self.destroy()
        ReturnSequence(Selected)

    def Button_6(self):
        print("s")

    def Vanilla_Templates(self):
        print("Button 5 was pressed")

    # A Functions That Handles Switching The Button Hover Event
    def On_Enter(self, event, Button, index):
        Button.config(image=self.Button_Images['hover'][index])

    def On_Leave(self, event, Button, index):
        Button.config(image=self.Button_Images['default'][index])

def ReturnSequence(Selection):

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

        if Selection == "Recipe Generator":
            Script_Path = os.path.join(MasterCraftCurrentDirectory, "ScriptAPI", "Custom_Recipe_Generator.py")
            call(["python", Script_Path])

        if Selection == "Font Generator":
            Script_Path = os.path.join(MasterCraftCurrentDirectory, "ScriptAPI", "Minecraft_Font_Generator.py")
            call(["python", Script_Path])

        if Selection == "Manifest Generator":
            Script_Path = os.path.join(MasterCraftCurrentDirectory, "ScriptAPI", "Minecraft_Manifest_Generator.py")
            call(["python", Script_Path])

def Main():
    App = MasterCraftApp()
    App.mainloop()

if __name__ == "__main__":
    Main()