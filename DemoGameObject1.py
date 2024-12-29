from pyglgame.gameobject.GameObject import GameObject
from pyglgame.gameobject.i.IClickable import IClickable
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *


class DemoGameObject1(GameObject, IClickable):
    def __init__(self):
        super().__init__()
        self.clickable: bool = True
        self.data_color = (0, 0, 12, 1)

    def onHoverMouse(self, mos, color_data, game_objects):
        print("onHoverMouse")

    def start(self):
        self.render_buf = RenderBuffer(GL_STREAM_DRAW)
        buf = self.render_buf.createBuffer(GL_QUADS, POS | COL)
        buf.pos(-0.5, 0.5, 0).col(0.3, 0, 0, 1).end()
        buf.pos(0.5, 0.5, 0).col(0.3, 0, 0, 1).end()
        buf.pos(0.5, -0.5, 0).col(0.3, 0, 0, 1).end()
        buf.pos(-0.5, -0.5, 0).col(0.3, 0, 0, 1).end()

    def render(self, dt: float, fps: float):
        glDisable(GL_CULL_FACE)
        self.render_buf.draw(False)
        return super().render(dt, fps)
