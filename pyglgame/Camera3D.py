from .Camera import Camera


class Camera3D(Camera):
    @staticmethod
    def test()->"Camera3D":
        return Camera3D(60,0.1,1000,auto_aspect=True)
    
    def __init__(self, fov: float, near: float, far: float, aspect_ratio: float = None, should_render=False,auto_aspect=False):
        super().__init__(should_render)
        self._fov = fov
        self._near = near
        self._far = far
        self._aspect_ratio = aspect_ratio
        self._auto_aspect = auto_aspect
        

    def preSrart(self):
        super().preSrart()
        if self._aspect_ratio is None:
            self._aspect_ratio = self.window.size.w / self.window.size.h
        self.projection.perspective(self._fov, self._aspect_ratio, self._near, self._far)
        if self._auto_aspect:
            self.window.size.onChange(self.autoAspectRatio)


    def reset(self, fov: float = None, near: float = None, far: float = None, aspect_ratio:float = None):
        if fov is not None:
            self._fov = fov
        if near is not None:
            self._near = near
        if far is not None:
            self._far = far
        if aspect_ratio is not None:
            self._aspect_ratio = aspect_ratio
        self.projection.perspective(self._fov, self._aspect_ratio, self._near, self._far)

    def autoAspectRatio(self, w, h):
        self._aspect_ratio = w / h
        self.projection.perspective(self._fov, self._aspect_ratio, self._near, self._far)
