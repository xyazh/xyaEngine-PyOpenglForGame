from ..RenderGlobal import RenderGlobal


class GameObject:
    def __new__(cls, is_camera: bool = False):
        obj = super().__new__(cls)
        RenderGlobal.instance.addToLayer(obj, is_camera)
        return obj

    def __init__(self):
        self.active: bool = True
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.p: float = 0
        self.t: float = 0
        self.r: float = 0

    def __delete__(self):
        self.delete()

    def delete(self):
        self.active = False
        RenderGlobal.instance.removeFromLayer(self)

    def start(self):
        pass

    def update(self, dt: float, tps: float):
        pass

    def render(self, dt: float, fps: float):
        pass
