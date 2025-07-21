from typing import TYPE_CHECKING
from .math.Color import Color
from .RenderLayer import RenderLayer
if TYPE_CHECKING:
    from .App import App
    from .BaseWindow import BaseWindow
    from .shader.Shader import Shader
    from .gameobject.GameObject import GameObject


class RenderGlobal:
    instance = None

    def __new__(cls, *arg, app: "App" = None, window: "BaseWindow" = None, **kw):
        if cls.instance is None:
            if app is None or window is None:
                raise TypeError(
                    "RenderGlobal.__new__() missing 2 required positional arguments: 'app' and 'window'")
            cls.instance: RenderGlobal = super().__new__(cls)
            cls.instance.__frist_init__(app, window)
        return cls.instance

    def __frist_init__(self, app: "App", window: "BaseWindow"):
        self.app: "App" = app
        self.window: "BaseWindow" = window
        self.bg: Color = Color(0, 0, 0)
        self.using_shader = None
        self.using_layer = RenderLayer()
        self.layers: dict[object:RenderLayer] = {0: self.using_layer}

    def __init__(self, *arg,  **kw) -> None:
        pass

    def start(self):
        self.using_shader: "Shader" = None

    def useLayer(self, layer):
        if layer in self.layers:
            self.using_layer = self.layers[layer]
            return
        self.using_layer = RenderLayer()
        self.layers[layer] = self.using_layer

    def updateLayer(self, dt: float, tps: float):
        layer: RenderLayer
        for layer in self.layers.values():
            layer.update(dt, tps)

    def renderLayer(self, dt: float, fps: float):
        layer: RenderLayer
        for layer in self.layers.values():
            layer.render(dt, fps)

    def addToLayer(self, obj: "GameObject", is_camera: bool = False):
        if is_camera:
            self.using_layer.addCamera(obj)
            return
        self.using_layer.addObject(obj)

    def removeFromLayer(self, obj: "GameObject", is_camera: bool = False):
        if is_camera:
            self.using_layer.removeCamera(obj)
            return
        self.using_layer.removeObject(obj)
