from pyglgame.Camera import Carmera
from pyglgame.IWindowCamera import IWindowCamera
from pyglgame.RenderBuffer import RenderBuffer
from pyglgame.BufferBuilder import *
from OpenGL.GL import *
from DemoBlock import DemoBlock, SIZE_X, SIZE_Y, SIZE_Z


class DemoCamera(Carmera, IWindowCamera):
    def __init__(self,size):
        super().__init__(size)

    def postStart(self):
        self.test()
        self.dz = 0.1
        self.rotate.rotate(180, (0, -1, 0))
        self.translate.translate(0, 0, -3)

        self.render_buffer = RenderBuffer(GL_STATIC_DRAW)
        self.buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        self.buf_builder.pos(-0.5, -1, 0).tex(0, 0).end()  # bottom left
        self.buf_builder.pos(+0.5, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(-0.5, +1, 0).tex(0, 1).end()   # top left
        self.buf_builder.pos(+0.5, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(+0.5, +1, 0).tex(1, 1).end()    # top right
        self.buf_builder.pos(-0.5, +1, 0).tex(0, 1).end()   # top left        
        return super().postStart()
    
    def drawToWindow(self):
        self.frame_buffer.window_shader.use()
        self.frame_buffer.bindTexture()
        self.render_buffer.draw()
        self.frame_buffer.window_shader.release()

    def render(self, dt: float, fps: float):
        self.position(-SIZE_X/2, SIZE_Y/2+1, -self.dz)
        self.dz += dt * self.dz / 10
        return super().render(dt, fps)
