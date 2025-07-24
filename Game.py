from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.RenderGlobal import RenderGlobal
from pyglgame.render.BufferBuilder import *
from pyglgame.gameobject.camera.Camera import Camera
from pyglgame.render.MSAAFrameBuffer import MSAAFrameBuffer
from pyglgame.gameobject.camera.m.MPerspective import MPerspective
from OpenGL.GL import *

import random


def generate_random_triangles(buffer_builder, count=10000000, scale=1, center=(0, 0, 0)):
    for _ in range(count):
        cx, cy, cz = (random.uniform(-100, 100),
                          random.uniform(-100, 100), 
                          random.uniform(20, 1000))
        # 每个三角形的三个顶点
        for _ in range(3):
            # 随机位置
            
            x = cx + random.uniform(-scale, scale)
            y = cy + random.uniform(-scale, scale)
            z = cz + random.uniform(-scale, scale)
            # 随机颜色
            r = random.random()
            g = random.random()
            b = random.random()
            a = 1.0
            buffer_builder.pos(x, y, z).col(r, g, b, a).end()


class TestObject(GameObject):
    def __new__(cls):
        return super().__new__(cls)

    def start(self):
        render_buffer = RenderBuffer()
        buffer_builder = render_buffer.createBuffer(GL_TRIANGLES, POS | COL)
        generate_random_triangles(buffer_builder)
        self.render_buffer = render_buffer

    def render(self, dt, fps):
        RenderGlobal.instance.using_shader.uniform1i("fuc", 0)
        self.render_buffer.draw(False)
        return super().render(dt, fps)


class TestCamera(Camera):
    def update(self, dt, tps):
        if dt > 1:
            return super().update(dt, tps)
        self.z += dt*10
        self.r += dt*10
        return super().update(dt, tps)


app = App()
app.window.setWindownSize((1920, 1080))

test_object = TestObject()
camera = TestCamera()
m = MPerspective()
m.updateAspectFromSize(960,540)
camera.setProjection(m)
camera.switch()

app.start()
