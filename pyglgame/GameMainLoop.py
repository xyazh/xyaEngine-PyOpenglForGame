from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .xyaHelper import *
from .RenderGlobal import RenderGlobal
from .shader.ShaderManager import ShaderManager
from .render.RenderBuffer import *


class GameMainLoop:
    def __init__(self) -> None:
        self.render_last_time = 0
        self.render_dt = 0
        self.render_global = None

    def start(self):
        self.render_global = RenderGlobal.instance
        shader = ShaderManager.loadShader("./res/shader/dis")
        shader.use()
        self.window = self.render_global.window
        self.app = self.render_global.app
        self.render_global.start()

        self.render_global.render_buffer = RenderBuffer(GL_STATIC_DRAW)
        buf_builder = self.render_global.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        buf_builder.pos(-1, -1, 0).tex(0, 0).end()  # bottom left
        buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left
        buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        buf_builder.pos(+1, +1, 0).tex(1, 1).end()    # top right
        buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left

    def doUpdate(self, dt: float, tps: float):
        self.render_global.updateLayer(dt, tps)

    def doRender(self, dt: float, fps: float):
        glClearColor(*self.render_global.bg)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render_global.using_shader.uniform2f(
            "win_wh", self.window.size.w, self.window.size.h)
        self.render_global.renderLayer(dt, fps)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        for camera in self.render_global.cameras:
            camera.windowCameraDraw()
        # glFlush()
        glutSwapBuffers()

    def updateLoop(self):
        xyaTimerFunc(10, self.doUpdate)

    def renderLoop(self):
        current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        self.render_dt = current_time - self.render_last_time
        self.render_last_time = current_time
        fps = 1.0 / self.render_dt if self.render_dt > 0 else 0
        self.window.clearMouseHit()
        self.window.clearKeyDown()
        self.doRender(self.render_dt, fps)

    def run(self):
        """while True:
            if glutGetWindow() == 0:  # 窗口已关闭
                pass
            glutMainLoopEvent()  # 处理单个事件
            glutPostRedisplay()  # 请求重绘
            self.renderLoop()"""
        self.updateLoop()
        glutIdleFunc(self.renderLoop)
