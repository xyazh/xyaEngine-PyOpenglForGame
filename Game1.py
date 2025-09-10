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
from pyglgame.gameobject.camera.m.MOrthographic import MOrthographic


class TestObject(GameObject):
    def __new__(cls):
        return super().__new__(cls)

    def start(self):
        render_buffer = RenderBuffer()
        self.render_buffer = render_buffer
        self.cube_light = 2

    def render(self, dt, fps):
        buffer_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | COL)
        self.renderPlain(buffer_builder)
        self.renderCube(buffer_builder)

        self.render_buffer.draw()
        return super().render(dt, fps)

    def renderPlain(self, buffer_builder: BufferBuilder):
        buffer_builder.pos(-100, -5, +100).col(0.7, 0.7, 0.7, 1).end()
        buffer_builder.pos(+100, -5, +100).col(0.7, 0.7, 0.7, 1).end()
        buffer_builder.pos(-100, -5, -100).col(0.7, 0.7, 0.7, 1).end()
        buffer_builder.pos(+100, -5, +100).col(0.7, 0.7, 0.7, 1).end()
        buffer_builder.pos(+100, -5, -100).col(0.7, 0.7, 0.7, 1).end()
        buffer_builder.pos(-100, -5, -100).col(0.7, 0.7, 0.7, 1).end()

    def renderCube(self, buffer_builder: BufferBuilder):
        # 平移量
        offset_z = 10
        offset_y = 2

        # 顶点坐标（中心在原点，边长为2的立方体，Z方向整体平移+10）
        vertices = [
            (-1, -1 + offset_y, -1 + offset_z),  # 0 后左下
            (1, -1 + offset_y, -1 + offset_z),  # 1 后右下
            (1,  1 + offset_y, -1 + offset_z),  # 2 后右上
            (-1,  1 + offset_y, -1 + offset_z),  # 3 后左上
            (-1, -1 + offset_y,  1 + offset_z),  # 4 前左下
            (1, -1 + offset_y,  1 + offset_z),  # 5 前右下
            (1,  1 + offset_y,  1 + offset_z),  # 6 前右上
            (-1,  1 + offset_y,  1 + offset_z),  # 7 前左上
        ]

        # 定义每个面由两个三角形组成，保持面朝外的顶点顺序（逆时针）
        faces = [
            (0, 1, 2, 3),  # Back
            (5, 4, 7, 6),  # Front
            (4, 0, 3, 7),  # Left
            (1, 5, 6, 2),  # Right
            (3, 2, 6, 7),  # Top
            (4, 5, 1, 0),  # Bottom
        ]

        l =  self.cube_light

        for a, b, c, d in faces:
            buffer_builder.pos(*vertices[a]).col(1*l, 0*l, 1*l, 1).end()
            buffer_builder.pos(*vertices[b]).col(1*l, 0*l, 1*l, 1).end()
            buffer_builder.pos(*vertices[c]).col(1*l, 0*l, 1*l, 1).end()
            buffer_builder.pos(*vertices[a]).col(1*l, 0*l, 1*l, 1).end()
            buffer_builder.pos(*vertices[c]).col(1*l, 0*l, 1*l, 1).end()
            buffer_builder.pos(*vertices[d]).col(1*l, 0*l, 1*l, 1).end()

    def update(self, dt, tps):
        #self.cube_light += dt
        return super().update(dt, tps)


class TestCamera(Camera):
    def __new__(cls, msaa_val: int = 4):
        return super().__new__(cls, msaa_val=8)

    def __init__(self, msaa_val: int = 4):
        super().__init__(msaa_val)
        self.last_mouse = None
        self.forward = None
        self.right = None
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
        speed = 10 * dt
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
