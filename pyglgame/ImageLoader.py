from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .Size import Size

class ImageLoader:
    def __init__(self,game_main_loop)->None:
        self.image:Image = None
        self.img_data = None
        self.has_tex_id:bool = False
        self.tex_id:int = None
        self.img_is_loaded:False = False
        self.path:str = None
        self.game_main_loop = game_main_loop
        self.window = game_main_loop.window

    def loadFromPath(self)->None:
        try:
            self.image = Image.open(self.path)
        except BaseException as e:
            raise e
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.img_data = self.image.convert("RGBA").tobytes()
        self.img_is_loaded = True

    def loadfromImg(self,img:Image)->None:
        self.image = img
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.img_data = self.image.convert("RGBA").tobytes()
        self.img_is_loaded = True

    def delImage(self):
        self.image = None
        self.img_data = None
        self.img_is_loaded = False

    def getTextureId(self)->int:
        if self.has_tex_id:
            return self.tex_id
        if not self.img_is_loaded:
            self.loadFromPath()
        try:
            id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image.width, self.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_data)
        except BaseException as e:
            raise e
        self.tex_id = id
        self.has_tex_id = True
        return id

    def delTex(self):
        if self.has_tex_id:
            self.has_tex_id = False
            pass

    def crop(self,x:int,y:int,w:int,h:int):
        r = ImageLoader()
        r.loadfromImg(self.image.crop((x,y,w,h)))
        return r


    def getSize(self):
        if self.img_is_loaded:
            return Size(self.image.width,self.image.height)
        else:
            self.loadFromPath()
            return Size(self.image.width,self.image.height)


    def _drawPlane(self, x: float, y:float,h:float,w:float)->None:
        glBegin(GL_TRIANGLE_STRIP)
        #右上角点
        glTexCoord2f(1.0, 1.0)
        #x,z,y
        glVertex3f(x+w,y,-1.0)
        #左上角点x
        glTexCoord2f(0.0, 1.0)
        #x,z,y
        glVertex3f(x,  y,-1.0,)
        #右下角点
        glTexCoord2f(1.0, 0.0)
        #x,z,y
        glVertex3f(x+w, y-h, -1.0)
        #左下角点
        glTexCoord2f(0.0, 0.0)
        #x,z,y
        glVertex3f(x, y-h, -1.0)
        glEnd()