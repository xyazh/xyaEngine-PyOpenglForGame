from .RenderGlobal import RenderGlobal

class GameObject:
    def __new__(cls,*args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal().game_objects.append(instance)
        return instance

    def __init__(self):
        pass

    def start(self):
        self.shader = RenderGlobal().dis_shader
        pass

    def update(self, dt: float, tps: float):
        pass

    def render(self, dt: float, fps: float):
        pass