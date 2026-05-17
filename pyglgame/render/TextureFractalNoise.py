import glm
from OpenGL.GL import *
from .TextureBase import TextureBase
from .TextureStorage2D import TextureStorage2D
from ..shader.ShaderManager import ShaderManager
from ..RenderGlobal import RenderGlobal


class TextureFractalNoise(TextureBase):
    def __init__(self, w: int, h: int, value: float = 0.0, amplitude: float = 0.5, frequency: float = 0.5):
        self.w = w
        self.h = h
        self.texture_storage = TextureStorage2D(int(w), int(h), unit=7)
        self.time = glm.vec3(0.0)
        self.value = value
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = glm.vec2(0.0)
        self.compute_shader = ShaderManager.loadComputeShader(
            "./res/shader/computeFractalNoise")

    def render(self, dt, fps):
        self.dis_shader = RenderGlobal.instance.using_shader
        self.compute_shader.use()
        self.compute_shader.uniform3f("u_time", *self.time)
        self.compute_shader.uniform1f("u_value", self.value)
        self.compute_shader.uniform1f("u_amplitude", self.amplitude)
        self.compute_shader.uniform1f("u_frequency", self.frequency)
        self.compute_shader.uniform2f("u_offset", *self.offset)
        self.compute_shader.dispatch(
            self.texture_storage.group_x, self.texture_storage.group_y, 1)
        self.compute_shader.memoryBarrier()
        self.dis_shader.use()
        self.time += glm.vec3(dt/10)
        #self.offset += glm.vec2(dt/10)

    def bindUnit(self, unit=0):
        self.texture_storage.bindUnit(unit)

    def bind(self, unit=GL_TEXTURE0):
        self.texture_storage.bind(unit)
