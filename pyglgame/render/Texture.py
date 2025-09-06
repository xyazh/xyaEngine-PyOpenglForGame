from typing import Optional
from typing import TYPE_CHECKING
from OpenGL.GL import *
from ..RenderGlobal import RenderGlobal
from .TextureBase import TextureBase

if TYPE_CHECKING:
    from .Image import Image

NEAREST = 0
LINEAR = 1


class Texture(TextureBase):
    @staticmethod
    def createDataTexture(image: "Image",
                          width: int, height: int,
                          filter: int = LINEAR, mipmap: bool = False, wrap_mode: int = GL_REPEAT) -> "Texture":
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        x = GL_RGBA32F if image.use_hdr else GL_RGBA
        glTexImage2D(GL_TEXTURE_2D, 0, x,
                     width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE,
                     image.data)
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
        return Texture.createDataTexture(image, width, height, filter, mipmap, wrap_mode)

    def bind(self, unit=GL_TEXTURE0):
        glActiveTexture(unit)
        glBindTexture(GL_TEXTURE_2D, self.id)
        shader = RenderGlobal.instance.using_shader
        if shader is not None:
            shader.uniformTex(unit)

    def bindImage2D(self, uint=0):
        glBindTexture(GL_TEXTURE_2D, self.id)
        glBindImageTexture(uint, self.id, 0,
                           GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)
