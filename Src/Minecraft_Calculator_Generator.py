import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as TkFont
from tkextrafont import Font
from PIL import ImageTk, Image
import subprocess
import time
import pygame
import math

class MinecraftCalculatorGenerator(tk.Tk):

    def __init__(self):
        super().__init__()

        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Initialize Calculator Variables
        self.Current_Input = tk.StringVar(value="0")
        self.Operation = None
        self.First_Number = None
        self.Calculator_Mode = tk.StringVar(value="Minecraft Basic")

        # Creating Minecraft Calculator UI  
        self.Create_UI()

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
        
        # List Of Custom Sounds
        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Button"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Operation"),
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

    def Play_Sound(self, Sound_Name):

        Sound = self.Sounds.get(Sound_Name)

        if Sound:
            Sound.play()

    def Create_UI(self):

        # Set Window Title
        self.title("MasterCraft - Calculator")

        # Set The Main Window Color
        self.configure(bg="#2B2B2B")

        # Set Window Icon
        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Path)

        # Sets The Size Of The Window
        self.geometry("350x500")

        # Create Header Frame
        Header_Frame = tk.Frame(self, bg='#4C4C4C')
        Header_Frame.pack(fill=tk.X)

        Title_Label = tk.Label(Header_Frame, text="CALCULATOR", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Create Dropdown For Calculator Mode
        Mode_Dropdown = ttk.Combobox(Header_Frame, textvariable=self.Calculator_Mode, values=["Minecraft Basic", "Minecraft Scientific"], state="readonly", font=self.Custom_Fonts["Minecraft Seven v2"])
        Mode_Dropdown.pack(side=tk.RIGHT, padx=10, pady=5)
        Mode_Dropdown.bind("<<ComboboxSelected>>", self.Change_Calculator_Mode)

        # Create Main Frame
        self.Main_Frame = tk.Frame(self, bg='#3C3F41')
        self.Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.Create_Basic_Calculator()

    def Create_Basic_Calculator(self):

        for Widget in self.Main_Frame.winfo_children():
            Widget.destroy()

        # Create Display
        Display_Frame = tk.Frame(self.Main_Frame, bg='#2B2B2B', bd=4, relief=tk.SUNKEN)
        Display_Frame.pack(fill=tk.X, pady=(0, 10))

        Display = tk.Label(Display_Frame, textvariable=self.Current_Input, font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white', anchor='e', padx=10, pady=10)
        Display.pack(fill=tk.X)

        # Create Button Grid
        Button_Frame = tk.Frame(self.Main_Frame, bg='#2B2B2B')
        Button_Frame.pack()

        Buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        Row = 0
        Column = 0

        for Button in Buttons:

            Function = lambda x=Button: self.Click(x)
            CalculatorButton = tk.Button(Button_Frame, text=Button, command=Function, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white', width=5, height=2)
            CalculatorButton.grid(row=Row, column=Column, padx=2, pady=2)

            CalculatorButton.bind("<Enter>", lambda e, ButtonPress=CalculatorButton: ButtonPress.config(bg='#6C6C6C'))
            CalculatorButton.bind("<Leave>", lambda e, ButtonPress=CalculatorButton: ButtonPress.config(bg='#4C4C4C'))

            Column += 1

            if Column > 3:

                Column = 0
                Row += 1

        # Create Back Button
        Back_Button = tk.Button(self.Main_Frame, text="Back", command=self.Show_MasterCraftMainScreen, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white')
        Back_Button.pack(pady=(10, 0))

    def Create_Scientific_Calculator(self):

        for Widget in self.Main_Frame.winfo_children():
            Widget.destroy()

        # Create Display
        Display_Frame = tk.Frame(self.Main_Frame, bg='#2B2B2B', bd=4, relief=tk.SUNKEN)
        Display_Frame.pack(fill=tk.X, pady=(0, 10))

        Display = tk.Label(Display_Frame, textvariable=self.Current_Input, font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white', anchor='e', padx=10, pady=10)
        Display.pack(fill=tk.X)

        # Create Button Grid
        Button_Frame = tk.Frame(self.Main_Frame, bg='#2B2B2B')
        Button_Frame.pack()

        Buttons = [
            'KB1', 'KB2', 'SB', 'CE', '/',
            '7', '8', '9', 'OW', '*',
            '4', '5', '6', 'NE', '-',
            '1', '2', '3', '(', '+',
            '0', '.', '=', ')', 'C',
            'FT', 'FD'
        ]

        Row = 0
        Column = 0

        for Button in Buttons:

            Function = lambda x=Button: self.Scientific_Click(x)
            CalculatorButton = tk.Button(Button_Frame, text=Button, command=Function, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white', width=5, height=2)
            CalculatorButton.grid(row=Row, column=Column, padx=2, pady=2)

            CalculatorButton.bind("<Enter>", lambda e, ButtonPress=CalculatorButton: ButtonPress.config(bg='#6C6C6C'))
            CalculatorButton.bind("<Leave>", lambda e, ButtonPress=CalculatorButton: ButtonPress.config(bg='#4C4C4C'))

            Column += 1

            if Column > 4:
                Column = 0
                Row += 1

        # Create Back Button
        Back_Button = tk.Button(self.Main_Frame, text="Back", command=self.Show_MasterCraftMainScreen, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white')
        Back_Button.pack(pady=(10, 0))

    def Change_Calculator_Mode(self, event):

        if self.Calculator_Mode.get() == "Minecraft Basic":
            self.Create_Basic_Calculator()
        else:
            self.Create_Scientific_Calculator()

    def Scientific_Click(self, Key):

        if Key in ['KB1', 'KB2', 'SB', 'OW', 'NE', 'FT', 'FD']:

            self.Play_Sound("Operation")

            if Key == 'KB1':
                Result = self.ApplyKnockBackOriginalQuadraticEquation(float(self.Current_Input.get()))

            elif Key == 'KB2':
                Result = self.ApplyKnockBackRootQuadraticEquation(float(self.Current_Input.get()))

            elif Key == 'SB':
                Result = self.SlimeBounceLogarithmicEquation(float(self.Current_Input.get()))

            elif Key in ['OW', 'NE']:
                self.Show_Coordinate_Input_Dialog(Key)
                return

            elif Key == 'FT':
                Result = self.BlockFallTime(float(self.Current_Input.get()))

            elif Key == 'FD':
                Result = self.BlockFallDamage(float(self.Current_Input.get()))

            self.Current_Input.set(str(Result))

        elif Key == 'CE':

            self.Play_Sound("Button")
            self.Current_Input.set("0")
            self.Operation = None
            self.First_Number = None

        elif Key == 'C':

            self.Play_Sound("Button")
            current = self.Current_Input.get()
            self.Current_Input.set(current[:-1] if len(current) > 1 else "0")
            
        else:
            self.Click(Key)

    def Show_Coordinate_Input_Dialog(self, Conversion_Type):

        Dialog = tk.Toplevel(self)

        Dialog.title("Enter Coordinates")

        Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        Dialog.iconbitmap(Icon_Path)

        Dialog.iconbitmap()
        Dialog.geometry("300x280")
        Dialog.configure(bg='#2B2B2B')

        tk.Label(Dialog, text="Enter Coordinates", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#2B2B2B', fg='white').pack(pady=10)

        Entry_Frame = tk.Frame(Dialog, bg='#2B2B2B')
        Entry_Frame.pack(pady=10)

        Entries = []

        for Label in ['X:', 'Y:', 'Z:']:

            tk.Label(Entry_Frame, text=Label, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#2B2B2B', fg='white').pack()
            Entry = tk.Entry(Entry_Frame, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white', insertbackground='white')
            Entry.pack(pady=5)
            Entries.append(Entry)

        def Convert():

            try:

                X, Y, Z = [float(Entry.get()) for Entry in Entries]

                if Conversion_Type == 'OW':

                    Result = self.OverWorldToNetherConverter(X, Y, Z)
                else:

                    Result = self.NetherToOverWorldConverter(X, Y, Z)

                self.Current_Input.set(f"({Result[0]}, {Result[1]}, {Result[2]})")
                Dialog.destroy()

            except ValueError:
                tk.messagebox.showerror("Error", "Invalid input. Please enter numbers only.")

        tk.Button(Dialog, text="Convert", command=Convert, font=self.Custom_Fonts["Minecraft Seven v2"], bg='#4C4C4C', fg='white').pack(pady=10)
        
    def OverWorldToNetherConverter(self, CoordinateX, CoordinateY, CoordinateZ):

        X = math.ceil(CoordinateX / 8)
        Y = CoordinateY 
        Z = math.ceil(CoordinateZ / 8)
        return X, Y, Z

    def NetherToOverWorldConverter(self, CoordinateX, CoordinateY, CoordinateZ):

        X = math.ceil(CoordinateX * 8)
        Y = CoordinateY 
        Z = math.ceil(CoordinateZ * 8)
        return X, Y, Z

    def ApplyKnockBackOriginalQuadraticEquation(self, Value):

        X = Value
        KnockBackDistance = 2.03660714 * X ** 2 + 8.46803571 * X - 5.856
        return KnockBackDistance

    def ApplyKnockBackRootQuadraticEquation(self, Value):

        X = Value
        KnockAPIValue = (-8.46803571 + math.sqrt(71.7076287858352 - 4 * 2.03660714 * (-5.865 - X))) / 4.07321428
        return KnockAPIValue

    def SlimeBounceLogarithmicEquation(self, Value):

        X = Value
        BounceHeight = 25 * math.log(0.0252 * X + 1)
        return BounceHeight
    
    def BlockFallTime(self, Value):

        X = Value
        Angle = 3.3
        Time = (X * math.sin(-Angle) + (1.8 * math.log(X + 10) - 5)**2 * math.cos(Angle))**(2 / 3.4)

        if isinstance(Time, complex):
            Time = 0

        return Time

    def BlockFallDamage(self, Value):

        X = Value
        FallDamage = (X - 3) / 2

        if FallDamage < 0:
            FallDamage = 0
            
        return FallDamage

    def Click(self, Key):

        if Key.isdigit() or Key == '.':

            self.Play_Sound("Button")

            if self.Current_Input.get() == "0" and Key != '.':

                self.Current_Input.set(Key)
            else:
                self.Current_Input.set(self.Current_Input.get() + Key)

        elif Key in ['+', '-', '*', '/']:

            self.Play_Sound("Operation")
            self.Operation = Key
            self.First_Number = float(self.Current_Input.get())
            self.Current_Input.set("0")

        elif Key == '=':

            self.Play_Sound("Operation")

            if self.Operation and self.First_Number is not None:

                Second_Number = float(self.Current_Input.get())
                Result = self.Calculate(self.First_Number, Second_Number, self.Operation)
                self.Current_Input.set(str(Result))
                self.Operation = None
                self.First_Number = None

    def Calculate(self, First_Value, Second_Value, OperationType):

        if OperationType == '+':
            return First_Value + Second_Value
        
        elif OperationType == '-':
            return First_Value - Second_Value
        
        elif OperationType == '*':
            return First_Value * Second_Value
        
        elif OperationType == '/':
            return First_Value / Second_Value if Second_Value != 0 else "Error"

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
    App = MinecraftCalculatorGenerator()
    App.mainloop()

if __name__ == "__main__":
    Main()