from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gameobject.GameObject import GameObject
    from .gameobject.Camera import Camera


class Layer:
    def __init__(self,level:int):
        self.level = level
        self.render_game_objects: "set[GameObject]" = set()
        self.render_cameras: "list[Camera]" = []

class RenderLayers:
    @staticmethod
    def layer(level:int):
        def decorator(cls:"GameObject.__class__"):
            cls._layer = level
            return cls
        return decorator

    def __init__(self):
        self.layers: "dict[int,Layer]" = {}

    def addGameObject(self, game_object: "GameObject", level: int = None) -> None:
        if level is None:
            level = game_object.getLayer()
        if level not in self.layers:
            self.layers[level] = Layer(level)
        self.layers[level].render_game_objects.add(game_object)

    def removeGameObject(self, game_object: "GameObject", level: int = None) -> None:
        if level is None:
            level = game_object.getLayer()
        if level not in self.layers:
            self.layers[level] = Layer(level)
        self.layers[level].render_game_objects.remove(game_object)


    def appendCamera(self, camera: "Camera", level: int = None) -> None:
        if level is None:
            level = camera.getLayer()
        if level not in self.layers:
            self.layers[level] = Layer(level)
        self.layers[level].render_cameras.append(camera)
