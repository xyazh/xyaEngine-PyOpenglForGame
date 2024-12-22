from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .App import App
    from .BaseWindow import BaseWindow
    from .GameObject import GameObject
    from .shader.Shader import Shader
    from .Camera import Carmera


class RenderGlobal:
    instance = None

    def __new__(cls, app: "App" = None, window: "BaseWindow" = None):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            if app is None or window is None:
                raise TypeError("RenderGlobal.__new__() missing 2 required positional arguments: 'app' and 'window'")
            cls.instance.app = app
            cls.instance.window = window
            cls.instance.game_objects = []
            cls.instance.using_shader = None
            cls.instance.dis_shader = None
            cls.instance.dis_shader_1 = None
            cls.instance.cameras = []
        return cls.instance

    def __init__(self, app: "App" = None, window: "BaseWindow" = None) -> None:
        self.app: "App"
        self.window: "BaseWindow"
        self.game_objects: "list[GameObject]"
        self.using_shader: "Shader"
        self.dis_shader: "Shader"
        self.dis_shader_1: "Shader"
        self.cameras: "list[Carmera]" = []

    def start(self):
        pass
