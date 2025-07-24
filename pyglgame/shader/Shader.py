import glm
from typing import TYPE_CHECKING
from OpenGL.GL import *

from ..RenderGlobal import RenderGlobal


class Shader:
    def __init__(self, shader: int):
        self.shader: int = shader

    def use(self):
        if RenderGlobal.instance.using_shader == self:
            return
        glUseProgram(self.shader)
        RenderGlobal.instance.using_shader = self

    def release(self):
        if RenderGlobal.instance.using_shader == self:
            return
        glUseProgram(0)
        RenderGlobal.instance.using_shader = None

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
