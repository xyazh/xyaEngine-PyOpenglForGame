from .GameObject import GameObject
from .RenderGlobal import RenderGlobal
from .FrameBuffer import FrameBuffer
from .shader.Shader import Shader
from .Size import Size
from .Matrix import Matrix
from .Vec3 import Vec3


class Camera(GameObject):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.cameras.append(instance)
        return instance

    def __init__(self,should_render=False):
        super().__init__(should_render)
        self.view = Matrix()
        self.projection = Matrix()

    def lookAtV(self, eye:Vec3, center:Vec3, up:Vec3):
        self.view.lookAt(eye, center, up)

    def lookAt(self, eye:tuple|list, center:tuple|list, up:tuple|list):
        self.lookAtV(Vec3(*eye), Vec3(*center), Vec3(*up))

    def useUniform(self, shader:Shader):
        shader.uniformMatrix4fv("view", self.view)
        shader.uniformMatrix4fv("projection", self.projection)