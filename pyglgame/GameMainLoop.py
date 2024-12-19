import random
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
        self.render_global.dis_shader = ShaderManager.loadShader("./res/shader/dis")
        self.render_global.dis_shader_1 = ShaderManager.loadShader("./res/shader/dis1")
        for game_object in self.render_global.game_objects:
            game_object.start()

    def doUpdate(self, dt: float,tps: float):
        for game_object in self.render_global.game_objects:
            game_object.update(dt, tps)

    def doRender(self, dt: float, fps: float):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for game_object in self.render_global.game_objects:
            game_object.render(dt, fps)
        glutSwapBuffers()

    def updateLoop(self):
        xyaTimerFunc(10, self.doUpdate)

    def renderLoop(self):
        current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        self.render_dt = current_time - self.render_last_time
        self.render_last_time = current_time
        fps = 1.0 / self.render_dt if self.render_dt > 0 else 0
        self.doRender(self.render_dt, fps)

    def run(self):
        self.updateLoop()
        glutIdleFunc(self.renderLoop)
