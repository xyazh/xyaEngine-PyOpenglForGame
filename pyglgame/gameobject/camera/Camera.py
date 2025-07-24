from .m.MBase import MBase
from ..GameObject import GameObject
from ...render.MSAAFrameBuffer import MSAAFrameBuffer
from ...render.RenderBuffer import RenderBuffer
from ...render.BufferBuilder import *
from ...RenderGlobal import RenderGlobal
from OpenGL.GL import *


class Camera(GameObject):
    def __new__(cls, msaa_val: int = 4):
        return super().__new__(cls, is_camera=True)

    def __init__(self, msaa_val: int = 4):
        super().__init__()
        self._msaa_val = msaa_val
        self.m: MBase = None

    def start(self):
        super().start()
        self.size = RenderGlobal.instance.window.size
        self.createFrameBuffer()
        self.render_buffer = RenderBuffer(GL_STATIC_DRAW)
        self.buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        self.buf_builder.pos(-1, -1, 0).tex(0, 0).end()  # bottom left
        self.buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left
        self.buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(+1, +1, 0).tex(1, 1).end()    # top right
        self.buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left

    def setProjection(self, m: MBase):
        self.m = m

    def createFrameBuffer(self):
        self.frame_buffer = MSAAFrameBuffer(
            self.size.w, self.size.w, use_depth=True, samples=self._msaa_val)

    def renderStart(self):
        if self.m is not None:
            self.m.setCameraPosAndPYR(
                self.x, self.y, self.z, self.p, self.t, self.r)
            self.m.setCameraUniforms()
        self.frame_buffer.drawStart()

    def renderEnd(self):
        self.frame_buffer.drawEnd()

    def draw(self):
        self.frame_buffer.drawToWindow()

    def windowCameraSet(self,
                        bottom_left: tuple[float, float, float],
                        bottom_right: tuple[float, float, float],
                        top_left: tuple[float, float, float],
                        top_right: tuple[float, float, float]):
        self.buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        self.buf_builder.pos(*bottom_left).tex(0, 0).end()
        self.buf_builder.pos(*bottom_right).tex(1, 0).end()
        self.buf_builder.pos(*top_left).tex(0, 1).end()
        self.buf_builder.pos(*bottom_right).tex(1, 0).end()
        self.buf_builder.pos(*top_right).tex(1, 1).end()
        self.buf_builder.pos(*top_left).tex(0, 1).end()

    def windowCameraDraw(self):
        self.frame_buffer.bindTexture()
        RenderGlobal.instance.using_shader.uniform1i("fuc", 1)
        self.render_buffer.draw()

    def switch(self, state: bool = None):
        rg = RenderGlobal.instance
        if state is None:
            if rg.hasWindowCamera(self):
                rg.removeWindowCamera(self)
            else:
                rg.addWindowCamera(self)
        elif state:
            rg.addWindowCamera(self)
        else:
            rg.removeWindowCamera(self)
