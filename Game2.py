from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.gameobject.animation.AnimationFrame import AnimationFrame
from OpenGL.GL import *
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.RenderGlobal import RenderGlobal
from pyglgame.shader.ShaderManager import ShaderManager
from pyglgame.render.TextureStorage2D import TextureStorage2D
from pyglgame.ResourceLocation import ResourceLocation
from pyglgame.render.Image import Image
from pyglgame.gameobject.camera.Camera import Camera
from pyglgame.gameobject.camera.m.MSimple2D import MSimple2D
import math
import glm

app = App()
app.window.setWindownSize((960, 540))


class TestObject(GameObject):
    def __init__(self):
        super().__init__()

    def start(self):
        self.animation = AnimationFrame(
            5, 6, 30, ResourceLocation("./res/img/006.png"),
            time=1,
            scale=(1, 1, 1),
            vertical_first=True
        )
        self.animation.setFlipX(True)
        glDisable(GL_CULL_FACE)
        return super().start()

    def render(self, dt, fps):
        self.animation.render(dt, fps)
        return super().render(dt, fps)


RenderGlobal.instance.setScale(glm.vec3(1/960, 1/540, 1))
obj = TestObject()
camera = Camera()
camera.setProjection(MSimple2D())
camera.switch()

app.start()
