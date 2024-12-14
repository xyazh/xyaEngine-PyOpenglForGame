from typing import Optional
from typing import TYPE_CHECKING
from OpenGL.GL import *

if TYPE_CHECKING:
    from .Image import Image

NEAREST = 0
LINEAR = 1



class Texture:
    @staticmethod
    def _createDataTexture(data, 
                           width: int, height: int, 
                           filter: int = LINEAR, mipmap: bool = False, wrap_mode: int = GL_REPEAT) -> "Texture":
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        if mipmap:
            glGenerateMipmap(GL_TEXTURE_2D)
            if filter == NEAREST:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            elif filter == LINEAR:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        else:
            if filter == NEAREST:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            elif filter == LINEAR:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_mode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_mode)
        return Texture(texture_id)

    @staticmethod
    def createFromImage(image: "Image", 
                        width: int = -1, height: int = -1, 
                        filter: int = LINEAR, mipmap: bool = False, wrap_mode: int = GL_REPEAT) -> "Texture":
        if width == -1:
            width = image.width
        if height == -1:
            height = image.height
        return Texture._createDataTexture(image.data, width, height, filter, mipmap, wrap_mode)

    def __init__(self, id: int):
        self.id = id

    def __del__(self):
        glDeleteTextures(self.id)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)
