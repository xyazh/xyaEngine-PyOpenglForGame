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
        self.use_bloom: bool = False
        self.bloom_ping: MSAAFrameBuffer = None
        self.bloom_pong: MSAAFrameBuffer = None
        self.bloom: MSAAFrameBuffer = None
        self.w: int = 960
        self.h: int = 540
        self.w1: int = 96
        self.h1: int = 54

    def start(self):
        super().start()
        self.size = RenderGlobal.instance.window.size
        self.createFrameBuffer()
        self.render_buffer = RenderBuffer.getWindownRenderBuffer()
        
        if self.use_bloom:
            if self.bloom_ping is None:
                self.bloom_ping = MSAAFrameBuffer(
                    self.w, self.h, param=GL_LINEAR,samples=8)
            if self.bloom_pong is None:
                self.bloom_pong = MSAAFrameBuffer(
                    self.w1, self.h1, param=GL_LINEAR)
            if self.bloom is None:
                fb = self.frame_buffer
                self.bloom = MSAAFrameBuffer(
                    fb.width, fb.height, fb.use_depth, fb.param, samples=fb.samples)

    def setProjection(self, m: MBase):
        self.m = m

    def createFrameBuffer(self):
        self.frame_buffer = MSAAFrameBuffer(
            self.size.w, self.size.h, use_depth=True, samples=self._msaa_val)

    def renderStart(self):
        if self.m is not None:
            self.m.setCameraPosAndPYR(
                self.x, self.y, self.z, self.p, self.t, self.r)
            self.m.setCameraUniforms()
        self.frame_buffer.drawStart()

    def renderEnd(self):
        self.frame_buffer.drawEnd()
        self.copyOrigiral()
        self.getHDRPix()
        self.pingpong()
        self.mixBloom()

    def copyOrigiral(self):
        self.bloom.drawStart()
        self.frame_buffer.drawToWindow(4)
        self.bloom.drawEnd()

    def getHDRPix(self):
        self.bloom_ping.drawStart()
        self.frame_buffer.drawToWindow(2)
        self.bloom_ping.drawEnd()

    def pingpong(self):
        ping_or_pong = 1
        for _ in range(4):
            ping_or_pong ^= 1
            if ping_or_pong == 1:
                self.bloom_ping.drawStart()
                self.bloom_pong.drawToWindow(3)
                self.bloom_ping.drawEnd()
            else:
                self.bloom_pong.drawStart()
                self.bloom_ping.drawToWindow(3)
                self.bloom_pong.drawEnd()

    def mixBloom(self):
        self.bloom_ping.bindTexture(GL_TEXTURE1)
        self.bloom.bindTexture(GL_TEXTURE0)
        self.frame_buffer.drawStart()
        self.bloom.drawToWindow(5)
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

    def useBloom(self, active: bool = True, w=1024, h=576, w1=480, h1=270):
        self.use_bloom = active
        self.w = w
        self.h = h
        self.w1 = w1
        self.h1 = h1
        if not active or not self.started:
            return
        if self.bloom_ping is None:
            self.bloom_ping = MSAAFrameBuffer(w, h, param=GL_LINEAR)
        if self.bloom_pong is None:
            self.bloom_pong = MSAAFrameBuffer(w1, h1, param=GL_LINEAR)
        if self.bloom is None:
            fb = self.frame_buffer
            self.bloom = MSAAFrameBuffer(
                fb.width, fb.height, fb.use_depth, fb.param, samples=fb.samples)
