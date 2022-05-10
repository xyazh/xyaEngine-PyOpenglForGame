from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class ImageLoader:
    def __init__(self)->None:
        self.image = None
        self.img_data = None

    def loadfromPath(self,path:str)->None:
        self.image = Image.open(path)
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.img_data = self.image.convert("RGBA").tobytes()

    def loadfromImg(self,img)->None:
        self.image = img
        self.img_data = self.image.convert("RGBA").tobytes()

    def toTex(self)->int:
        id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image.width, self.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_data)
        return id

    def crop(self,x:int,y:int,w:int,h:int):
        r = ImageLoader()
        r.loadfromImg(self.image.crop((x,y,w,h)))
        return r


    def getSize(self):
        return self.Size(self.image.width,self.image.height)

    class Size:
        def __init__(self,w,h)->None:
            self.w = w
            self.h = h