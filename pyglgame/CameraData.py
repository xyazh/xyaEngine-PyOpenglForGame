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
        self._forward = Vec3(0, 0, -1)
        self._right = Vec3(1, 0, 0)
        self._up = Vec3(0, 1, 0)
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

    def updateForward(self):
        p = self._pitch
        y = self._yaw
        forward = Vec3(
            math.cos(math.radians(p)) * math.sin(math.radians(y)),
            math.sin(math.radians(p)),
            math.cos(math.radians(p)) * math.cos(math.radians(y))
        )
        self._forward = glm.normalize(forward)
        self._right = glm.normalize(glm.cross(forward, self._up))

    def updateView(self):
        self.view.lookAt(self._pos, self._pos + self._forward, self._up)

    def updataProjection(self, w, h):
        self.projection.perspective(45.0, w / h, 0.1, 100.0)