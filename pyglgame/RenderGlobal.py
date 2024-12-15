from typing import TYPE_CHECKING
from .shader.ShaderManager import ShaderManager

if TYPE_CHECKING:
    from .App import App
    from .BaseWindow import BaseWindow


class RenderGlobal:
    instance = None

    def __new__(cls, app: "App", window: "BaseWindow"):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.app = app
            cls.instance.window = window
        return cls.instance

    def __init__(self, app: "App", window: "BaseWindow") -> None:
        self.app:"App"
        self.window:"BaseWindow"

    def start(self):
        self.dis_shader = ShaderManager.loadShader("./res/shader/dis")
        self.dis_shader_1 = ShaderManager.loadShader("./res/shader/dis1")
