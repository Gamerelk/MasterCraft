import os
import tkinter as tk
import tkinter.font as TkFont
from tkextrafont import Font
from PIL import ImageTk, Image
import subprocess
import time
import pygame
import threading
import re

class HostServerApp(tk.Tk):
        
    def __init__(self):
        super().__init__()

        # Maximizes The Window
        self.state("zoomed")
        
        # Getting User Pathway
        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Creating Minecraft UI  
        self.Create_UI()

        # Add Text Widget for Port Display
        self.Create_Port_Display()

        # Initialize Server Process To None
        self.Server_Process = None

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
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Run Server"),
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Stop Server"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Back")
        ]
        
        for Sound_File, Button_Name in Sound_Files:
            self.Sounds[Button_Name] = pygame.mixer.Sound(Sound_File)

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

        # Creates The Main Frame
        self.Main_Frame = tk.Frame(self, bg="#3C3F41")
        self.Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Buttons
        self.Create_Buttons()

    def Create_Header_Frame(self):

        Server_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Host_Server.png")
        Server_Icon = ImageTk.PhotoImage(Image.open(Server_Icon_Path).resize((32, 32)))

        Header_Frame = tk.Frame(self, bg='#4C4C4C') 
        Header_Frame.pack(fill=tk.X)

        Icon_Label = tk.Label(Header_Frame, image=Server_Icon, bg='#4C4C4C')
        Icon_Label.image = Server_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="Minecraft Host Server", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Buttons(self):

        self.Button_Frame = tk.Frame(self.Main_Frame, bg="#1E1E1E", bd=2, relief=tk.GROOVE)
        self.Button_Frame.pack(fill="x", padx=10, pady=10)

        Buttons = [
            ("Run Server", self.Run_Server, "#007ACC", "#0095fa", "#FFFFFF"),
            ("Run Server", self.Stop_Server, "#CC0000", "#fa0000", "#FFFFFF"),
            ("Back", self.Show_MasterCraftMainScreen, "#4C4C4C", "#2B2B2B", "#6C6C6C")
        ]

        for Text, Function, Color, Highlight_Color, Pressed_Color in Buttons:
            self.Add_Button(self.Button_Frame, Text, Function, Color, Highlight_Color, Pressed_Color)

    def Create_Port_Display(self):

        self.Port_Display = tk.Text(self.Main_Frame, height=3, width=50, font=self.Custom_Fonts["Minecraft Seven v2"], bg="#1E1E1E", fg="white")
        self.Port_Display.pack(pady=10)
        self.Port_Display.insert(tk.END, "Server Ports Will Be Displayed Here When The Server Starts.")
        self.Port_Display.config(state=tk.DISABLED)

    def Add_Button(self, Parent, Text, Function, Color, Highlight_Color, Pressed_Color):

        Button = tk.Button(Parent, text=Text, command=Function, bg=Color, fg='white', activebackground=Pressed_Color, font=self.Custom_Fonts["Minecraft Seven v2"])

        if Text == "Run Server":
            Button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        if Text == "Stop Server":
            Button.pack(side=tk.LEFT, padx=5, pady=10)

        if Text == "Back":
            Button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        Button.bind("<Enter>", lambda e: Button.config(bg=Highlight_Color))
        Button.bind("<Leave>", lambda e: Button.config(bg=Color))
        Button.bind("<Button-1>", lambda e, Button_Text=Text: self.On_Button_Click(Button_Text))

    def On_Button_Click(self, Button_Text):

        self.Play_Sound(Button_Text)

    def Run_Server(self):

        self.Play_Sound("Run")

        def Run_Exe():

            MinecraftLocalServerExecutableDirectory = os.path.join(self.MasterCraftCurrentDirectory, "App_Local_Server", "bedrock_server.exe")

            self.Server_Process = subprocess.Popen(
                MinecraftLocalServerExecutableDirectory,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            threading.Thread(target=self.Read_Server_Output, daemon=True).start()

        thread = threading.Thread(target=Run_Exe)
        thread.start()

    def Stop_Server(self):

        self.Play_Sound("Stop")

        if self.Server_Process:
            
            self.Server_Process.stdin.write("stop\n")
            self.Server_Process.stdin.flush()
            self.Server_Process.wait()
            self.Port_Display.config(state=tk.NORMAL)
            self.Port_Display.delete(1.0, tk.END)
            self.Port_Display.insert(tk.END, "Server Ports Will Be Displayed Here When The Server Starts.")
            self.Port_Display.config(state=tk.DISABLED)

    def Read_Server_Output(self):

        IPV4_Port = None
        IPV6_Port = None

        for Line in self.Server_Process.stdout:
            if "IPv4 supported, port:" in Line:
                IPV4_Port = re.search(r"port: (\d+)", Line).group(1)
            elif "IPv6 supported, port:" in Line:
                IPV6_Port = re.search(r"port: (\d+)", Line).group(1)

            if IPV4_Port and IPV6_Port:
                self.Display_Ports(IPV4_Port, IPV6_Port)
                break

    def Display_Ports(self, IPV4_port, IPV6_port):

        Port_Info = f"IPV4 Port: {IPV4_port}\nIPV6 Port: {IPV6_port}"
        self.Port_Display.config(state=tk.NORMAL)
        self.Port_Display.delete(1.0, tk.END)
        self.Port_Display.insert(tk.END, Port_Info)
        self.Port_Display.config(state=tk.DISABLED)

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
    App = HostServerApp()
    App.mainloop()

if __name__ == "__main__":
    Main()