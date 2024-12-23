from .RenderGlobal import RenderGlobal

class GameObject:
    def __new__(cls,*args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.game_objects.append(instance)
        return instance

    def __init__(self):
        pass

    def preSrart(self):
        self.render_global = RenderGlobal.instance
        self.app = self.render_global.app
        self.window = self.render_global.window
        pass

    def start(self):
        pass

    def postStart(self):
        pass

    def update(self, dt: float, tps: float):
        pass

    def render(self, dt: float, fps: float):
        pass