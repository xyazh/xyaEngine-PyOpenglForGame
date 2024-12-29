from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .xyaHelper import *
from .RenderGlobal import RenderGlobal
from .gameobject.i.IWindowCamera import IWindowCamera
from .gameobject.i.IClicker import IClicker
from .gameobject.Camera import Camera
from .shader.ShaderManager import ShaderManager


class GameMainLoop:
    def __init__(self) -> None:
        self.render_last_time = 0
        self.render_dt = 0
        self.render_global = None

    def start(self):
        self.render_global = RenderGlobal.instance
        self.window = self.render_global.window
        self.game_objects = self.render_global.game_objects
        self.render_layer = self.render_global.render_layer
        self.render_global.dis_shader = ShaderManager.loadShader("./res/shader/dis")
        self.render_global.dis_shader_1 = ShaderManager.loadShader("./res/shader/dis1")
        self.render_global.click_checker_shader = ShaderManager.loadShader("./res/shader/click_check")
        for game_object in self.game_objects:
            game_object.preSrart()
        for game_object in self.game_objects:
            game_object.start()
        for game_object in self.game_objects:
            game_object.postStart()

        for layer in self.render_layer.layers.values():
            cameras = layer.render_cameras
            for camera in cameras:
                camera:Camera|IClicker
                if isinstance(camera, IClicker):
                    camera.__init_clicker__()


    def doUpdate(self, dt: float,tps: float):
        for game_object in self.game_objects:
            game_object.update(dt, tps)

    def doRender(self, dt: float, fps: float):
        glClearColor(*self.render_global.bg_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        for game_object in self.game_objects:
            game_object.renderTick(dt, fps)
            
        glDepthMask(GL_TRUE)
        glEnable(GL_DEPTH_TEST)
        for layer in self.render_layer.layers.values():
            cameras = layer.render_cameras
            render_game_objects = layer.render_game_objects
            for camera in cameras:
                camera:Camera|IClicker
                camera.renderStart()
                for game_object in render_game_objects:
                    shader = game_object.shader
                    shader.use()
                    self.render_global.useUniform(shader)
                    camera.useUniform(shader)
                    game_object.render(dt, fps)
                    shader.release()
                camera.renderEnd()
                if isinstance(camera,IClicker):
                    camera.renderClickerStart()
                    for game_object in render_game_objects:
                        if not game_object.clickable:
                            continue
                        shader = self.render_global.click_checker_shader
                        shader.use()
                        self.render_global.useUniform(shader)
                        camera.useUniform(shader)
                        camera.setDataColorUniform(shader, *game_object.data_color)
                        game_object.render(dt, fps)
                        shader.release()
                    camera.renderClickerEnd()
                    camera.onHoverMouse(render_game_objects)
            

        glDepthMask(GL_FALSE)
        glDisable(GL_DEPTH_TEST)
        for layer in self.render_layer.layers.values():
            cameras = layer.render_cameras
            for camera in cameras:
                if isinstance(camera, IWindowCamera):
                    camera.drawToWindow()

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
