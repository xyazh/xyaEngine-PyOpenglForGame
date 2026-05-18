import ctypes
from OpenGL.GL import *

class TextureBase:
    def __init__(self, id: int):
        self.id = int(id)

    def __del__(self):
        glDeleteTextures(self.id)

    def bind(self, unit):
        raise NotImplementedError("Method bind not implemented")
    
    def getData(self, level=0, fmt=GL_RGBA, dtype=GL_UNSIGNED_BYTE, ref_data=None):
        if dtype == GL_UNSIGNED_BYTE:
            c_type = ctypes.c_ubyte
        elif dtype == GL_FLOAT:
            c_type = ctypes.c_float
        else:
            raise ValueError(f"Unsupported dtype {dtype}")
        if fmt in (GL_RGBA, GL_RGBA8, GL_RGBA32F):
            channels = 4
        elif fmt in (GL_RGB, GL_RGB8, GL_RGB32F):
            channels = 3
        elif fmt in (GL_RED, GL_R32F):
            channels = 1
        else:
            raise ValueError(f"Unsupported format {fmt}")
        if ref_data is None:
            count = self.w * self.h * channels
            ref_data = (c_type * count)()
        buf_size = ctypes.sizeof(ref_data)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glGetTextureImage(self.id, level, fmt, dtype, buf_size, ref_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return ref_data