from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .xyaHelper import *
from .BufferBuilder import *
from .RenderBuffer import RenderBuffer
from .Image import Image
from .ResourceLocation import ResourceLocation

import random


class GameMainLoop:
    def __init__(self) -> None:
        self.render_buffer = RenderBuffer(GL_STREAM_DRAW)
        self.logo_img = Image(ResourceLocation("./res/img/logo.png", True))

    def start(self):
        self.logo_tex = self.logo_img.getTexture()
        buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        buf_builder.pos(-1, -0.5, 0).tex(0,1).end()  # bottom left
        buf_builder.pos(1, -0.5, 0).tex(1,1).end()   # bottom right
        buf_builder.pos(-1, 0.5, 0).tex(0,0).end()   # top left
        buf_builder.pos(1, -0.5, 0).tex(1,1).end()   # bottom right
        buf_builder.pos(1, 0.5, 0).tex(1,0).end()    # top right
        buf_builder.pos(-1, 0.5, 0).tex(0,0).end()   # top left
        self.logo_tex.bind()

    def doUpdate(self):
        pass

    def doRender(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        self.render_buffer.draw()

        glFlush()

    def updateLoop(self):
        xyaTimerFunc(100, self.doUpdate)

    def renderLoop(self, _=None):
        self.doRender()
        glutTimerFunc(1, self.renderLoop, 1)

    def run(self):
        self.updateLoop()
        self.renderLoop()
