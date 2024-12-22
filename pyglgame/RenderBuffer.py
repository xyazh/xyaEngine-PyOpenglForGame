from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pyglgame.xyaHelper import *
from ctypes import sizeof, c_float, c_void_p
from .BufferBuilder import *
from .RenderGlobal import RenderGlobal


class RenderBuffer:
    def __init__(self, usage: int = GL_DYNAMIC_DRAW):
        self.vbo = -1
        self.usage = usage
        self.buffer_builder = None
        self.is_build = False

    def __del__(self):
        if self.vbo == -1:
            return
        glDeleteBuffers(1, [self.vbo])

    def getBuffer(self,):
        return self.buffer_builder

    def createBuffer(self, pri_type: int, format_type: int):
        self.buffer_builder = BufferBuilder(pri_type, format_type)
        return self.buffer_builder

    def build(self,re_build:bool=True):
        if self.vbo == -1:
            self.vbo = glGenBuffers(1)
        elif not re_build:
            return
        vertices = self.buffer_builder.buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float),
                     (c_float * len(vertices))(*vertices), self.usage)

    def draw(self,re_build:bool=True):
        self.build(re_build)
        shader = RenderGlobal.instance.using_shader
        if shader is not None:
            shader.uniform1i("formatType", self.buffer_builder.format_type)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        self.configureVertexAttributes()
        glDrawArrays(self.buffer_builder.pri_type,0, self.buffer_builder.size)

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
        if format_type & SIZ:
            glEnableVertexAttribArray(5)
            glVertexAttribPointer(5, 1, GL_FLOAT, GL_FALSE,
                                  stride, c_void_p(offset))
            offset += f_size
