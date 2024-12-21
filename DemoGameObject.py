import random
from pyglgame.GameObject import GameObject
from pyglgame.RenderBuffer import RenderBuffer
from pyglgame.Camera import Carmera
from pyglgame.BufferBuilder import *
from OpenGL.GL import *
from DemoBlock import DemoBlock, SIZE_X, SIZE_Y, SIZE_Z


class TestGameObject(GameObject):
    def __init__(self):
        super().__init__()
        bloch_height_map = [
            [random.randint(0, SIZE_Y-1) for _2 in range(SIZE_Z)] for _1 in range(SIZE_X)]
        for x in range(SIZE_X):
            for z in range(SIZE_Z):
                for y in range(SIZE_Y):
                    """if bloch_height_map[x][z] > y:
                        DemoBlock(x, y, z)"""
                    if random.randint(0, 100) > 90:
                        DemoBlock(x, y, z)

    def start(self):
        self.render_buffer = RenderBuffer(GL_STREAM_DRAW)
        buf_builder = self.render_buffer.createBuffer(GL_POINTS, POS | COL)
        for block in DemoBlock.all_blocks:
            block.addSurface(buf_builder)
        self.camera = Carmera()
        self.camera.test()
        self.dz = 0
        #self.camera.rotate.rotate(90, (-1, 0, 0))
        return super().start()

    def render(self, dt: float, fps: float):
        self.shader.use()
        self.camera.use()
        
        self.camera.position(SIZE_X/2, SIZE_Y/2, self.dz*2)
        self.dz += dt
        self.render_buffer.draw(False)
        self.shader.release()
        return super().render(dt, fps)
