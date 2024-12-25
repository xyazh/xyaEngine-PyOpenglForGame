from ..RenderGlobal import RenderGlobal

class GameObject:
    @property
    def should_render(self):
        return self._should_render
    
    @should_render.setter
    def should_render(self,value):
        self._should_render = value
        if value:
            RenderGlobal.instance.render_game_objects.add(self)
        elif self in RenderGlobal.instance.render_game_objects:
            RenderGlobal.instance.render_game_objects.remove(self)

    def __new__(cls,should_render=True,*args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.game_objects.append(instance)
        if should_render:
            RenderGlobal.instance.render_game_objects.add(instance)
        return instance

    def __init__(self,should_render=True):
        self._should_render = should_render

    def preSrart(self):
        self.render_global = RenderGlobal.instance
        self.shader = self.render_global.dis_shader
        self.app = self.render_global.app
        self.window = self.render_global.window

    def start(self):
        pass

    def postStart(self):
        pass

    def update(self, dt: float, tps: float):
        pass

    def render(self, dt: float, fps: float):
        pass

    def renderTick(self, dt: float, fps: float):
        pass