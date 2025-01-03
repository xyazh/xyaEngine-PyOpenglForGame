import random
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.gameobject.i.IClickable import IClickable
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *
from DemoBlock import DemoBlock, SIZE_X, SIZE_Y, SIZE_Z


class DemoGameObject(GameObject,IClickable):
    def __init__(self):
        self.f = 0
        self.df = 0.001
        super().__init__()
        self.clickable: bool = True
        self.data_color = (0, 0, 12, 1)
        bloch_height_map = [
            [random.randint(0, SIZE_Y-1) for _2 in range(SIZE_Z)] for _1 in range(SIZE_X)]
        for x in range(SIZE_X):
            for z in range(SIZE_Z):
                for y in range(SIZE_Y):
                    DemoBlock(x, y, z)


    def getLayer(self):
        return 1

    def start(self):
        self.render_buffer = RenderBuffer(GL_STREAM_DRAW)
        buf_builder = self.render_buffer.createBuffer(
            GL_QUADS, POS | COL | SIZ)
        for block in DemoBlock.all_blocks:
            block.addSurface(buf_builder)
        self.render_global.translate(0, -3, -100)
        return super().start()

    def render(self, dt: float, fps: float):
        self.render_buffer.draw(False)
        return super().render(dt, fps)
