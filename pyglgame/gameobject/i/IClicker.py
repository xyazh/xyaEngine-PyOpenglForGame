import numpy as np
from typing import TYPE_CHECKING, Generator
from ...render.BufferBuilder import *
from OpenGL.GL import *
from ...math.Size import Size
from ...gameobject.i.IClickable import IClickable
if TYPE_CHECKING:
    from ...render.FrameBuffer import FrameBuffer
    from ...shader.Shader import Shader
    from ...BaseWindow import BaseWindow
    from ...gameobject.GameObject import GameObject


class IClicker:
    size: Size
    window: "BaseWindow"

    def __init_clicker__(self):
        self.clicker_frame_buffer = self.creatFrameBuffer()

    def hoverMouse(self, objects: "set[GameObject]") -> "tuple[tuple,np.ndarray,Generator[GameObject|IClickable]]":
        mos = self.window.getMouse()
        color_data = self.getPixelColor(*mos)
        game_objects = (
            game_object for game_object in objects
            if game_object.clickable and
            isinstance(game_object, IClickable) and
            game_object.isDataColor(*color_data)
        )
        return (mos, color_data, game_objects)

    def onHoverMouse(self, objects: "set[GameObject]") -> None:
        mos, color_data, game_objects = self.hoverMouse(objects)
        for game_object in game_objects:
            game_object.onHoverMouse(mos, color_data, game_objects)

    def renderClickerStart(self):
        self.clicker_frame_buffer.drawStart()

    def renderClickerEnd(self):
        self.clicker_frame_buffer.drawEnd()

    def setDataColorUniform(self, shader: "Shader", r: float, g: float, b: float, a: float):
        shader.uniform4f("data_color", r, g, b, a)

    def getPixelColor(self, x, y):
        x = int(x / self.size.w * self.clicker_frame_buffer.width)
        y = self.clicker_frame_buffer.height - \
            int(y / self.size.h * self.clicker_frame_buffer.height)
        self.clicker_frame_buffer.bind()
        color = np.zeros(4, dtype=np.float32)
        glReadPixels(x, y, 1, 1, GL_RGBA, GL_FLOAT, color)
        self.clicker_frame_buffer.unbind()
        return color

    def creatFrameBuffer(self) -> "FrameBuffer":
        raise NotImplementedError("creatFrameBuffer is not implemented")
