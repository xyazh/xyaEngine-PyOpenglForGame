from typing import TYPE_CHECKING
from .math.Matrix import Matrix
from .math.Vec3 import Vec3
from .math.Color import Color
from .RenderLayers import RenderLayers
if TYPE_CHECKING:
    from .App import App
    from .BaseWindow import BaseWindow
    from .gameobject.GameObject import GameObject
    from .shader.Shader import Shader


class RenderGlobal:
    instance = None

    def __new__(cls, app: "App" = None, window: "BaseWindow" = None):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            if app is None or window is None:
                raise TypeError(
                    "RenderGlobal.__new__() missing 2 required positional arguments: 'app' and 'window'")
            cls.instance.__frist_init__(app, window)
        return cls.instance

    def __frist_init__(self, app: "App", window: "BaseWindow"):
        self.app: "App" = app
        self.window: "BaseWindow" = window
        self.game_objects: "list[GameObject]" = []
        self.using_shader: "Shader" = None
        self.dis_shader: "Shader" = None
        self.dis_shader_1: "Shader" = None
        self.click_checker_shader: "Shader" = None
        self.bg_color: Color = Color(0.0, 0.0, 0.0, 0.0)

        self.render_layer = RenderLayers()

        self.m_scale: Matrix = Matrix()
        self.m_rotate: Matrix = Matrix()
        self.m_translate: Matrix = Matrix()

    def __init__(self, app: "App" = None, window: "BaseWindow" = None) -> None:
        pass

    def start(self):
        pass

    def scale(self, x: float, y: float, z: float):
        self.m_scale.scale(x, y, z)

    def scaleV(self, v: Vec3):
        self.m_scale.scaleV(v)

    def rotate(self, angle: float, axis: tuple | list):
        self.m_rotate.rotate(angle, axis)

    def rotateV(self, angle: float, v: Vec3):
        self.m_rotate.rotateV(angle, v)

    def translate(self, x: float, y: float, z: float):
        self.m_translate.translate(x, y, z)

    def translateV(self, v: Vec3):
        self.m_translate.translateV(v)

    def useUniform(self, shader: "Shader"):
        shader.uniformMatrix4fv("scale", self.m_scale)
        shader.uniformMatrix4fv("rotate", self.m_rotate)
        shader.uniformMatrix4fv("translate", self.m_translate)
