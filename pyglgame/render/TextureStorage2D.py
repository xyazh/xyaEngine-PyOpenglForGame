from OpenGL.GL import *
from .TextureBase import TextureBase


class TextureStorage2D(TextureBase):
    def __init__(self,w:int,h:int,unit:int=0,internal_format:int=GL_RGBA32F,access:int=GL_READ_WRITE):
        super().__init__(glGenTextures(1))
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexStorage2D(GL_TEXTURE_2D, 1, internal_format, w, h)
        glBindImageTexture(unit, self.id, 0, GL_FALSE,
                           0, access, internal_format)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.w = w
        self.h = h
        self.group_x = int((w + 15) // 16)
        self.group_y = int((h + 15) // 16)


    def bind(self, unit=GL_TEXTURE0):
        glActiveTexture(unit)
        glBindTexture(GL_TEXTURE_2D, self.id)
    