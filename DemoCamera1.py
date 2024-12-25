import math
from pyglgame.gameobject.Camera import Camera
from pyglgame.gameobject.i.IWindowCamera import IWindowCamera
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *
from DemoBlock import DemoBlock, SIZE_X, SIZE_Y, SIZE_Z


class DemoCamera1(Camera, IWindowCamera):
    def __init__(self, size):
        super().__init__(size)

    def postStart(self):
        self.test()
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.dp = 0
        self.dw = 0
        #self.rotate.rotate(180, (0, -1, 0))
        self.translate.translate(0, 0, -3)

        self.render_buffer = RenderBuffer(GL_STATIC_DRAW)
        self.buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        self.buf_builder.pos(-1.0, -1, 0).tex(0, 0).end()  # bottom left
        self.buf_builder.pos(+0.0, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(-1.0, +1, 0).tex(0, 1).end()   # top left
        self.buf_builder.pos(+0.0, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(+0.0, +1, 0).tex(1, 1).end()    # top right
        self.buf_builder.pos(-1.0, +1, 0).tex(0, 1).end()   # top left
        return super().postStart()

    def drawToWindow(self):
        return super().drawToWindow()
        self.frame_buffer.window_shader.use()
        self.frame_buffer.bindTexture()
        self.render_buffer.draw()
        self.frame_buffer.window_shader.release()

    def render(self, dt: float, fps: float):
        self.positionHeading(self.dx, self.dy, self.dz,self.dw,self.dp)
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
        return super().render(dt, fps)
