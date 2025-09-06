import glm
from typing import TYPE_CHECKING
from OpenGL.GL import *

from ..RenderGlobal import RenderGlobal

UINT_MAP = {
    GL_TEXTURE0: ("tex0", 0),
    GL_TEXTURE1: ("tex1", 1),
    GL_TEXTURE2: ("tex2", 2),
    GL_TEXTURE3: ("tex3", 3),
    GL_TEXTURE4: ("tex4", 4),
    GL_TEXTURE5: ("tex5", 5),
    GL_TEXTURE6: ("tex6", 6),
    GL_TEXTURE7: ("tex7", 7),
    GL_TEXTURE8: ("tex8", 8),
    GL_TEXTURE9: ("tex9", 9),
    GL_TEXTURE10: ("tex10", 10),
    GL_TEXTURE11: ("tex11", 11),
    GL_TEXTURE12: ("tex12", 12),
    GL_TEXTURE13: ("tex13", 13),
    GL_TEXTURE14: ("tex14", 14),
    GL_TEXTURE15: ("tex15", 15),
    GL_TEXTURE16: ("tex16", 16),
    GL_TEXTURE17: ("tex17", 17),
    GL_TEXTURE18: ("tex18", 18),
    GL_TEXTURE19: ("tex19", 19),
    GL_TEXTURE20: ("tex20", 20),
    GL_TEXTURE21: ("tex21", 21),
    GL_TEXTURE22: ("tex22", 22),
    GL_TEXTURE23: ("tex23", 23),
    GL_TEXTURE24: ("tex24", 24),
    GL_TEXTURE25: ("tex25", 25),
    GL_TEXTURE26: ("tex26", 26),
    GL_TEXTURE27: ("tex27", 27),
    GL_TEXTURE28: ("tex28", 28),
    GL_TEXTURE29: ("tex29", 29),
    GL_TEXTURE30: ("tex30", 30),
    GL_TEXTURE31: ("tex31", 31),
}


class Shader:
    def __init__(self, shader: int):
        self.shader: int = shader

    def use(self):
        render_global = RenderGlobal.instance
        if render_global is None:
            glUseProgram(self.shader)
            print(self.shader)
            return
        if render_global.using_shader == self:
            return
        glUseProgram(self.shader)
        render_global.using_shader = self

    def release(self):
        render_global = RenderGlobal.instance
        if render_global is None:
            glUseProgram(0)
            return
        if render_global.using_shader == self:
            return
        glUseProgram(0)
        render_global.using_shader = None

    def getShaderId(self) -> int:
        return self.shader

    def uniformMatrix4fv(self, uniform_name: str, matrix: glm.mat4x4):
        loc = self.getLoc(uniform_name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(matrix))

    def boolean1b(self, name: str, b: bool):
        self.uniform1i(name, 1 if b else 0)

    def uniform1i(self, name: str, i: int):
        loc = self.getLoc(name)
        glUniform1i(loc, i)

    def uniform2i(self, name: str, i0: int, i1: int):
        loc = self.getLoc(name)
        glUniform2i(loc, i0, i1)

    def  uniform3i(self, name: str, i0: int, i1: int, i2: int):
        loc = self.getLoc(name)
        glUniform3i(loc, i0, i1, i2)

    def uniform4i(self, name: str, i0: int, i1: int, i2: int, i3: int):
        loc = self.getLoc(name)
        glUniform4i(loc, i0, i1, i2, i3)

    def uniformTex(self, uint):
        loc = self.getLoc(UINT_MAP[uint][0])
        glUniform1i(loc, UINT_MAP[uint][1])

    def uniform1f(self, name: str, f: float):
        loc = self.getLoc(name)
        glUniform1f(loc, f)

    def uniform2f(self, name: str, f0: float, f1: float):
        loc = self.getLoc(name)
        glUniform2f(loc, f0, f1)

    def uniform3f(self, name: str, f: float, g: float, h: float):
        loc = self.getLoc(name)
        glUniform3f(loc, f, g, h)

    def uniform4f(self, name: str, f: float, g: float, h: float, i: float):
        loc = self.getLoc(name)
        glUniform4f(loc, f, g, h, i)

    def getLoc(self, name: str):
        return glGetUniformLocation(self.getShaderId(), name)

    def dispatch(self, x: int, y: int = 1, z: int = 1):
        """Dispatch compute shader."""
        glDispatchCompute(x, y, z)

    def memoryBarrier(self, barrier=GL_ALL_BARRIER_BITS):
        """Call glMemoryBarrier after dispatch."""
        glMemoryBarrier(barrier)
