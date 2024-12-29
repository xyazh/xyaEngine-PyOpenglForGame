import numpy as np
from typing import TYPE_CHECKING, Generator
from pyglgame.render.BufferBuilder import *
from OpenGL.GL import *
if TYPE_CHECKING:
    from ...gameobject.GameObject import GameObject


class IClickable:
    def onHoverMouse(self, mos: tuple, color_data: np.ndarray, game_objects: "Generator[GameObject]") -> None:
        pass