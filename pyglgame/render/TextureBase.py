from OpenGL.GL import *

class TextureBase:
    def __init__(self, id: int):
        self.id = int(id)

    def __del__(self):
        glDeleteTextures(self.id)

    def bind(self, unit):
        raise NotImplementedError("Method bind not implemented")