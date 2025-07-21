from .GameObject import GameObject
from ..render.FrameBuffer import FrameBuffer
from ..RenderGlobal import RenderGlobal


class Camera(GameObject):
    def __new__(cls):
        return super().__new__(cls, is_camera=True)

    def start(self):
        size = RenderGlobal.instance.window.size
        self.frame_buffer = FrameBuffer(size.w, size.w)

    def renderStart(self):
        self.frame_buffer.drawStart()

    def renderEnd(self):
        self.frame_buffer.drawEnd()

    def render(self, dt, fps):
        self.frame_buffer.drawToWindow()
