from .m.MBase import MBase
from ..GameObject import GameObject
from ...render.MSAAFrameBuffer import MSAAFrameBuffer
from ...render.RenderBuffer import RenderBuffer
from ...render.BufferBuilder import *
from ...RenderGlobal import RenderGlobal
from ...filler.Bloom import Bloom
from ...render.TextureStorage2D import TextureStorage2D
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
        self.render_global: RenderGlobal = None
        self.__level1 = 2
        self.__level2 = 4

    def start(self):
        super().start()
        self.render_global = RenderGlobal.instance
        self.size = RenderGlobal.instance.window.size
        self.createFrameBuffer()
        self.render_buffer = RenderBuffer.getWindownRenderBuffer()
        self.bloom: Bloom = None
        self.bloomed_texture: TextureStorage2D = None
        if self.use_bloom:
            self.bloom = Bloom(self.size.w, self.size.h,
                               self.__level1, self.__level2)
            self.bloom.sefTexture(self.frame_buffer.getTexture())

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
        if not self.use_bloom:
            return
        self.bloomed_texture = self.bloom.bloom()

    def draw(self, fuc: int = 1):
        if self.use_bloom:
            self.bloomed_texture.bind()
        else:
            self.frame_buffer.bindTexture()
        RenderGlobal.instance.using_shader.uniform1i("fuc", fuc)
        self.render_buffer.draw(False)

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
        if self.use_bloom:
            self.bloomed_texture.bind()
        else:
            self.frame_buffer.bindTexture()
        RenderGlobal.instance.using_shader.uniform1i("fuc", 1)
        self.render_buffer.draw(False)

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

    def useBloom(self, active: bool = True, level1: float = 2, level2: float = 4):
        self.use_bloom = active
        self.__level1 = level1
        self.__level2 = level2
        if not active or not self.started:
            return
        self.bloom = Bloom(self.size.w, self.size.h,
                           level1=level1, level2=level2)
        self.bloom.sefTexture(self.frame_buffer.getTexture())
