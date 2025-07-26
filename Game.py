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
import colorsys


# 黑体辐射算法 (简化版)


def generate_random_triangles(buffer_builder, count=200000, scale=1, center=(0, 0, 0)):
    for _ in range(count):
        cx, cy, cz = (random.uniform(-5000, 5000),
                      random.uniform(-5000, 5000),
                      random.uniform(20, 10000))
        # 每个三角形的三个顶点
        # 生成基础色温 (2000~15000K)
        scale = random.random()*30+1
        for _ in range(3):
            # 随机位置
            x = cx + random.uniform(-scale, scale)
            y = cy + random.uniform(-scale, scale)
            z = cz + random.uniform(-scale, scale)
            # 随机颜色

            # 随机色调（0~1），饱和度高，亮度高
            h = random.random()
            s = 1.0
            v = random.uniform(3.0, 10.0)  # HDR亮度

            r, g, b = colorsys.hsv_to_rgb(h, s, 1.0)
            r *= v
            g *= v
            b *= v

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
        RenderGlobal.instance.setPosition(0, 0, 10000)
        RenderGlobal.instance.updateGlobalUniforms()
        self.render_buffer.draw(False)
        RenderGlobal.instance.setPosition(0, 0, 0)
        RenderGlobal.instance.updateGlobalUniforms()
        self.render_buffer.draw(False)

        print(fps)
        return super().render(dt, fps)


class TestCamera(Camera):
    def __new__(cls, msaa_val: int = 4):
        return super().__new__(cls, msaa_val=8)

    def update(self, dt, tps):
        self.z += dt*100
        # self.r += dt*10
        if self.z > 10000:
            self.z = 0
        return super().update(dt, tps)


app = App()
app.window.setWindownSize((1920, 1080))

test_object = TestObject()
camera = TestCamera()
m = MPerspective()
m.updateAspectFromSize(960, 540)
camera.setProjection(m)
camera.switch()
camera.useBloom()

app.start()
