import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .xyaHelper import *
from .BufferBuilder import *
from .RenderBuffer import RenderBuffer
from .Image import Image
from .ResourceLocation import ResourceLocation
from .FrameBuffer import FrameBuffer
from .RenderGlobal import RenderGlobal


class GameMainLoop:
    def __init__(self) -> None:
        self.render_last_time = 0
        self.render_dt = 0

        self.render_buffer = RenderBuffer(GL_STREAM_DRAW)
        self.logo_img = Image(ResourceLocation("./res/img/logo.png", True))
        self.test_img = Image(ResourceLocation("./res/img/test.png", True))
        self.dz = -0.5

    def start(self):
        window_size = RenderGlobal.instance.window.size
        self.frame_buffer = FrameBuffer(window_size.w, window_size.h)

    def doUpdate(self, dt: float,tps: float):
        self.dz -= 0.1 * dt
        pass

    def doRender(self, dt: float, fps: float):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        buf_builder = self.render_buffer.createBuffer(
            GL_QUADS, POS | COL)
        buf_builder.pos(0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(-0.5, 0.5, 0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, 0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(0.5, -0.5, 0.5).col(1, 1, 0, 1).end()

        # 后面
        buf_builder.pos(0.5, 0.5, -0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(0.5, -0.5, -0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(-0.5, 0.5, -0.5).col(1, 1, 0, 1).end()

        # 左面
        buf_builder.pos(-0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(-0.5, 0.5, -0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(-0.5, -0.5, 0.5).col(1, 1, 0, 1).end()

        # 右面
        buf_builder.pos(0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(0.5, -0.5, 0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(0.5, 0.5, -0.5).col(1, 1, 0, 1).end()

        # 上面
        buf_builder.pos(0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(0.5, 0.5, -0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, 0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(-0.5, 0.5, 0.5).col(1, 1, 0, 1).end()

        # 下面
        buf_builder.pos(0.5, -0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, 0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(0.5, -0.5, -0.5).col(1, 1, 0, 1).end()

        self.render_buffer.draw()
        glFlush()

    def updateLoop(self):
        xyaTimerFunc(1, self.doUpdate)

    def renderLoop(self, _=None):
        current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        self.render_dt = current_time - self.render_last_time
        self.render_last_time = current_time
        fps = 1.0 / self.render_dt if self.render_dt > 0 else 0
        self.doRender(self.render_dt, fps)
        glutTimerFunc(1, self.renderLoop, 1)

    def run(self):
        self.updateLoop()
        self.renderLoop()
