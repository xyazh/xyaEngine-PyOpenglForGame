import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .xyaHelper import *
from .RenderGlobal import RenderGlobal
from .shader.ShaderManager import ShaderManager
from .render.RenderBuffer import *

import time


class GameMainLoop:
    def __init__(self) -> None:
        self.render_last_time = 0
        self.render_dt = 0
        self.render_global = None

    def start(self):
        self.nextFrame()
        self.drawProgressBar(-1, -0.8, 2, 0.1, 0.01)
        self.app = RenderGlobal.instance.app
        self.render_global = RenderGlobal.instance
        self.window = self.render_global.window
        self.app = self.render_global.app
        self.render_global.bloom_shader = ShaderManager.loadComputeShader(
            "./res/shader/computeBloom")
        self.render_global.fractal_noise_shader = ShaderManager.loadComputeShader(
            "./res/shader/computeFractalNoise")
        self.render_global.dis_shader = ShaderManager.loadShader(
            "./res/shader/dis")
        self.nextFrame()
        self.drawProgressBar(-1, -0.8, 2, 0.1, 0.03)
        for i in range(len(self.app.init_fucs)):
            self.nextFrame()
            self.drawProgressBar(-1, -0.8, 2, 0.1, (i+4)/100)
            func, call_back, args, kwargs = self.app.init_fucs[i]
            r = func(*args, **kwargs)
            if call_back:
                if r is None:
                    call_back()
                else:
                    call_back(r)
        self.drawProgressBar(-1, -0.8, 2, 0.1, 1.0)
        self.nextFrame()
        self.render_global.dis_shader.use()
        self.render_global.start()

    def nextFrame(self):
        glutSwapBuffers()
        if glutGetWindow() == 0:
            sys.exit(0)
        glutMainLoopEvent()
        glutPostRedisplay()
        glClearColor(0.1, 0.1, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def drawProgressBar(self, x, y, w, h, progress):
        progress = max(0.0, min(1.0, progress))
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0.2)
        glVertex3f(x + w, y, 0.2)
        glVertex3f(x + w, y + h, 0.2)
        glVertex3f(x, y + h, 0.2)
        glEnd()
        glColor3f(0.8, 0.8, 0.8)
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0.1)
        glVertex3f(x + w * progress, y, 0.1)
        glVertex3f(x + w * progress, y + h, 0.1)
        glVertex3f(x, y + h, 0.1)
        glEnd()

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
        xyaTimerFunc(10, self.doUpdate)
        glutIdleFunc(self.renderLoop)
