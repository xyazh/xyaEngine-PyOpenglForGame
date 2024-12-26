import math
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
        self._eye = Vec3(0, 0, 0)
        self._center = Vec3(0, 0,-1)
        self._up = Vec3(0, 1, 0)
        self.view.lookAt(self._eye, self._center, self._up)

    def creatFrameBuffer(self):
        return FrameBuffer(
            self.size.w, self.size.h, use_depth=True, param=GL_LINEAR)

    def lookAtV(self, eye: Vec3, center: Vec3, up: Vec3):
        self._eye = eye
        self._center = center
        self._up = up
        self.view.lookAt(self._eye, self._center, self._up)

    def lookAt(self, eye: tuple | list, center: tuple | list, up: tuple | list):
        self.lookAtV(Vec3(*eye), Vec3(*center), Vec3(*up))

    def _position(self, x:float, y:float, z:float):
        dv = self._center - self._eye
        self._eye.x = x
        self._eye.y = y
        self._eye.z = z
        self._center = self._eye + dv

    def _pitchYaw(self, pitch: float, yaw: float):
        pitch_rad = math.radians(pitch)
        yaw_rad = math.radians(yaw)
        direction_x = math.cos(pitch_rad) * math.sin(yaw_rad)
        direction_y = math.sin(pitch_rad)
        direction_z = math.cos(pitch_rad) * math.cos(yaw_rad)
        self._center.x = self._eye.x + direction_x
        self._center.y = self._eye.y + direction_y
        self._center.z = self._eye.z + direction_z

    def positionAndPitchYaw(self, x: float, y: float, z: float, pitch: float, yaw: float):
        self._position(x, y, z)
        self._pitchYaw(pitch, yaw)
        self.view.lookAt(self._eye, self._center, self._up)

    def position(self,x,y,z):
        self._position(x, y, z)
        self.view.lookAt(self._eye, self._center, self._up)

    def pitchYaw(self,pitch:float,yaw:float):
        self._pitchYaw(pitch, yaw)
        self.view.lookAt(self._eye, self._center, self._up)

    def renderStart(self):
        self.framebuffer.drawStart()

    def renderEnd(self):
        self.framebuffer.drawEnd()

    def drawToWindow(self):
        self.framebuffer.drawToWindow()

    def useUniform(self, shader: Shader):
        shader.uniformMatrix4fv("view", self.view)
        shader.uniformMatrix4fv("projection", self.projection)
