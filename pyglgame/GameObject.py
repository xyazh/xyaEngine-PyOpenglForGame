from .RenderGlobal import RenderGlobal

class GameObject:
    def __new__(cls,*args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.game_objects.append(instance)
        return instance

    def __init__(self):
        pass

    def preSrart(self):
        pass

    def start(self):
        pass

    def postStart(self):
        pass

    def update(self, dt: float, tps: float):
        pass

    def render(self, dt: float, fps: float):
        pass