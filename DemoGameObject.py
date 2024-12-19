from pyglgame.GameObject import GameObject
from pyglgame.RenderBuffer import RenderBuffer
from pyglgame.Camera import Carmera
from pyglgame.BufferBuilder import *
from OpenGL.GL import *

class TestGameObject(GameObject):
    def start(self):
        self.render_buffer = RenderBuffer(GL_STREAM_DRAW)
        buf_builder = self.render_buffer.createBuffer(GL_QUADS, POS | COL)
        buf_builder.pos(0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(-0.5, 0.5, 0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, 0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(0.5, -0.5, 0.5).col(1, 1, 0, 1).end()
        # 后
        buf_builder.pos(0.5, 0.5, -0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(0.5, -0.5, -0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(-0.5, 0.5, -0.5).col(1, 1, 0, 1).end()
        # 左
        buf_builder.pos(-0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(-0.5, 0.5, -0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(-0.5, -0.5, 0.5).col(1, 1, 0, 1).end()
        # 右
        buf_builder.pos(0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(0.5, -0.5, 0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(0.5, 0.5, -0.5).col(1, 1, 0, 1).end()
        # 上
        buf_builder.pos(0.5, 0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(0.5, 0.5, -0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, 0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(-0.5, 0.5, 0.5).col(1, 1, 0, 1).end()
        # 下
        buf_builder.pos(0.5, -0.5, 0.5).col(1, 0, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, 0.5).col(0, 1, 0, 1).end()
        buf_builder.pos(-0.5, -0.5, -0.5).col(0, 0, 1, 1).end()
        buf_builder.pos(0.5, -0.5, -0.5).col(1, 1, 0, 1).end()
        self.camera = Carmera()
        self.camera.test()
        return super().start()
    
    def render(self, dt: float, fps: float):
        self.shader.use()
        self.camera.use()
        self.camera.rotate.rotate(0.5, (1,1,1))
        self.render_buffer.draw()
        self.shader.release()
        return super().render(dt, fps)