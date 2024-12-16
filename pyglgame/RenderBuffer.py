from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pyglgame.xyaHelper import *
from ctypes import sizeof, c_float, c_void_p
from .BufferBuilder import *
from .RenderGlobal import RenderGlobal
from .Matrix import Matrix


class RenderBuffer:
    def __init__(self, usage: int = GL_DYNAMIC_DRAW):
        self.vbo = -1
        self.usage = usage
        self.buffer_builder = None
        self.is_build = False
        self.matrix = Matrix()
        self.view = Matrix()

    def __del__(self):
        if self.vbo == -1:
            return
        glDeleteBuffers(1, [self.vbo])

    def getBuffer(self,):
        return self.buffer_builder

    def createBuffer(self, pri_type: int, format_type: int):
        self.buffer_builder = BufferBuilder(pri_type, format_type)
        return self.buffer_builder

    def build(self):
        if self.vbo == -1:
            glGenBuffers(1)
        vertices = self.buffer_builder.buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float),
                     (c_float * len(vertices))(*vertices), self.usage)

    def draw(self, use_dis_shader: bool = True):
        self.build()
        if use_dis_shader:
            RenderGlobal.instance.dis_shader.use()
            size = RenderGlobal.instance.window.size
            self.matrix.perspective(90.0, size.w / size.h, 0.1, 100.0)
            RenderGlobal.instance.dis_shader.uniform1i(
                "formatType", self.buffer_builder.format_type)
            RenderGlobal.instance.dis_shader.uniformMatrix4fv(
                "projection", self.matrix)
            RenderGlobal.instance.dis_shader.uniformMatrix4fv(
                "view", self.view)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            self.configureVertexAttributes()
            glDrawArrays(self.buffer_builder.pri_type,
                         0, self.buffer_builder.size)
            RenderGlobal.instance.dis_shader.release()
            return
        glDrawArrays(self.buffer_builder.pri_type, 0, self.buffer_builder.size)

    def configureVertexAttributes(self):
        f_size = sizeof(c_float)
        stride = f_size * len(self.buffer_builder.temp_buffer)
        offset = 0
        format_type = self.buffer_builder.format_type
        if format_type & POS:
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                                  stride, c_void_p(offset))
            offset += f_size * 3
        if format_type & COL:
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE,
                                  stride, c_void_p(offset))
            offset += f_size * 4
        if format_type & TEX:
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                                  stride, c_void_p(offset))
            offset += f_size * 2
        if format_type & NOR:
            glEnableVertexAttribArray(3)
            glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE,
                                  stride, c_void_p(offset))
            offset += f_size * 3
        if format_type & LIT:
            glEnableVertexAttribArray(4)
            glVertexAttribPointer(4, 2, GL_FLOAT, GL_FALSE,
                                  stride, c_void_p(offset))
            offset += f_size * 2
