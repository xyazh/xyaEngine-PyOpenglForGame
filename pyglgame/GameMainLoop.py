from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .xyaHelper import *
from .RenderGlobal import RenderGlobal
from .shader.ShaderManager import ShaderManager


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

    def doUpdate(self, dt: float, tps: float):
        self.render_global.updateLayer(dt, tps)

    def doRender(self, dt: float, fps: float):
        glClearColor(*self.render_global.bg)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render_global.renderLayer(dt, fps)
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
        self.updateLoop()
        glutIdleFunc(self.renderLoop)
