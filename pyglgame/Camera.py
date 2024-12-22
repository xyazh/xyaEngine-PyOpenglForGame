from .CameraData import CarameData
from .GameObject import GameObject
from .RenderGlobal import RenderGlobal
from .FrameBuffer import FrameBuffer
from .shader.Shader import Shader
from .Size import Size


class Carmera(GameObject, CarameData):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.cameras.append(instance)
        return instance

    def __init__(self,size=None):
        super().__init__()
        super().__init_data__()
        self.shader: Shader = None
        self.should_update_frame_buffer = False
        self.size = size

    def preSrart(self):
        self.window_size = RenderGlobal.instance.window.size
        self.size.onChange(self.updataProjection)
        if self.size is None:
            self.size = self.window_size
        return super().preSrart()

    def start(self):
        self.frame_buffer = FrameBuffer(self.size.x, self.size.y, True)
        self.window_size.onChange(self.changeSize)
        return super().start()
    
    def changeSize(self, w, h):
        pass

    def updateFarmeBuffer(self):
        self.frame_buffer = FrameBuffer(self.size.x, self.size.y, True)

    def test(self):
        self.updataProjection(self.size.x, self.size.y)

    def drawToWindow(self):
        self.frame_buffer.drawToWindow()

    def use(self):
        if self.shader is None:
            self.shader = RenderGlobal.instance.dis_shader
        shader = self.shader
        shader.use()
        shader.uniformMatrix4fv("scale", self.scale)
        shader.uniformMatrix4fv("rotate", self.rotate)
        shader.uniformMatrix4fv("translate", self.translate)
        shader.uniformMatrix4fv("view", self.view)
        shader.uniformMatrix4fv("projection", self.projection)

    def release(self):
        if self.shader is None:
            self.shader = RenderGlobal.instance.dis_shader
        shader = self.shader
        shader.release()
