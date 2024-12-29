import numpy as np
from pyglgame.math.Matrix import Matrix
from pyglgame.gameobject.Camera import Camera
from pyglgame.gameobject.i.IWindowCamera import IWindowCamera
from pyglgame.gameobject.i.IClicker import IClicker
from pyglgame.render.BufferBuilder import *
from pyglgame.render.FrameBufferFake import FrameBufferFake
from OpenGL.GL import *


class DemoCamera1(Camera, IWindowCamera):
    def __init__(self):
        super().__init__(auto_size=True)

    def postStart(self):
        return super().postStart()

    def creatFrameBuffer(self):
        return super().creatFrameBuffer()
        #return FrameBufferFake(self.size.w, self.size.h)

    def renderEnd(self):
        return super().renderEnd()

    def drawToWindow(self):
        return super().drawToWindow()
        # self.clicker_frame_buffer.drawToWindow()

    def renderTick(self, dt, fps):
        self.view = Matrix()
        return super().renderTick(dt, fps)
