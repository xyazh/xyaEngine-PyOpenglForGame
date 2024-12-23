import glm
import math
from .Matrix import Matrix
from .Vec3 import Vec3


class CarameData:

    def __init__(self):
        self.__init_data__()

    def __init_data__(self):
        self._pitch: float = 0
        self._yaw: float = 0
        self._pos = Vec3(0, 0, 0)
        self._forward = Vec3(0, 0, 1)
        self._right = Vec3(1, 0, 0)
        self._up = Vec3(0, 1, 0)
        self._fov = 45
        self._near = 0.1
        self._far = 1000
        self.scale = Matrix()
        self.rotate = Matrix()
        self.translate = Matrix()
        self.view = Matrix()
        self.projection = Matrix()

    @property
    def x(self) -> float:
        return self._pos.x

    @x.setter
    def x(self, value: float):
        self._pos.x = value
        self.updateView()

    @property
    def y(self) -> float:
        self._pos.y

    @y.setter
    def y(self, value: float):
        self._pos.y = value
        self.updateView()

    @property
    def z(self) -> float:
        return self._pos.z

    @z.setter
    def z(self, value: float):
        self._pos.z = value
        self.updateView()

    @property
    def pos(self) -> Vec3:
        return self._pos

    @pos.setter
    def pos(self, value: Vec3):
        self._pos = value
        self.updateView()

    @property
    def pitch(self) -> float:
        return self._pitch

    @pitch.setter
    def pitch(self, value: float):
        self._pitch = value
        self.updateForward()
        self.updateView()

    @property
    def yaw(self) -> float:
        return self._yaw

    @yaw.setter
    def yaw(self, value: float):
        self._yaw = value
        self.updateForward()
        self.updateView()

    @property
    def roll(self) -> float:
        return self._roll

    @roll.setter
    def roll(self, value: float):
        self._roll = value
        self.updateForward()
        self.updateView()

    def position(self, x, y, z):
        self._pos.x = x
        self._pos.y = y
        self._pos.z = z
        self.updateView()

    def pitchYawRoll(self, pitch, yaw, roll):
        self._pitch = pitch
        self._yaw = yaw
        self._roll = roll
        self.updateForward()
        self.updateView()

    def positionAndPitchYawRoll(self, x, y, z, pitch, yaw, roll):
        self._pos.x = x
        self._pos.y = y
        self._pos.z = z
        self._pitch = pitch
        self._yaw = yaw
        self._roll = roll
        self.updateForward()
        self.updateView()

    def positionHeading(self, x=None, y=None, z=None, pitch=None, yaw=None, roll=None):
        if x is not None:
            self._pos.x = x
        if y is not None:
            self._pos.y = y
        if z is not None:
            self._pos.z = z
        if pitch is not None:
            self._pitch = pitch
        if yaw is not None:
            self._yaw = yaw
        if roll is not None:
            self._roll = roll
        self.updateForward()
        self.updateView()

    def fovNearFar(self, fov, aspect_ratio, near, far):
        self._fov = fov
        self._near = near
        self._far = far
        self.projection.perspective(self._fov, aspect_ratio, self._near, self._far)

    def projectionArr(self, aspect_ratio, fov=None, near=None, far=None):
        if fov is not None:
            self._fov = fov
        if near is not None:
            self._near = near
        if far is not None:
            self._far = far
        self.projection.perspective(self._fov, aspect_ratio, self._near, self._far)

    def updateForward(self):
        p = self._pitch
        y = self._yaw
        forward = Vec3(
            math.cos(math.radians(p)) * math.sin(math.radians(y)),
            math.sin(math.radians(p)),
            math.cos(math.radians(p)) * math.cos(math.radians(y))
        )
        self._forward = glm.normalize(forward)

    def updateView(self):
        self.view.lookAt(self._pos, self._pos + self._forward, self._up)

    def updataProjection(self, w, h):
        self.projection.perspective(self._fov, w / h, self._near, self._far)
