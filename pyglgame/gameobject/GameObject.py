from ..RenderGlobal import RenderGlobal


class GameObject:
    @property
    def should_render(self):
        return self._should_render

    @should_render.setter
    def should_render(self, value):
        self._should_render = value
        render_layer = RenderGlobal.instance.render_layer
        if value:
            render_layer.addGameObject(self)
        else:
            render_layer.removeGameObject(self)

    def __new__(cls, should_render=True, *args, **kwargs):
        instance = super().__new__(cls)
        RenderGlobal.instance.game_objects.append(instance)
        if should_render:
            RenderGlobal.instance.render_layer.addGameObject(instance)
        return instance
    
    def getLayer(self)->int:
        return 0

    def __init__(self, should_render=True):
        self._should_render = should_render
        self.clickable: bool = False
        self.data_color = (0, 0, 0, 0)

    def isDataColor(self, r, g, b, a) -> bool:
        return (self.data_color[0] == r and \
                self.data_color[1] == g and \
                self.data_color[2] == b)

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
