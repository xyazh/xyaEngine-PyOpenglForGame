from pyglgame.gameobject.Camera3D import Camera3D
from pyglgame.gameobject.i.IWindowCamera import IWindowCamera
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.render.BufferBuilder import *
from pyglgame.math.Size import Size
from OpenGL.GL import *
from DemoBlock import DemoBlock, SIZE_X, SIZE_Y, SIZE_Z


class DemoCamera(Camera3D, IWindowCamera):
    def __init__(self):
        super().__init__(60, 0.1, 1000, auto_aspect=True, auto_size=True)

    def postStart(self):
        return super().postStart()
