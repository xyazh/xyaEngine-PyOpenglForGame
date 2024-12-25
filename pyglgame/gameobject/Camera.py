from OpenGL.GL import GL_LINEAR
from .GameObject import GameObject
from ..RenderGlobal import RenderGlobal
from ..render.FrameBuffer import FrameBuffer
from ..shader.Shader import Shader
from ..math.Size import Size
from ..math.Matrix import Matrix
from ..math.Vec3 import Vec3


class Camera(GameObject):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.cameras.append(instance)
        return instance

    def preSrart(self):
        super().preSrart()
        if self.size is None:
            self.size = Size(self.window.size.x, self.window.size.y)
        if self._auto_size:
            self.window.size.onChange(self.autoSize)

        self.framebuffer = self.creatFrameBuffer()

    def __init__(self, size: Size = None, auto_size: bool = False, should_render=False):
        super().__init__(should_render)
        self.view = Matrix()
        self.projection = Matrix()
        self._auto_size = auto_size
        self.size = size

    def autoSize(self, w, h):
        self.size.updateSize(w, h)

    def creatFrameBuffer(self):
        return FrameBuffer(
            self.size.w, self.size.h, use_depth=True, param=GL_LINEAR)

    def lookAtV(self, eye: Vec3, center: Vec3, up: Vec3):
        self.view.lookAt(eye, center, up)

    def lookAt(self, eye: tuple | list, center: tuple | list, up: tuple | list):
        self.lookAtV(Vec3(*eye), Vec3(*center), Vec3(*up))

    def renderStart(self):
        self.framebuffer.drawStart()

    def renderEnd(self):
        self.framebuffer.drawEnd()

    def drawToWindow(self):
        self.framebuffer.drawToWindow()

    def useUniform(self, shader: Shader):
        shader.uniformMatrix4fv("view", self.view)
        shader.uniformMatrix4fv("projection", self.projection)
