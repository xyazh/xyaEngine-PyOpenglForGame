import glm
from typing import TYPE_CHECKING
from .math.Color import Color
from .RenderLayer import RenderLayer
if TYPE_CHECKING:
    from .App import App
    from .BaseWindow import BaseWindow
    from .shader.Shader import Shader
    from .gameobject.GameObject import GameObject
    from .gameobject.camera.Camera import Camera


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
        self.layers: dict[object, RenderLayer] = {0: self.using_layer}
        self.cameras: set[Camera] = set()

        # === Model transforms ===
        self._position = glm.vec3(0.0)
        self._rotation = glm.vec3(0.0)  # in degrees
        self._scale = glm.vec3(1.0)
        self._model_dirty = True
        self._model = glm.mat4(1.0)

    def __init__(self, *arg,  **kw) -> None:
        self.using_shader: "Shader" = None

    def start(self):
        for layer in self.layers.values():
            layer.start()

    def useLayer(self, layer):
        if layer in self.layers:
            self.using_layer = self.layers[layer]
            return
        self.using_layer = RenderLayer()
        self.layers[layer] = self.using_layer

    def updateLayer(self, dt: float, tps: float):
        for layer in self.layers.values():
            layer.update(dt, tps)

    def renderLayer(self, dt: float, fps: float):
        self.updateGlobalUniforms()
        self.using_shader.uniform1i("fuc", 0)
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

    def addWindowCamera(self, camera: "Camera"):
        self.cameras.add(camera)

    def removeWindowCamera(self, camera: "Camera"):
        if camera in self.cameras:
            self.cameras.remove(camera)

    def hasWindowCamera(self, camera: "Camera") -> bool:
        return camera in self.cameras

    # === Model Matrix ===
    def setPosition(self, x, y, z):
        self._position = glm.vec3(x, y, z)
        self._model_dirty = True

    def setRotation(self, rot: glm.vec3):
        self._rotation = rot
        self._model_dirty = True

    def setScale(self, scale: glm.vec3):
        self._scale = scale
        self._model_dirty = True

    @property
    def translate(self):
        return glm.translate(glm.mat4(1.0), self._position)

    @property
    def rotate(self):
        r = self._rotation
        mat = glm.mat4(1.0)
        mat = glm.rotate(mat, glm.radians(r.x), glm.vec3(1, 0, 0))
        mat = glm.rotate(mat, glm.radians(r.y), glm.vec3(0, 1, 0))
        mat = glm.rotate(mat, glm.radians(r.z), glm.vec3(0, 0, 1))
        return mat

    @property
    def scale(self):
        return glm.scale(glm.mat4(1.0), self._scale)

    @property
    def model(self):
        if self._model_dirty:
            self._model = self.translate * self.rotate * self.scale
            self._model_dirty = False
        return self._model

    # === Uniform Helper ===

    def updateGlobalUniforms(self, shader: "Shader" = None):
        if shader == None:
            shader = self.using_shader
        shader.uniformMatrix4fv("translate", self.translate)
        shader.uniformMatrix4fv("rotate", self.rotate)
        shader.uniformMatrix4fv("scale", self.scale)
        # 可选：shader.setMat4("model", self.model)
