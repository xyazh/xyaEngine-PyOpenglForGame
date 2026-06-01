from ...ResourceLocation import ResourceLocation
from ...render.Image import Image
from ...render.RenderBuffer import RenderBuffer
from ...render.BufferBuilder import *
from .AnimationBase import AnimationBase
from OpenGL.GL import *


class AnimationFrame(AnimationBase):
    def __init__(self, rows: int, columns: int, frame_count: int,
                 resourceLocation: ResourceLocation,
                 time: float = -1,
                 scale: tuple[float, float] = (1, 1),
                 vertical_first: bool = False):
        super().__init__(resourceLocation)
        image = Image(resourceLocation)
        self.rows = rows
        self.columns = columns
        self.vertical_first = vertical_first
        self.width = image.width // columns
        self.height = image.height // rows
        self.s_columns = 1.0 / columns
        self.s_rows = 1.0 / rows
        self.frame_count = min(frame_count, rows * columns)
        self.texture = image.getTexture()
        self.render_buffer = RenderBuffer()
        self.max_time = float(self.frame_count) if time <= 0 else time
        self.time = 0.0
        self.l = -self.width / 2 * scale[0]
        self.r = self.width / 2 * scale[0]
        self.t = self.height / 2 * scale[1]
        self.b = -self.height / 2 * scale[1]
        self.x = 0
        self.y = 0
        self.z = 0
        self.flip_x = False
        self.flip_y = False

    def setFlipX(self, flip: bool):
        self.flip_x = flip

    def setFlipY(self, flip: bool):
        self.flip_y = flip

    def render(self, dt: float, fps: float):
        super().render(dt, fps)

        self.time %= self.max_time

        frame_time = self.max_time / self.frame_count
        index = int(self.time / frame_time) % self.frame_count

        if self.vertical_first:
            row = index % self.rows
            col = index // self.rows
        else:
            col = index % self.columns
            row = index // self.columns

        tpos_x = col * self.s_columns
        tpos_y = row * self.s_rows

        u0 = tpos_x
        u1 = tpos_x + self.s_columns
        v0 = tpos_y
        v1 = tpos_y + self.s_rows

        if self.flip_x:
            u0, u1 = u1, u0

        if self.flip_y:
            v0, v1 = v1, v0

        self.texture.bind()

        buf_builder = self.render_buffer.createBuffer(GL_TRIANGLES, POS | COL | TEX)

        buf_builder.pos(self.l + self.x, self.b + self.y, self.z).col(1, 1, 1, 1).tex(u0, v1).end()
        buf_builder.pos(self.r + self.x, self.b + self.y, self.z).col(1, 1, 1, 1).tex(u1, v1).end()
        buf_builder.pos(self.l + self.x, self.t + self.y, self.z).col(1, 1, 1, 1).tex(u0, v0).end()

        buf_builder.pos(self.r + self.x, self.b + self.y, self.z).col(1, 1, 1, 1).tex(u1, v1).end()
        buf_builder.pos(self.r + self.x, self.t + self.y, self.z).col(1, 1, 1, 1).tex(u1, v0).end()
        buf_builder.pos(self.l + self.x, self.t + self.y, self.z).col(1, 1, 1, 1).tex(u0, v0).end()

        self.render_buffer.draw()

        self.time += dt