import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.font as TkFont
from tkextrafont import Font
import subprocess
import os
import pygame
import json

class Block:

    def __init__(self, Type, Text, Color, Code_Template, Is_Object=False, Is_Object_And_Parameter=False, Is_Escape=False, Override_Code_Structure=None, Is_An_Extension = False):

        self.Type = Type
        self.Text = Text
        self.Color = Color
        self.Code_Template = Code_Template
        self.Is_Object = Is_Object
        self.Is_Object_And_Parameter = Is_Object_And_Parameter
        self.Is_Escape = Is_Escape
        self.Override_Code_Structure = Override_Code_Structure
        self.Is_An_Extension = Is_An_Extension

class EnhancedCodeBuilder(tk.Tk):

    def __init__(self):
        super().__init__()

        # Maximizes The Window
        self.state("zoomed") 

        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        # Setting The Current Setting To None
        self.Default_Text_Color_Setting = None
        self.Default_Import_Color_Setting = None
        self.Default_Control_Color_Setting = None
        self.Default_World_Color_Setting = None
        self.Default_Player_Color_Setting = None
        self.Default_Dimension_Color_Setting = None
        self.Default_Entity_Color_Setting = None
        self.Default_Custom_Color_Setting = None

        # Loads The Code Builder Settings
        self.Load_Code_Builder_Menu_Settings()

        # Loading Custom Fonts
        self.Load_Custom_Fonts()

        # Loading Sounds
        self.Load_Sounds()

        # Creating Minecraft UI 
        self.Create_UI()

        # Block Colors
        self.Import_Color = self.Default_Import_Color_Setting
        self.Control_Color = self.Default_Control_Color_Setting
        self.World_Color = self.Default_World_Color_Setting
        self.Player_Color = self.Default_Player_Color_Setting
        self.Dimension_Color = self.Default_Dimension_Color_Setting
        self.Entity_Color = self.Default_Entity_Color_Setting
        self.Custom_Color = self.Default_Custom_Color_Setting

        # All Block Code Structures
        self.Blocks = [
            Block("Import", "Minecraft/Server <>", self.Import_Color, "import {} from '@minecraft/server'", False, False, False, 1, False),
            Block("Import", "Minecraft/Server-UI <>", self.Import_Color, "import {} from '@minecraft/server-ui'", False, False, False, 2, False),
            Block("Import", "Minecraft/GameTest", self.Import_Color, "import {} from '@minecraft/gametest'", False, False, False, 3, False),
            Block("Control", "True", self.Control_Color, "true", False, False, False, None, False),
            Block("Control", "False", self.Control_Color, "false", False, False, False, None, False),
            Block("Control", "Not", self.Control_Color, "!", False, False, False, None, False),
            Block("Control", "Is", self.Control_Color, "==", False, False, False, None, False),
            Block("Control", "Is Really", self.Control_Color, "===", False, False, False, None, False),
            Block("Control", "Is Not", self.Control_Color, "!=", False, False, False, None, False),
            Block("Control", "Is Really Not", self.Control_Color, "!==", False, False, False, None, False),
            Block("Control", "Less Than", self.Control_Color, "<", False, False, False, None, False),
            Block("Control", "Greater Than", self.Control_Color, ">", False, False, False, None, False),
            Block("Control", "Less Than Or Equal To", self.Control_Color, "<=", False, False, False, None, False),
            Block("Control", "Greater Than Or Equal To", self.Control_Color, ">=", False, False, False, None, False),
            Block("Control", "If <>", self.Control_Color, "if ()\n", True, False, False, None, False),
            Block("Control", "Repeat <>", self.Control_Color, "for (let i = 0; i < {}; i++)\n", True, False, False, None, False),
            Block("Control", "Console Warn <>", self.Control_Color, "console.warn", False, False, False, None, False),
            Block("Control", "System After Event <>", self.Control_Color, "system.afterEvents(()=>", False, True, False, None, False),
            Block("Control", "System Before Event <>", self.Control_Color, "system.beforeEvents(()=>", False, True, False, None, False),
            Block("Control", "System Clear Job <>", self.Control_Color, "system.clearJob", False, False, False, None, False),
            Block("Control", "System Clear Run <>", self.Control_Color, "system.clearRun", False, False, False, None, False),
            Block("Control", "System Current Tick", self.Control_Color, "system.currentTick", False, False, False, None, False),
            Block("Control", "System Run", self.Control_Color, "system.run(()=>", False, True, False, None, False),
            Block("Control", "System Run Interval <>", self.Control_Color, "system.runInterval(()=>", False, True, False, None, False),
            Block("Control", "System Run Job <>", self.Control_Color, "system.runJob", False, False, False, None, False),  
            Block("Control", "System Run Timeout <>", self.Control_Color, "system.runTimeout(()=>", False, True, False, None, False),  
            Block("Control", "system Wait Ticks <>", self.Control_Color, "system.waitTicks", False, False, False, None, False),          
            Block("Control", "End Block", self.Control_Color, "}", False, False, True, None, False),
            Block("World", "After Event", self.World_Color, "world.afterEvents", False, False, False, None, False),
            Block("World", "Before Event", self.World_Color, "world.beforeEvents", False, False, False, None, False),
            Block("World", "Broadcast Client Message", self.World_Color, "world.broadcastClientMessage", False, False, False, None, False),
            Block("World", "Clear Dynamic Properties", self.World_Color, "world.clearDynamicProperties()", False, False, False, None, False),
            Block("World", "Gamerules", self.World_Color, "world.gameRules", False, False, False, None, False),
            Block("World", "Get Absolute Time", self.World_Color, "world.getAbsoluteTime()", False, False, False, None, False),
            Block("World", "Get All Players", self.World_Color, "world.getAllPlayers())\n", False, False, False, None, False),
            Block("World", "Get Day", self.World_Color, "world.getDay()", False, False, False, None, False),
            Block("World", "Get Default Spawn Location", self.World_Color, "world.getDefaultSpawnLocation()", False, False, False, None, False),
            Block("World", "Get Dimension", self.World_Color, "world.getDimension", False, False, False, None, False),
            Block("World", "Get Dynamic Property", self.World_Color, "world.getDynamicProperty", False, False, False, None, False),
            Block("World", "Get Dynamic Property Ids", self.World_Color, "world.getDynamicPropertyIds()", False, False, False, None, False),
            Block("World", "Get Dynamic Property Total Byte Count", self.World_Color, "world.getDynamicPropertyTotalByteCount()", False, False, False, None, False),    
            Block("World", "Get Entity", self.World_Color, "world.getEntity", False, False, False, None, False),     
            Block("World", "Get Moon Phase", self.World_Color, "world.getMoonPhase()", False, False, False, None, False),
            Block("World", "Get Player", self.World_Color, "world.getPlayers", False, False, False, None, False),
            Block("World", "Is Hardcore", self.World_Color, "world.isHardcore", False, False, False, None, False),
            Block("World", "Play Music", self.World_Color, "world.playMusic", False, False, False, None, False), 
            Block("World", "Play Sound", self.World_Color, "world.playSound", False, False, False, None, False), 
            Block("World", "Queue Music", self.World_Color, "world.queueMusic", False, False, False, None, False), 
            Block("World", "Scoreboard", self.World_Color, "world.scoreboard", False, False, False, None, False), 
            Block("World", "Send Message", self.World_Color, "world.sendMessage", False, False, False, None, False), 
            Block("World", "Set Absolute Time", self.World_Color, "world.setAbsoluteTime", False, False, False, None, False), 
            Block("World", "Set Default Spawn Location", self.World_Color, "world.setDefaultSpawnLocation", False, False, False, None, False), 
            Block("World", "Set Dynamic Property", self.World_Color, "world.setDynamicProperty", False, False, False, None, False), 
            Block("World", "Set Time Of Day", self.World_Color, "world.setTimeOfDay", False, False, False, None, False), 
            Block("World", "Stop Music", self.World_Color, "world.stopMusic()", False, False, False, None, False), 
            Block("World", "Structure Manager", self.World_Color, "world.structureManager", False, False, False, None, False),
            Block("Dimension", "Contains Block", self.Dimension_Color, ".containsBlock", False, False, False, None, True), 
            Block("Dimension", "Create Explosion", self.Dimension_Color, ".createExplosion", False, False, False, None, True),           
            Block("Dimension", "Fill Blocks", self.Dimension_Color, ".fillBlocks", False, False, False, None, True),
            Block("Dimension", "Find Closest Biome", self.Dimension_Color, ".findClosestBiome", False, False, False, None, True), 
            Block("Dimension", "Get Block", self.Dimension_Color, ".getBlock", False, False, False, None, True),           
            Block("Dimension", "Get Block Above", self.Dimension_Color, ".getBlockAbove", False, False, False, None, True),
            Block("Dimension", "Get Block Below", self.Dimension_Color, ".getBlockBelow", False, False, False, None, True), 
            Block("Dimension", "Get Block From Ray", self.Dimension_Color, ".getBlockFromRay", False, False, False, None, True),           
            Block("Dimension", "Get Blocks", self.Dimension_Color, ".getBlocks", False, False, False, None, True),
            Block("Dimension", "Get Entities", self.Dimension_Color, ".getEntities", False, False, False, None, True), 
            Block("Dimension", "Get Entities At Block Location", self.Dimension_Color, ".getEntitiesAtBlockLocation", False, False, False, None, True),           
            Block("Dimension", "Get Entities From Ray", self.Dimension_Color, ".getEntitiesFromRay", False, False, False, None, True),
            Block("Dimension", "Get Players", self.Dimension_Color, ".getPlayers", False, False, False, None, True), 
            Block("Dimension", "Get Topmost Block", self.Dimension_Color, ".getTopmostBlock", False, False, False, None, True),           
            Block("Dimension", "Get Weather", self.Dimension_Color, "..getWeather()", False, False, False, None, True),
            Block("Dimension", "Height Range", self.Dimension_Color, ".heightRange", False, False, False, None, True), 
            Block("Dimension", "Id", self.Dimension_Color, ".id", False, False, False, None, True),           
            Block("Dimension", "PlaySound", self.Dimension_Color, ".playSound", False, False, False, None, True),
            Block("Dimension", "Run Command", self.Dimension_Color, ".runCommand", False, False, False, None, True),
            Block("Dimension", "Run Command Async", self.Dimension_Color, ".runCommandAsync", False, False, False, None, True),
            Block("Dimension", "Set Block Permutation", self.Dimension_Color, ".setBlockPermutation", False, False, False, None, True),
            Block("Dimension", "Set Block Type", self.Dimension_Color, ".setBlockType", False, False, False, None, True),
            Block("Dimension", "Set Weather", self.Dimension_Color, ".setWeather", False, False, False, None, True),
            Block("Dimension", "SpawnEntity", self.Dimension_Color, ".spawnEntity", False, False, False, None, True),
            Block("Dimension", "Spawn Item", self.Dimension_Color, ".spawnItem", False, False, False, None, True),
            Block("Dimension", "Spawn Particle", self.Dimension_Color, ".spawnParticle", False, False, False, None, True),
            Block("Player", "Add Affect", self.Player_Color, ".addEffect", False, False, False, None, True),
            Block("Player", "Add Experience", self.Player_Color, ".addExperience", False, False, False, None, True),
            Block("Player", "Add Levels", self.Player_Color, ".addLevels", False, False, False, None, True),
            Block("Player", "Add Tag", self.Player_Color, ".addTag", False, False, False, None, True),
            Block("Player", "Apply Damage", self.Player_Color, ".applyDamage", False, False, False, None, True),
            Block("Player", "Apply Knockback", self.Player_Color, ".applyKnockback", False, False, False, None, True),
            Block("Player", "Camera", self.Player_Color, ".camera", False, False, False, None, True),
            Block("Player", "Clear Dynamic Properties", self.Player_Color, ".clearDynamicProperties()", False, False, False, None, True),
            Block("Player", "Dimension", self.Player_Color, ".dimension", False, False, False, None, True),
            Block("Player", "EatI tem", self.Player_Color, ".eatItem", False, False, False, None, True),
            Block("Player", "Extinguish Fire", self.Player_Color, ".extinguishFire", False, False, False, None, True),
            Block("Player", "Get Block From View Direction", self.Player_Color, ".getBlockFromViewDirection", False, False, False, None, True),
            Block("Player", "Get Component", self.Player_Color, ".getComponent", False, False, False, None, True),
            Block("Player", "Get Components", self.Player_Color, ".getComponents", False, False, False, None, True),
            Block("Player", "Get Dynamic Property", self.Player_Color, ".getDynamicProperty", False, False, False, None, True),
            Block("Player", "Get Dynamic Property Ids", self.Player_Color, ".getDynamicPropertyIds()", False, False, False, None, True),
            Block("Player", "Get Dynamic Property Total Byte Count", self.Player_Color, ".getDynamicPropertyTotalByteCount()", False, False, False, None, True),
            Block("Player", "Get Effect", self.Player_Color, ".getEffect", False, False, False, None, True),
            Block("Player", "Get Effects", self.Player_Color, ".getEffects()", False, False, False, None, True),
            Block("Player", "Get Entities From View Direction", self.Player_Color, ".getEntitiesFromViewDirection", False, False, False, None, True),
            Block("Player", "Get GameMode", self.Player_Color, ".getGameMode()", False, False, False, None, True),
            Block("Player", "Get Head Location", self.Player_Color, ".getHeadLocation()", False, False, False, None, True),
            Block("Player", "Get Item Cooldown", self.Player_Color, ".getItemCooldown", False, False, False, None, True),
            Block("Player", "Get Property", self.Player_Color, ".getProperty", False, False, False, None, True),
            Block("Player", "Get Rotation", self.Player_Color, ".getRotation()", False, False, False, None, True),
            Block("Player", "Get Spawn Point", self.Player_Color, ".getSpawnPoint()", False, False, False, None, True),
            Block("Player", "Get Tags", self.Player_Color, ".getTags()", False, False, False, None, True),
            Block("Player", "Get Total Xp", self.Player_Color, ".getTotalXp()", False, False, False, None, True),
            Block("Player", "Get Velocity", self.Player_Color, ".getVelocity()", False, False, False, None, True),
            Block("Player", "Get View Direction", self.Player_Color, ".getViewDirection()", False, False, False, None, True),
            Block("Player", "Has Component", self.Player_Color, ".hasComponent", False, False, False, None, True),
            Block("Player", "Has Tag", self.Player_Color, ".hasTag", False, False, False, None, True),
            Block("Player", "Id", self.Player_Color, ".id", False, False, False, None, True),
            Block("Player", "Input Permissions", self.Player_Color, ".inputPermissions", False, False, False, None, True),
            Block("Player", "Is Climbing", self.Player_Color, ".isClimbing", False, False, False, None, True),
            Block("Player", "Is Emoting", self.Player_Color, ".isEmoting", False, False, False, None, True),
            Block("Player", "Is Falling", self.Player_Color, ".isFalling", False, False, False, None, True),
            Block("Player", "Is Flying", self.Player_Color, ".isFlying", False, False, False, None, True),
            Block("Player", "Is Gliding", self.Player_Color, ".isGliding", False, False, False, None, True),
            Block("Player", "Is In Water", self.Player_Color, ".isInWater", False, False, False, None, True),
            Block("Player", "Is Jumping", self.Player_Color, ".isJumping", False, False, False, None, True),
            Block("Player", "Is On Ground", self.Player_Color, ".isOnGround", False, False, False, None, True),
            Block("Player", "Is Operator", self.Player_Color, ".isOp", False, False, False, None, True),
            Block("Player", "Is Sleeping", self.Player_Color, ".isSleeping", False, False, False, None, True),
            Block("Player", "Is Sneaking", self.Player_Color, ".isSneaking", False, False, False, None, True),
            Block("Player", "Is Sprinting", self.Player_Color, ".isSprinting", False, False, False, None, True),
            Block("Player", "Is Swimming", self.Player_Color, ".isSwimming", False, False, False, None, True),
            Block("Player", "Is Valid", self.Player_Color, ".isValid()", False, False, False, None, True),
            Block("Player", "Kill", self.Player_Color, ".kill()", False, False, False, None, True),
            Block("Player", "Level", self.Player_Color, ".level", False, False, False, None, True),
            Block("Player", "Location", self.Player_Color, ".location", False, False, False, None, True),
            Block("Player", "Matches", self.Player_Color, ".matches", False, False, False, None, True),
            Block("Player", "Name", self.Player_Color, ".name", False, False, False, None, True),
            Block("Player", "Name Tag", self.Player_Color, ".nameTag", False, False, False, None, True),
            Block("Player", "On Screen Display", self.Player_Color, ".onScreenDisplay", False, False, False, None, True),
            Block("Player", "Play Animation", self.Player_Color, ".playAnimation", False, False, False, None, True),
            Block("Player", "Play Music", self.Player_Color, ".playMusic", False, False, False, None, True),
            Block("Player", "Play Sound", self.Player_Color, ".playSound", False, False, False, None, True),
            Block("Player", "Post Client Message", self.Player_Color, ".postClientMessage", False, False, False, None, True),
            Block("Player", "Queue Music", self.Player_Color, ".queueMusic", False, False, False, None, True),
            Block("Player", "Remove Effect", self.Player_Color, ".removeEffect", False, False, False, None, True),
            Block("Player", "Remove Tag", self.Player_Color, ".removeTag", False, False, False, None, True),
            Block("Player", "Reset Level", self.Player_Color, ".resetLevel()", False, False, False, None, True),
            Block("Player", "Reset Property", self.Player_Color, ".resetProperty", False, False, False, None, True),
            Block("Player", "Run Command", self.Player_Color, ".runCommand", False, False, False, None, True),
            Block("Player", "Run Command Async", self.Player_Color, "runCommandAsync", False, False, False, None, True),
            Block("Player", "Scoreboard Identity", self.Player_Color, ".scoreboardIdentity", False, False, False, None, True),
            Block("Player", "Selected Slot Index", self.Player_Color, ".selectedSlotIndex", False, False, False, None, True),
            Block("Player", "Send Message", self.Player_Color, ".sendMessage", False, False, False, None, True),
            Block("Player", "Set Dynamic Property", self.Player_Color, ".setDynamicProperty", False, False, False, None, True),
            Block("Player", "Set GameMode", self.Player_Color, ".setGameMode", False, False, False, None, True),
            Block("Player", "Set On Fire", self.Player_Color, ".setOnFire", False, False, False, None, True),
            Block("Player", "Set Operator", self.Player_Color, ".setOp", False, False, False, None, True),
            Block("Player", "Set Property", self.Player_Color, ".setProperty", False, False, False, None, True),
            Block("Player", "Set Rotation", self.Player_Color, ".setRotation", False, False, False, None, True),
            Block("Player", "Set Spawn Point", self.Player_Color, ".setSpawnPoint", False, False, False, None, True),
            Block("Player", "Spawn Particle", self.Player_Color, ".spawnParticle", False, False, False, None, True),
            Block("Player", "Start Item Cooldown", self.Player_Color, ".startItemCooldown", False, False, False, None, True),
            Block("Player", "Stop Music", self.Player_Color, ".stopMusic()", False, False, False, None, True),
            Block("Player", "Target", self.Player_Color, ".target", False, False, False, None, True),
            Block("Player", "Teleport", self.Player_Color, ".teleport", False, False, False, None, True),
            Block("Player", "Total Xp Needed For Next Level", self.Player_Color, ".totalXpNeededForNextLevel", False, False, False, None, True),
            Block("Player", "Trigger Event", self.Player_Color, ".triggerEvent", False, False, False, None, True),
            Block("Player", "Try Teleport", self.Player_Color, ".tryTeleport", False, False, False, None, True),
            Block("Player", "Type Id", self.Player_Color, ".typeId", False, False, False, None, True),
            Block("Player", "Xp Earned At Current Level", self.Player_Color, ".xpEarnedAtCurrentLevel", False, False, False, None, True),
            Block("Entity", "Entity", self.Entity_Color, "entity({});"),
            Block("Custom", "Camera", self.Custom_Color, "camera({});"),
        ]

        # Setups The Block Categories
        self.Categories = list(set(Block.Type for Block in self.Blocks))
        self.Current_Category = self.Categories[0]
        self.Create_Category_Buttons()

        # Generates Blocks Onto Canvas
        self.Create_Block_Buttons()
        self.Canvas_Blocks = []

        # Variables For Draging And Snapping
        self.Drag_Data = {"X": 0, "Y": 0, "Item": None}
        self.Snapping_Distance = 20  # Define the snapping distance

    def Load_Code_Builder_Menu_Settings(self):

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
        
        def Read_Code_Builder_Menu_Settings():

            Code_Builder_Settings = self.Current_Settings.get("Code Builder Menu", {})

            Default_Text_Color = Code_Builder_Settings["Default Text Color"]
            Default_Import_Color = Code_Builder_Settings["Default Import Color"]
            Default_Control_Color = Code_Builder_Settings["Default Control Color"]
            Default_World_Color = Code_Builder_Settings["Default World Color"]
            Default_Player_Color = Code_Builder_Settings["Default Player Color"]
            Default_Dimension_Color = Code_Builder_Settings["Default Dimension Color"]
            Default_Entity_Color = Code_Builder_Settings["Default Entity Color"]
            Default_Custom_Color = Code_Builder_Settings["Default Custom Color"]

            return Default_Text_Color, Default_Import_Color, Default_Control_Color, Default_World_Color, Default_Player_Color, Default_Dimension_Color, Default_Entity_Color, Default_Custom_Color

        self.Default_Text_Color_Setting, self.Default_Import_Color_Setting, self.Default_Control_Color_Setting, self.Default_World_Color_Setting, self.Default_Player_Color_Setting, self.Default_Dimension_Color_Setting, self.Default_Entity_Color_Setting, self.Default_Custom_Color_Setting = Read_Code_Builder_Menu_Settings()

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

        # List Of Custom Sounds
        Sound_Files = [
            (os.path.join(Sound_Directory, "UI_Button_Press_2.ogg"), "Setting"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Update Preview"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Download"),
            (os.path.join(Sound_Directory, "UI_Button_Press.ogg"), "Convert Font"),
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
        self.title("MasterCraft - Code Builder")

        # Set The Main Window Color
        self.configure(bg="#3C3F41")

        # Set The Icon Of The Window
        Icon_Image_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")
        self.iconbitmap(Icon_Image_Path)
       
        self.Create_Header_Frame()

        # Creates The Main Frame
        Main_Frame = tk.Frame(self, bg="#3C3F41")
        Main_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Creates The Left Panel For Inputs
        self.Left_Panel = tk.Frame(Main_Frame, bg="#2B2B2B", width=300)
        self.Left_Panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))

        # Creates The Category Panel
        self.Category_Frame = tk.Frame(self.Left_Panel, bg="#2B2B2B")
        self.Category_Frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Creates The Block Display Panel
        self.Block_Frame = tk.Frame(self.Left_Panel, bg="#2B2B2B")
        self.Block_Frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Creates Right Panel For Output Code And Canvas Area
        Right_Panel = tk.Frame(Main_Frame, bg="#2B2B2B")
        Right_Panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.Canvas = tk.Canvas(Right_Panel, bg="#1E1E1E", bd=0, highlightthickness=0)
        self.Canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.Code_Preview = tk.Text(Right_Panel, bg="#1E1E1E", fg=self.Default_Text_Color_Setting, font=self.Custom_Fonts["Minecraft Seven v2"], wrap=tk.NONE)
        self.Code_Preview.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bind Mouse Events For Drag, Motion, And Drop
        self.Canvas.tag_bind("Block", "<ButtonPress-1>", self.On_Drag_Start)
        self.Canvas.tag_bind("Block", "<B1-Motion>", self.On_Drag_Motion)
        self.Canvas.tag_bind("Block", "<ButtonRelease-1>", self.On_Drag_Stop)

    def Create_Header_Frame(self):

        Header_Frame = tk.Frame(self, bg='#4C4C4C')
        Header_Frame.pack(fill=tk.X)

        Font_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Code_Builder.png")
        Font_Icon = ImageTk.PhotoImage(Image.open(Font_Icon_Path).resize((32, 32)))

        Icon_Label = tk.Label(Header_Frame, image=Font_Icon, bg='#4C4C4C')
        Icon_Label.image = Font_Icon
        Icon_Label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        Title_Label = tk.Label(Header_Frame, text="Code Builder", font=self.Custom_Fonts["Minecraft Ten v2"], bg='#4C4C4C', fg='white')
        Title_Label.pack(side=tk.LEFT, pady=5)

        # Add Settings Button To The Title Frame On The Right
        Settings_Icon_Path = os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Textures", "Settings_Darken.png")
        Settings_Icon = ImageTk.PhotoImage(Image.open(Settings_Icon_Path).resize((24, 24)))

        Settings_Button = tk.Button(Header_Frame, image=Settings_Icon, bg='#4C4C4C', bd=0, highlightthickness=0, command=self.Setting, activebackground="#4C4C4C")
        Settings_Button.image = Settings_Icon
        Settings_Button.pack(side=tk.RIGHT, padx=(0, 10))

    def Create_Block_Buttons(self):

        for Block in self.Blocks:

            Block_Button = tk.Button(self.Left_Panel, text=Block.Text, bg=Block.Color, fg="black", font=self.Custom_Fonts["Minecraft Seven v2"], command=lambda Event=Block: self.Add_Block_To_Canvas(Event))
            Block_Button.pack(fill=tk.X, pady=1, padx=10)

    def Add_Block_To_Canvas(self, Block):
        
        X, Y = 50, len(self.Canvas_Blocks) * 30 + 30
        Block_Id = self.Canvas.create_rectangle(X, Y, X + 200, Y + 25, fill=Block.Color, outline="black", tags="Block")
        Text_Id = self.Canvas.create_text(X + 5, Y + 12, text=Block.Text, anchor=tk.W, font=self.Custom_Fonts["Minecraft Seven v2"], tags="Block")
        self.Canvas_Blocks.append((Block_Id, Text_Id, Block))
        self.Update_Code_Preview()

    def Create_Category_Buttons(self):

        for Category in self.Categories:

            Category_Button = tk.Button(self.Category_Frame, text=Category, bg="#4C4C4C", fg="white", font=self.Custom_Fonts["Minecraft Seven v2"], command=lambda Event=Category: self.Switch_Category(Event))
            Category_Button.pack(side=tk.LEFT, padx=(0, 5))

    def Switch_Category(self, Category):

        self.Current_Category = Category
        self.Update_Block_Buttons()

    def Create_Block_Buttons(self):

        self.Block_Buttons = []

        for Block in self.Blocks:

            Block_Button = tk.Button(self.Block_Frame, text=Block.Text, bg=Block.Color, fg="black", font=self.Custom_Fonts["Minecraft Seven v2"], command=lambda Event=Block: self.Add_Block_To_Canvas(Event))
            self.Block_Buttons.append((Block_Button, Block))

        self.Update_Block_Buttons()

    def Update_Block_Buttons(self):

        for Block_Button, Block in self.Block_Buttons:
            Block_Button.pack_forget()

        for Block_Button, Block in self.Block_Buttons:

            if Block.Type == self.Current_Category:
                Block_Button.pack(fill=tk.X, pady=1)

    def Update_Code_Preview(self):

        self.Code_Preview.delete("1.0", tk.END)
        Sorted_Blocks = sorted(self.Canvas_Blocks, key=lambda X: self.Canvas.coords(X[0])[1])
        
        # Separate Override Blocks And Regular Blocks
        Override_Blocks = [Structure for Structure in Sorted_Blocks if Structure[2].Override_Code_Structure is not None]
        Regular_Blocks = [Structure for Structure in Sorted_Blocks if Structure[2].Override_Code_Structure is None]
        
        # Sort Override Blocks Based On Their Override_Code_Structure Value
        Override_Blocks.sort(key=lambda X: X[2].Override_Code_Structure)
        
        # Generate Code For Override Blocks
        Override_Code = self.Generate_Nested_Code(Override_Blocks)
        
        # Generate Code For Regular Blocks
        Regular_Code = self.Generate_Nested_Code(Regular_Blocks)
        
        # Combine Override And Regular Code
        Full_Code = Override_Code + Regular_Code
        
        self.Code_Preview.insert(tk.END, "\n".join(Full_Code))
        self.Code_Preview.see(tk.END)

    def Generate_Nested_Code(self, Blocks, Indent=0):

        Code_Lines = []
        I = 0
        Current_Line = ""

        while I < len(Blocks):

            Block_Id, Text_Id, Block = Blocks[I]

            if Block.Is_Escape:

                # Decrease Indent, But Not Below 0
                Indent = max(0, Indent - 1)
                I += 1
                continue

            if Block.Is_Object:

                Object_Lines, Blocks_Consumed = self.Process_Object_Block(Blocks[I:], Indent)
                Code_Lines.extend(Object_Lines)
                I += Blocks_Consumed
                Current_Line = ""

            elif Block.Is_Object_And_Parameter:

                Object_Lines, Blocks_Consumed = self.Process_Object_And_Parameter_Block(Blocks[I:], Indent)
                Code_Lines.extend(Object_Lines)
                I += Blocks_Consumed
                Current_Line = ""

            else:

                if Block.Is_An_Extension:
                    Current_Line += Block.Code_Template.strip()

                else:

                    if Current_Line:
                        Code_Lines.append("    " * Indent + Current_Line)

                    Current_Line = Block.Code_Template.strip()
                I += 1

        if Current_Line:
            Code_Lines.append("    " * Indent + Current_Line)

        return Code_Lines

    def Process_Object_Block(self, Blocks, Indent):

        Block_Id, Text_Id, Block = Blocks[0]
        Code_Lines = ["    " * Indent + Block.Code_Template.strip() + " {"]
        I = 1
        Current_Line = ""

        while I < len(Blocks):

            Next_Block_Id, Next_Text_Id, Next_Block = Blocks[I]

            if Next_Block.Is_Escape:
                break

            if Next_Block.Is_Object:

                if Current_Line:

                    Code_Lines.append("    " * (Indent + 1) + Current_Line)
                    Current_Line = ""

                Nested_Lines, Nested_I = self.Process_Object_Block(Blocks[I:], Indent + 1)
                Code_Lines.extend(Nested_Lines)
                I += Nested_I

            elif Next_Block.Is_Object_And_Parameter:
                
                if Current_Line:

                    Code_Lines.append("    " * (Indent + 1) + Current_Line)
                    Current_Line = ""
            
                Nested_Lines, Nested_I = self.Process_Object_And_Parameter_Block(Blocks[I:], Indent + 1)
                Code_Lines.extend(Nested_Lines)
                I += Nested_I

            else:

                if Next_Block.Is_An_Extension:
                    Current_Line += Next_Block.Code_Template.strip()

                else:

                    if Current_Line:
                        Code_Lines.append("    " * (Indent + 1) + Current_Line)

                    Current_Line = Next_Block.Code_Template.strip()
                I += 1

        if Current_Line:
            Code_Lines.append("    " * (Indent + 1) + Current_Line)
        
        Code_Lines.append("    " * Indent + "}")
        return Code_Lines, I + 1 

    def Process_Object_And_Parameter_Block(self, Blocks, Indent):

        Block_Id, Text_Id, Block = Blocks[0]
        Code_Lines = ["    " * Indent + Block.Code_Template.strip() + " {"]
        I = 1
        Current_Line = ""

        while I < len(Blocks):

            Next_Block_Id, Next_Text_Id, Next_Block = Blocks[I]

            if Next_Block.Is_Escape:
                break

            if Next_Block.Is_Object:

                if Current_Line:

                    Code_Lines.append("    " * (Indent + 1) + Current_Line)
                    Current_Line = ""

                Nested_Lines, Nested_I = self.Process_Object_Block(Blocks[I:], Indent + 1)
                Code_Lines.extend(Nested_Lines)
                I += Nested_I

            elif Next_Block.Is_Object_And_Parameter:

                if Current_Line:

                    Code_Lines.append("    " * (Indent + 1) + Current_Line)
                    Current_Line = ""

                Nested_Lines, Nested_I = self.Process_Object_And_Parameter_Block(Blocks[I:], Indent + 1)
                Code_Lines.extend(Nested_Lines)
                I += Nested_I

            else:

                if Next_Block.Is_An_Extension:

                    Current_Line += Next_Block.Code_Template.strip()

                else:

                    if Current_Line:
                        Code_Lines.append("    " * (Indent + 1) + Current_Line)
                        
                    Current_Line = Next_Block.Code_Template.strip()
                I += 1

        if Current_Line:
            Code_Lines.append("    " * (Indent + 1) + Current_Line)

        Code_Lines.append("    " * Indent + "})")
        return Code_Lines, I + 1

    def Is_Nested(self, Parent_Id, Child_Id):

        Parent_Coordinate = self.Canvas.coords(Parent_Id)
        Child_Coordinate = self.Canvas.coords(Child_Id)
        
        # Check If The Child Block Is Horizontally Aligned With The Parent
        Horizontally_Aligned = abs(Parent_Coordinate[0] - Child_Coordinate[0]) < self.Snapping_Distance
        
        # Check If The Child Block Is Below The Parent
        Vertically_Below = Child_Coordinate[1] > Parent_Coordinate[1]
        
        # Check If The Child Block Is Within The Horizontal Span Of The Parent
        Within_Horizontal_Span = Parent_Coordinate[0] <= Child_Coordinate[0] <= Parent_Coordinate[2]
        
        return Horizontally_Aligned and Vertically_Below and Within_Horizontal_Span
    
    def On_Drag_Start(self, Event):

        # Find The Closest Item
        Item = self.Canvas.find_closest(Event.x, Event.y)[0]

        # Check If The Item Is Part Of A Block (Either The Colored Rectangle Or Block Text)
        for Block_Id, Text_Id, _ in self.Canvas_Blocks:

            if Item in (Block_Id, Text_Id):

                self.Drag_Data["Item"] = (Block_Id, Text_Id)
                break
        else:
            return

        self.Drag_Data["X"] = Event.x
        self.Drag_Data["Y"] = Event.y

    def On_Drag_Motion(self, Event):

        if not self.Drag_Data["Item"]:
            return
        
        # Compute How Much The Mouse Has Moved
        Delta_X = Event.x - self.Drag_Data["X"]
        Delta_Y = Event.y - self.Drag_Data["Y"]

        # Move Both The Rectangle And Text
        for Item in self.Drag_Data["Item"]:
            self.Canvas.move(Item, Delta_X, Delta_Y)

        # Record The New Position
        self.Drag_Data["X"] = Event.x
        self.Drag_Data["Y"] = Event.y

    def On_Drag_Stop(self, Event):
        
        if not self.Drag_Data["Item"]:
            return

        Dragged_Block_Id, Dragged_Text_Id = self.Drag_Data["Item"]
        Dragged_Coordinates = self.Canvas.coords(Dragged_Block_Id)

        # Maximum Allowed Horizontal Distance For Snapping
        Closest_Block_Id = None
        Minimum_Distance = float('inf')
        Horizontal_Threshold = 10

        for Block_Id, Text_Id, Block in self.Canvas_Blocks:

            if Block_Id == Dragged_Block_Id:
                continue

            Coordinates = self.Canvas.coords(Block_Id)
            
            # Check If Blocks Are Horizontally Aligned Within The Threshold
            Horizontal_Distance = abs(Dragged_Coordinates[0] - Coordinates[0])

            if Horizontal_Distance > Horizontal_Threshold:
                continue

            Distance_Above = abs(Dragged_Coordinates[1] - Coordinates[3])
            Distance_Below = abs(Dragged_Coordinates[3] - Coordinates[1])

            if Distance_Below < Minimum_Distance and Distance_Below <= self.Snapping_Distance:

                Minimum_Distance = Distance_Below
                Closest_Block_Id = Block_Id
                Position = 'Above'

            if Distance_Above < Minimum_Distance and Distance_Above <= self.Snapping_Distance:

                Minimum_Distance = Distance_Above
                Closest_Block_Id = Block_Id
                Position = 'Below'

        if Closest_Block_Id is not None:

            Closest_Coordinates = self.Canvas.coords(Closest_Block_Id)

            if Position == 'Above':
                New_Y = Closest_Coordinates[1] - (Dragged_Coordinates[3] - Dragged_Coordinates[1])

            else:
                New_Y = Closest_Coordinates[3]

            # Align To The Left Side Of The Closest Block
            New_X = Closest_Coordinates[0]

            Delta_Y = New_Y - Dragged_Coordinates[1]
            Delta_X = New_X - Dragged_Coordinates[0]
            
            self.Canvas.move(Dragged_Block_Id, Delta_X, Delta_Y)
            self.Canvas.move(Dragged_Text_Id, Delta_X, Delta_Y)
            
        else:
            # If Not Snapping To Any Block, Keep The Block At Its Current Position
            pass

        # Reset The Drag Information
        self.Drag_Data["Item"] = None
        self.Drag_Data["X"] = 0
        self.Drag_Data["Y"] = 0
        self.Update_Code_Preview()

    # A Function That Interacts With The Program Settings
    def Setting(self):

        self.Play_Sound("Setting")

        Script_Path = os.path.join(self.MasterCraftCurrentDirectory, "Settings", "Setting.py")
        subprocess.Popen(["python", Script_Path])

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

if __name__ == "__main__":
    app = EnhancedCodeBuilder()
    app.mainloop()