import glm
from OpenGL.GL import *
from .TextureBase import TextureBase
from .TextureStorage2D import TextureStorage2D


class TextureFractalNoise(TextureBase):
    def __init__(self, w: int, h: int,
                 scale: float = 0.2, velocity: tuple | glm.vec3 = (0, 0, 0), speed: float = 1.0, contrast: float = 1,
                 texture_storage: TextureStorage2D = None):
        if texture_storage is None:
            texture_storage = TextureStorage2D(w, h)
        self.w = w
        self.h = h
        self.texture_storage = texture_storage
        self.scale = scale
        self.velocity = velocity
        self.speed = speed
        self.contrast = contrast
        
