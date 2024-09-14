import pygame
from pygame.locals import DOUBLEBUF, OPENGL, FULLSCREEN
from OpenGL.GL import glTranslatef, glRotatef, glClear, glBindTexture, glTexParameteri, glEnable, glBegin, glEnd, glDisable, glTexImage2D, glGenTextures, glTexCoord2fv, glVertex3fv, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_RGB, GL_UNSIGNED_BYTE, GL_QUADS
from OpenGL.GLU import gluPerspective 
import os

class Cubemap:

    def __init__(self, Image_Files):

        # Launch Pygame
        pygame.init()

        # Get The User's Screen Resolution
        DisplayInfo = pygame.display.Info()
        Display = (DisplayInfo.current_w, DisplayInfo.current_h)

        self.InitialDirectory = '/'
        self.DirectoryName = 'MasterCraft'
        self.MasterCraftCurrentDirectory = self.SearchDirectory()

        if self.MasterCraftCurrentDirectory:
            self.Images = [pygame.image.load(os.path.join(self.MasterCraftCurrentDirectory, "s", File)) for File in Image_Files]
        else:
            self.Images = [pygame.image.load(File) for File in Image_Files]

        # Set Up Display And Icon
        pygame.display.set_mode(Display, DOUBLEBUF | OPENGL | FULLSCREEN)
        pygame.display.set_icon(pygame.image.load(os.path.join(self.MasterCraftCurrentDirectory, "App_UI_Elements", "Icons", "Icon_Image.ico")))

        # Set Up The Perspective With A Wider Field Of View For Panorama Effect
        gluPerspective(90, (Display[0] / Display[1]), 0.1, 100.0)

        # Place The Camera At The Center Of The Cube
        glTranslatef(0.0, 0.0, 0.0)

        # Rotate The Camera By 90 Degrees To Adjust The View
        glRotatef(90, 0, 1, 0)

        self.Textures = self.Load_Textures()

        # Define The Rotation Speed
        Rotation_Speed = 0.05

        Clock = pygame.time.Clock()

        while True:

            for Event in pygame.event.get():

                if Event.type == pygame.QUIT or (Event.type == pygame.KEYDOWN and Event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return

            # Rotates The Cube And
            glRotatef(Rotation_Speed, 0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            Draw_Cube(self.Textures)

            pygame.display.flip()
            Clock.tick(60)

    def Load_Textures(self):

        Textures = []

        for Image in self.Images:

            Texture_Surface = pygame.image.tostring(Image, 'RGB', 1)
            Width, Height = Image.get_size()
            Texture = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, Texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Width, Height, 0, GL_RGB, GL_UNSIGNED_BYTE, Texture_Surface)
            Textures.append(Texture)

        return Textures

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

def Draw_Cube(Textures):

    glEnable(GL_TEXTURE_2D)

    # Define Vertices For A Cube With Reversed Order For Inward Normals
    Vertices = [
        [ 1,  1, -1], [ 1, -1, -1], [ 1, -1,  1], [ 1,  1,  1],
        [-1,  1, -1], [-1, -1, -1], [-1, -1,  1], [-1,  1,  1]
    ]

    # Define Faces Using Vertices
    Faces = [
        (0, 1, 2, 3),  # Right
        (3, 2, 6, 7),  # Back
        (7, 6, 5, 4),  # Left
        (4, 5, 1, 0),  # Front
        (4, 0, 3, 7),  # Top
        (1, 5, 6, 2)   # Bottom
    ]

    # Define Texture Coordinates
    Texture_Coordinates = [
        (0, 1), (0, 0), (1, 0), (1, 1)
    ]

    for I, Face in enumerate(Faces):
        glBindTexture(GL_TEXTURE_2D, Textures[I])
        glBegin(GL_QUADS)

        for Coordinate, Vertex in enumerate(Face):
            glTexCoord2fv(Texture_Coordinates[Coordinate])
            glVertex3fv(Vertices[Vertex])

        glEnd()
    
    glDisable(GL_TEXTURE_2D)

def Main():
    Cubemap(['panorama_0.png', 'panorama_1.png', 'panorama_2.png', 'panorama_3.png', 'panorama_4.png', 'panorama_5.png'])

if __name__ == "__main__":
    Main()
