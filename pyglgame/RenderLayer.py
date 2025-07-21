from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gameobject.GameObject import GameObject
    from .gameobject.Camera import Camera


class RenderLayer:
    def __init__(self):
        self.objects: set["GameObject"] = set()
        self.cameras: set["Camera"] = set()

    def addObject(self, obj: "GameObject"):
        self.objects.add(obj)

    def removeObject(self, obj: "GameObject"):
        if obj in self.objects:
            self.objects.remove(obj)

    def addCamera(self, camera: "Camera"):
        self.objects.add(camera)
        self.cameras.add(camera)

    def removeCamera(self, camera: "Camera"):
        if camera in self.objects:
            self.objects.remove(camera)
        if camera in self.cameras:
            self.cameras.remove(camera)

    def update(self, dt: float, tps: float):
        for obj in self.objects:
            if obj.active:
                obj.update(dt, tps)

    def render(self, dt: float, fps: float):
        for obj in self.objects:
            if obj.active:
                obj.render(dt, fps)
