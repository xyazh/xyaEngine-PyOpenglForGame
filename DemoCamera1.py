import numpy as np
from pyglgame.math.Matrix import Matrix
from pyglgame.gameobject.Camera import Camera
from pyglgame.gameobject.i.IWindowCamera import IWindowCamera
from pyglgame.gameobject.i.IClicker import IClicker
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *


class DemoCamera1(Camera, IWindowCamera ,IClicker):
    def __init__(self):
        super().__init__(auto_size=True)

    def postStart(self):
        return super().postStart()

    def creatFrameBuffer(self):
        return super().creatFrameBuffer()

    def getPixelColor(self,x, y):
        return super().getPixelColor(x, y)

    def renderEnd(self):
        mos = self.window.getMouse()
        print(self.getPixelColor(*mos))
        return super().renderEnd()
    
    def drawToWindow(self):
        return super().drawToWindow()
        #self.clicker_frame_buffer.drawToWindow()

    def renderTick(self, dt, fps):
        self.view = Matrix()
        glDisable(GL_CULL_FACE)
        return super().renderTick(dt, fps)
