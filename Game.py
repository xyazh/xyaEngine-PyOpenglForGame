import glm
from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.RenderGlobal import RenderGlobal
from pyglgame.render.BufferBuilder import *
from pyglgame.gameobject.camera.Camera import Camera
from pyglgame.render.MSAAFrameBuffer import MSAAFrameBuffer
from pyglgame.gameobject.camera.m.MPerspective import MPerspective
from OpenGL.GL import *
from pyglgame.KEYS import *

import random
import colorsys


def generate_random_triangles(buffer_builder, count=20000, scale=1, center=(0, 0, 0)):
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
            """h = random.random()*5+1
            s = 1.0
            v = random.uniform(3.0, 10.0)  # HDR亮度

            r, g, b = colorsys.hsv_to_rgb(h, s, 1.0)
            r *= v
            g *= v
            b *= v
            """

            r = 0.3
            g = 0.0
            b = 0.0
            a = 1.0
            buffer_builder.pos(x, y, z).col(r, g, b, a).siz(20000).end()

def generate_random_points(buffer_builder, count=10000, scale=30000):
    for _ in range(count):
            # 随机位置
        x = random.uniform(-5000, 5000)
        y = random.uniform(-5000, 5000)
        z = random.uniform(20, 10000)
        # 随机颜色
        # 随机色调（0~1），饱和度高，亮度高
        # 随机色调（0~1），饱和度高，亮度高
        """h = random.random()*5+1
        s = 1.0
        v = random.uniform(3.0, 10.0)  # HDR亮度
        r, g, b = colorsys.hsv_to_rgb(h, s, 1.0)
        r *= v
        g *= v
        b *= v
        """
        l = 8
        r = random.random()*l
        g = random.random()*l
        b = random.random()*l
        a = 1.0
        buffer_builder.pos(x, y, z).col(r, g, b, a).siz(scale*random.random()).end()


class TestObject(GameObject):
    def __new__(cls):
        return super().__new__(cls)

    def start(self):
        render_buffer = RenderBuffer()
        buffer_builder = render_buffer.createBuffer(GL_POINTS, POS | COL | SIZ)
        #generate_random_triangles(buffer_builder)
        generate_random_points(buffer_builder)
        self.render_buffer = render_buffer
        self.render_buffer.build()
        self.render_buffer.buffer_builder.buffer.clear()

    def render(self, dt, fps):
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
    
    def __init__(self, msaa_val = 4):
        self.last_mouse = None
        self.forward = None
        self.right = None
        super().__init__(msaa_val)


    def renderStart(self):
        if self.m is not None:
            self.forward = self.m.setCameraPosAndPYR(
                self.x, self.y, self.z, self.p, self.t, self.r)
            self.right = glm.cross(self.forward, glm.vec3(0.0, 1.0, 0.0))
            self.m.setCameraUniforms()
        self.frame_buffer.drawStart()
    def update(self, dt, tps):
        if self.forward is None or self.right is None:
            return super().update(dt, tps)
        
        move_x, move_y, move_z = 0, 0, 0

        window = self.render_global.window
        speed = 1000 * dt
        if window.getKey("w") or window.getKey("W"):
            move_x += self.forward.x * speed
            move_y += self.forward.y * speed
            move_z += self.forward.z * speed
        if window.getKey("s") or window.getKey("S"):
            move_x -= self.forward.x * speed
            move_y -= self.forward.y * speed
            move_z -= self.forward.z * speed
        if window.getKey("d") or window.getKey("D"):
            move_x += self.right.x * speed
            move_z += self.right.z * speed
        if window.getKey("a") or window.getKey("A"):
            move_x -= self.right.x * speed
            move_z -= self.right.z * speed
        if window.getKey(KEY_SPACE):
            move_y += speed
        if window.getKey(KEY_SHIFT):
            move_y -= speed

        # 更新位置
        self.x += move_x
        self.y += move_y
        self.z += move_z

        # 鼠标控制旋转（保持不变）
        mouse = window.getOnMouse()
        if self.last_mouse is not None and window.mouse_left_button_on:
            self.t -= (mouse[0] - self.last_mouse[0]) * dt * 5
            self.p -= (mouse[1] - self.last_mouse[1]) * dt * 5
        self.last_mouse = mouse
        if not window.mouse_left_button_on:
            self.last_mouse = None
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
