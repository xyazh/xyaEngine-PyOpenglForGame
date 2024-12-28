import random
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *


class DemoGameObject1(GameObject):
    def __init__(self):
        super().__init__()
        self.clickable: bool = True
        self.data_color = (0, 0, 12, 1)



    def start(self):
        self.render_buf = RenderBuffer(GL_STREAM_DRAW)
        buf = self.render_buf.createBuffer(GL_QUADS, POS | COL)
        buf.pos(-0.5, 0.5, 0).col(0.3, 0, 0, 1).end()
        buf.pos(0.5, 0.5, 0).col(0.3, 0, 0, 1).end()
        buf.pos(0.5, -0.5, 0).col(0.3, 0, 0, 1).end()
        buf.pos(-0.5, -0.5, 0).col(0.3, 0, 0, 1).end()

    def render(self, dt: float, fps: float):
        self.render_buf.draw(False) 
        return super().render(dt, fps)
