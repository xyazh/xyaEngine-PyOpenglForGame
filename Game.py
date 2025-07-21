from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.RenderGlobal import RenderGlobal
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *


class TestObject(GameObject):
    def __new__(cls):
        return super().__new__(cls)

    def render(self, dt, fps):
        render_buffer = RenderBuffer()
        buffer_builder = render_buffer.createBuffer(GL_TRIANGLES, POS | COL)
        buffer_builder.pos(0, 1, 0).col(1, 0, 0, 1).end()
        buffer_builder.pos(-1, -1, 0).col(0, 1, 0, 1).end()
        buffer_builder.pos(1, -1, 0).col(0, 0, 1, 1).end()
        RenderGlobal.instance.using_shader.uniform1i("fuc", 0)
        render_buffer.draw()
        return super().render(dt, fps)


app = App()
app.window.setWindownSize((960, 540))

test_object = TestObject()


app.start()
