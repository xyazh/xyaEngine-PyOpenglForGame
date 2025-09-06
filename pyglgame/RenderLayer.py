from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gameobject.GameObject import GameObject
    from .gameobject.camera.Camera import Camera


class RenderLayer:
    def __init__(self):
        self.objects: set["GameObject"] = set()
        self.cameras: set["Camera"] = set()
        self.__inited = False
        self.__starts: set["GameObject"] = set()

    def start(self):
        for obj in self.__starts:
            obj.start()
        self.__inited = True

    def addObject(self, obj: "GameObject"):
        self.objects.add(obj)
        if self.__inited:
            obj.start()
            return
        self.__starts.add(obj)

    def removeObject(self, obj: "GameObject"):
        if obj in self.objects:
            self.objects.remove(obj)

    def addCamera(self, camera: "Camera"):
        self.cameras.add(camera)
        self.addObject(camera)

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
            obj._render(dt, fps)
        for camera in self.cameras:
            camera.renderStart()
            for obj in self.objects:
                if obj.active:
                    obj.render(dt, fps)
            camera.renderEnd()
