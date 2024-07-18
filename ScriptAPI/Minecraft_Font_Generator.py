import tkinter as tk
from tkinter import filedialog
import tkinter.font as TkFont
from PIL import ImageTk, Image, ImageDraw, ImageDraw2, ImageFont, ImageFilter
import os
from subprocess import call
import ctypes as ct
from tkextrafont import Font
import pygetwindow as gs

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

        # Load Custom Font and Refresh Font List
        self.Load_Custom_Fonts()

        # Update available fonts list
        self.Available_Fonts = self.Custom_Fonts

        # Creates A Button
        self.Create_Buttons()

        # Creates A Dropdown Menu
        self.Create_DropDown()

        # Creates Title Bar Background
        self.Dark_Title_Bar()

        # Create The Background Mosaic
        self.Create_Background_Mosaic()
        
        # Creates Text Preview
        self.Text_Preview()
    
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

    # A Function To Setup The Dropdown Menu
    def Create_DropDown(self):
        
        Font = TkFont.Font(family="HP Simplified Jpan", size=13)

        Dropdown_Selection_Label = tk.Label(self, text="Select Font:", font=Font)
        Dropdown_Selection_Label.config()  
        Dropdown_Selection_Label.place(x=10, y=10)

        self.Selected_Font = tk.StringVar()
        self.Selected_Font.set(self.Available_Fonts[0])

        self.Selection_Dropdown = tk.OptionMenu(self, self.Selected_Font, *self.Available_Fonts)
        self.Selection_Dropdown.place(x=10, y=40)

        self.Color_Label = tk.Label(self, text="Select Color:", font=Font)
        self.Color_Label.place(x=200, y=10)

        self.Color_Options = ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
        self.Selected_Color = tk.StringVar()
        self.Selected_Color.set(self.Color_Options[0])

        self.Color_Dropdown = tk.OptionMenu(self, self.Selected_Color, *self.Color_Options)
        self.Color_Dropdown.place(x=200, y=40)

        self.Border_Color_Label = tk.Label(self, text="Border Color:", font=Font)
        self.Border_Color_Label.place(x=850, y=10)

        self.Border_Color_Options = ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Brown", "Pink", "White", "Gray", "Magenta"]
        self.Selected_Border_Color = tk.StringVar()
        self.Selected_Border_Color.set(self.Border_Color_Options[0])

        self.Border_Color_Dropdown = tk.OptionMenu(self, self.Selected_Border_Color, *self.Border_Color_Options)
        self.Border_Color_Dropdown.place(x=850, y=40)

        self.Size_Font_Sheet_Dropdown_Label = tk.Label(self, text="Select Glyph Size:", font=Font)
        self.Size_Font_Sheet_Dropdown_Label.place(x=1218, y=500)

        self.Size_Font_Sheet_Dropdown_Options = ["128x128", "256x256", "512x512", "1024x1024", "2048x2048"]
        self.Selected_Font_Sheet_Size = tk.StringVar()
        self.Selected_Font_Sheet_Size.set(self.Size_Font_Sheet_Dropdown_Options[0])

        self.Font_Sheet_Size_Dropdown = tk.OptionMenu(self, self.Selected_Font_Sheet_Size, *self.Size_Font_Sheet_Dropdown_Options)
        self.Font_Sheet_Size_Dropdown.place(x=1218, y=550)

        self.Filter_Font_Sheet_Dropdown_Label = tk.Label(self, text="Select Glyph Filter:", font=Font)
        self.Filter_Font_Sheet_Dropdown_Label.place(x=1360, y=500)

        self.Filter_Font_Sheet_Dropdown_Options = ["None", "Sharpen Edge", "Sharpen Edge More", "Detail"]
        self.Selected_Font_Sheet_Filter = tk.StringVar()
        self.Selected_Font_Sheet_Filter.set(self.Filter_Font_Sheet_Dropdown_Options[0])

        self.Filter_Sheet_Size_Dropdown = tk.OptionMenu(self, self.Selected_Font_Sheet_Filter, *self.Filter_Font_Sheet_Dropdown_Options)
        self.Filter_Sheet_Size_Dropdown.place(x=1360, y=550)

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

        ConvertButton = tk.Button(self, text="Convert Font To Minecraft Font Sheet", image=self.Button_Images['default'], command=self.Convert_Font, compound="center", wraplength=200, width=Button_Width, height=Button_Height, highlightthickness=0, bd=0, bg=self.cget('bg'), activebackground=self.cget('bg'), font=Font)
        ConvertButton.place(x=self.Screen_Width - Button_Width - 10, y=self.Screen_Height - 260)

        self.Download_Button = tk.Button(self, text="Download Image", command=self.Download_Image)
        self.Download_Button.place(x=120, y=150)

        ConvertButton.bind("<Enter>", lambda event, b=ConvertButton: self.On_Enter(event, b, 'default'))
        ConvertButton.bind("<Leave>", lambda event, b=ConvertButton: self.On_Leave(event, b, 'default'))

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

    def Load_Custom_Fonts(self):

        self.Custom_Fonts = []

        Font_Directory = os.path.join(self.MasterCraftCurrentDirectory, "Fonts")

        Font_Paths = [
            (os.path.join(Font_Directory, "minecraft-font", "MinecraftRegular-Bmg3.ttf"), "Minecraft Regular"),
            (os.path.join(Font_Directory, "minecraft_evenings", "Minecraft Evenings.ttf"), "Minecraft Evenings"),
            (os.path.join(Font_Directory, "enchantment-proper", "enchantment-proper.ttf"), "Enchantment Proper"),
            (os.path.join(Font_Directory, "minecrafter", "Minecrafter.Reg.ttf"), "Minecrafter"),
            (os.path.join(Font_Directory, "minecrafter", "Minecrafter.Alt.ttf"), "Minecrafter Alt"),
        ]

        for Font_Path, Font_Name in Font_Paths:

            Font(file=Font_Path, family=Font_Name)
            self.Custom_Fonts.append(Font_Name)

    def Text_Preview(self):
        
        Font = TkFont.Font(family="HP Simplified Jpan", size=13)

        self.Text_Entry = tk.Entry(self, font=Font)
        self.Text_Entry.place(x=10, y=120)

        self.Preview_Button = tk.Button(self, text="Update Preview", command=self.Update_Preview)
        self.Preview_Button.place(x=10, y=150)

        self.Preview_Canvas = tk.Canvas(self, bg='white')
        self.Preview_Canvas.place(x=10, y=200)

        self.Size_Entry_Label = tk.Label(self, text="Font Size:", font=TkFont.Font(family="HP Simplified Jpan", size=13))
        self.Size_Entry_Label.place(x=350, y=10)
        
        self.Size_Entry = tk.Entry(self, font=Font)
        self.Size_Entry.place(x=350, y=40)

        self.Border_Size_Label = tk.Label(self, text="Border Size:", font=TkFont.Font(family="HP Simplified Jpan", size=13))
        self.Border_Size_Label.place(x=600, y=10)

        self.Border_Size_Entry = tk.Entry(self, font=Font)
        self.Border_Size_Entry.place(x=600, y=40)

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

        # Clear previous text
        self.Preview_Canvas.delete("all")

        # Create a temporary font to measure text dimensions
        Temp_Font = TkFont.Font(family=Selected_Font, size=Selected_Size)
        Text_Width = Temp_Font.measure(User_Text)
        Text_Height = Temp_Font.metrics("linespace")

        # Resize the canvas to fit the text
        self.Preview_Canvas.config(width=Text_Width + 2 * Border_Size + 2, height=Text_Height + 2 * Border_Size + 2)

        # Draw the border by drawing text multiple times
        X, Y = Border_Size + 2, Border_Size + 1

        for DX in range(-Border_Size, Border_Size + 1):

            for DY in range(-Border_Size, Border_Size + 1):

                if DX != 0 or DY != 0:
                    self.Preview_Canvas.create_text(X + DX, Y + DY, text=User_Text, font=Temp_Font, fill=Border_Color, anchor='nw')

        # Draw the main text
        self.Preview_Canvas.create_text(X, Y, text=User_Text, font=Temp_Font, fill=Selected_Color, anchor='nw')

    def Download_Image(self):

        Download_Image = Image.new("RGBA", (self.Preview_Canvas.winfo_width(), self.Preview_Canvas.winfo_height()), (255, 255, 255, 0))
        ImageDraw2.Draw(Download_Image)

        self.Preview_Canvas.update()

        Downloads_Folder = os.path.join(self.User_Home, "Downloads")
        Temporary_Canvas_Path = os.path.join(Downloads_Folder, "Temporary_Canvas.eps")

        self.Preview_Canvas.postscript(file=Temporary_Canvas_Path, colormode='color')

        print("Image Downloaded As An EPS File")

    def Convert_Font(self):

        FilePath =filedialog.askopenfilename(initialdir=os.path.expanduser("~\\Downloads"), title="Select an TTF file", filetypes=(("TTF files", "*.ttf"), ("all files", "*.*")))

        if not FilePath:
            return

        Downloads_Folder = os.path.join(os.path.expanduser("~"), "Downloads")
        Output_Font_Image_Path = os.path.join(Downloads_Folder, "default8.png")  # Specify output filename

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

        # Create a new blank image with RGBA mode
        Glyph_Image = Image.new('RGBA', Image_Size, (0, 0, 0, 0))

        # Load the font
        Font = ImageFont.truetype(FilePath, Font_Size)

        # Create a drawing context
        Draw = ImageDraw.Draw(Glyph_Image)

        # Define the characters to include (16 characters per line)
        charactersBitMap = (
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

        # Draw each character in the appropriate cell if it has a glyph
        for I, Characters in enumerate(charactersBitMap):

            try:

                # Checks If The Character Has A Glyph
                Font.getmask(Characters)

                # Crea
                Row = I // GlyphColumns
                Column = I % GlyphColumns


                x = Column * Cell_Width - 2
                y = Row * Cell_Height
                Draw.text((x + Cell_Width // 4, y), Characters, font=Font, fill=(255, 255, 255, 255))
            except:
                pass

        # Save The Glyph Image
        Glyph_Image.save(Output_Font_Image_Path)

        # Add Additional Font Filters
        if self.Selected_Font_Sheet_Filter.get() == "Sharpen Edge":

            FontImage = Image.open(Output_Font_Image_Path)

            Enhance = FontImage.filter(ImageFilter.EDGE_ENHANCE)
            Enhance.save(Output_Font_Image_Path)

        if self.Selected_Font_Sheet_Filter.get() == "Sharpen Edge More":

            FontImage = Image.open(Output_Font_Image_Path)

            Enhance = FontImage.filter(ImageFilter.EDGE_ENHANCE)
            Enhance.save(Output_Font_Image_Path) 

        if self.Selected_Font_Sheet_Filter.get() == "Detail":

            FontImage = Image.open(Output_Font_Image_Path)

            Enhance = FontImage.filter(ImageFilter.DETAIL)
            Enhance.save(Output_Font_Image_Path)           
    
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