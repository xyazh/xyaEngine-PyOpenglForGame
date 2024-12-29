import math
from pyglgame.gameobject.Camera3D import Camera3D
from pyglgame.gameobject.i.IWindowCamera import IWindowCamera
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *
from pyglgame.gameobject.i.IClicker import IClicker

class DemoCamera(Camera3D, IWindowCamera, IClicker):
    def __init__(self):
        super().__init__(90, 0.1, 10000, auto_aspect=True, auto_size=True)
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.dw = 0
        self.dp = 0

    def getLayer(self):
        return 1

    def postStart(self):
        
        return super().postStart()
    def getPixelColor(self,x, y):
        return super().getPixelColor(x, y)

    def renderEnd(self):
        mos = self.window.getMouse()
        #print(self.getPixelColor(*mos))
        return super().renderEnd()
    def creatFrameBuffer(self):
        return super().creatFrameBuffer()
        #return FrameBufferMSAA(self.size.w, self.size.h, use_depth=True, param=GL_LINEAR)

    def keyBind(self, dt: float):
        if self.window.getKey("a"):
            self.dx += 10 * dt * math.cos(math.radians(self.dp))
            self.dz -= 10 * dt * math.sin(math.radians(self.dp))
        if self.window.getKey("d"):
            self.dx -= 10 * dt * math.cos(math.radians(self.dp))
            self.dz += 10 * dt * math.sin(math.radians(self.dp))
        if self.window.getKey("space"):
            self.dy += 10 * dt
        if self.window.getKey("shift"):
            self.dy -= 10 * dt
        if self.window.getKey("w"):
            self.dx += 10 * dt * math.sin(math.radians(self.dp))
            self.dz += 10 * dt * math.cos(math.radians(self.dp))
        if self.window.getKey("s"):
            self.dx -= 10 * dt * math.sin(math.radians(self.dp))
            self.dz -= 10 * dt * math.cos(math.radians(self.dp))
        if self.window.getKey("up"):
            self.dw += 45 * dt
            self.dw = min(self.dw, 89)
        if self.window.getKey("down"):
            self.dw -= 45 * dt
            self.dw = max(self.dw, -89)
        if self.window.getKey("left"):
            self.dp += 45 * dt
        if self.window.getKey("right"):
            self.dp -= 45 * dt

    def renderTick(self, dt, fps):
        self.positionAndPitchYaw(self.dx, self.dy, self.dz, self.dw, self.dp)
        self.keyBind(dt)
        return super().renderTick(dt, fps)

    def drawToWindow(self):
        super().drawToWindow()