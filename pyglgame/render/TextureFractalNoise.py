import glm
from OpenGL.GL import *
from .TextureBase import TextureBase
from .TextureStorage2D import TextureStorage2D
from ..shader.ShaderManager import ShaderManager
from ..RenderGlobal import RenderGlobal


class TextureFractalNoise(TextureStorage2D):
    def __init__(self, w: int, h: int, value: float = 0.0, amplitude: float = 0.5, frequency: float = 0.5):
        super().__init__(int(w), int(h), unit=7)
        self.time = glm.vec3(0.0)
        self.value = value
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = glm.vec2(0.0)
        self.compute_shader = RenderGlobal.instance.fractal_noise_shader

    def render(self, dt, fps):
        self.bindUnit(7)
        self.dis_shader = RenderGlobal.instance.using_shader
        self.compute_shader.use()
        self.compute_shader.uniform3f("u_time", *self.time)
        self.compute_shader.uniform1f("u_value", self.value)
        self.compute_shader.uniform1f("u_amplitude", self.amplitude)
        self.compute_shader.uniform1f("u_frequency", self.frequency)
        self.compute_shader.uniform2f("u_offset", *self.offset)
        self.compute_shader.dispatch(
            self.group_x, self.group_y, 1)
        self.compute_shader.memoryBarrier()
        self.dis_shader.use()
        self.time += glm.vec3(dt/10)