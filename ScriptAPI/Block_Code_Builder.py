import tkinter as tk
from tkinter import filedialog
import tkinter.font as TkFont
from PIL import ImageTk, Image, ImageDraw, ImageDraw2, ImageFont, ImageFilter
import os
from subprocess import call
import ctypes as ct

# Constants
MINIMUM_WINDOW_WIDTH = 600
MINIMUM_WINDOW_HEIGHT = 400

# Font Generator Screen
class FontGenerator(tk.Tk):

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

        # Set Selected Button Data
        self.SelectedButton = None

        # Set The Title Of The Window
        self.title("MasterCraft - Font Generator")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "IconImage.ico")
        self.iconbitmap(Icon_Image_Path)

        # Load The Initial Background Image
        BG_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Background.png")
        self.BG_Image = Image.open(BG_Image_Path)
        
        # Create A Label For The Background Image
        self.Background_Label = tk.Label(self)
        self.Background_Label.pack(fill="both", expand=True)

        # Creates Scrolling
        self.Create_Scroll()

        # Creates Buttons
        self.Create_Buttons()

        # Creates Code Blocks
        self.Code_Blocks()

        # Creates Title Bar Background
        self.Dark_Title_Bar()

        # Create The Background Mosaic
        self.Create_Background_Mosaic()
    
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

    def Create_Scroll(self):

        Font = TkFont.Font(family="Helvetica", size=12)

        Frame = tk.Frame(self)
        Frame.place(x=727, y=0, width=800, height=600)
        
        self.Code_Text = tk.Text(Frame, wrap=tk.WORD, width=11, height=4, bg="#8D8D8D", font=Font)
        self.Code_Text.config(state='disabled')
        self.Code_Text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.Scrollbar = tk.Scrollbar(Frame, orient='vertical', command=self.Code_Text.yview)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.Code_Text.config(yscrollcommand=self.Scrollbar.set)

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

        BackButton = tk.Button(self, text="Back", image=self.Button_Images['default'], command=self.Return, compound="center", wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font=Font)
        BackButton.place(x=self.Screen_Width - Button_Width - 10, y=self.Screen_Height - 160)

        BackButton.bind("<Enter>", lambda event, b=BackButton: self.On_Enter(event, b, 'default'))
        BackButton.bind("<Leave>", lambda event, b=BackButton: self.On_Leave(event, b, 'default'))

    def Code_Blocks(self):
        
        # Class Block Image
        Class_Block_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "Textures", "Code_Block_Textures", "Class_Event_Block.png")
        self.Class_Block_Image = ImageTk.PhotoImage(Image.open(Class_Block_Image_Path))

        World_Block = tk.Label(self, image=self.Class_Block_Image)
        World_Block.place(x=0,y=0)

        World_Block.bind("<Button-1>", self.Drag_Position)
        World_Block.bind("<B1-Motion>", self.Drag)

    def On_Enter(self, event, Button, state):
        if state == 'default':
            Button.config(image=self.Button_Images['hover'])

    def On_Leave(self, event, Button, state):
        if state == 'default':
            Button.config(image=self.Button_Images['default'])

    def Drag_Position(self, event):

        Object=event.widget
        Object.startX=event.x
        Object.startY=event.y

    def Drag(self, event):

        Object=event.widget
        x=Object.winfo_x() - Object.startX+event.x
        y=Object.winfo_y() - Object.startY+event.y
        Object.place(x=x,y=y)

    # A Function To Close This Window And Return To MasterCraft UI
    def Return(self):
        self.destroy()
        ReturnSequence()

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
    App = FontGenerator()
    App.mainloop()

if __name__ == "__main__":
    Main()