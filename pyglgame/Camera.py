from .CameraData import CarameData
from .GameObject import GameObject
from .RenderGlobal import RenderGlobal


class Carmera(GameObject, CarameData):
    def __init__(self):
        super().__init__()
        super().__init_data__()

    def start(self):
        size = RenderGlobal().window.size
        size.onChange(self.updataProjection)
        return super().start()
    
    def test(self):
        self.translate.translate(0, 0, -3)
        self.projection.perspective(45.0, 1920 / 1080, 0.1, 1000.0)

    def use(self):
        shader = RenderGlobal.instance.using_shader
        shader.uniformMatrix4fv("scale", self.scale)
        shader.uniformMatrix4fv("rotate", self.rotate)
        shader.uniformMatrix4fv("translate", self.translate)
        shader.uniformMatrix4fv("view", self.view)
        shader.uniformMatrix4fv("projection", self.projection)
