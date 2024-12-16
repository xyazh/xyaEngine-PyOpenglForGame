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

    def start(self):
        window_size = RenderGlobal.instance.window.size
        self.frame_buffer = FrameBuffer(window_size.w, window_size.h)
        self.test_tex = self.test_img.getTexture()
        buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX | COL)
        buf_builder.pos(-1, -1, 0).tex(0, 0).col(1, 0, 0, 1).end()  # bottom left
        buf_builder.pos(1, -1, 0).tex(1, 0).col(0, 1, 0, 1).end()   # bottom right
        buf_builder.pos(-1, 1, 0).tex(0, 1).col(1, 0, 1, 1).end()   # top left
        buf_builder.pos(1, -1, 0).tex(1, 0).col(0, 1,0, 1).end()   # bottom right
        buf_builder.pos(1, 1, 0).tex(1, 1).col(0, 0, 1, 1).end()    # top right
        buf_builder.pos(-1, 1, 0).tex(0, 1).col(1, 0, 1, 1).end()   # top left

    def doUpdate(self, dt: float,tps: float):
        pass

    def doRender(self, dt: float, fps: float):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.test_tex.bind()
        self.frame_buffer.draw(self.render_buffer.draw)
        self.frame_buffer.drawToWindow()
        glFlush()

    def updateLoop(self,):
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
