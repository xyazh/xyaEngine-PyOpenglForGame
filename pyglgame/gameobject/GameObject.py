from ..RenderGlobal import RenderGlobal


class GameObject:
    def __new__(cls, is_camera: bool = False):
        obj = super().__new__(cls)
        RenderGlobal.instance.addToLayer(obj, is_camera=False)
        return obj

    def __init__(self):
        self.active: bool = True

    def __delete__(self):
        self.delete()

    def delete(self):
        self.active = False
        RenderGlobal.instance.removeFromLayer(self)

    def update(self, dt: float, tps: float):
        pass

    def render(self, dt: float, fps: float):
        pass
