from typing import TYPE_CHECKING
import glm
from dataclasses import dataclass
from .MBase import MBase
from ....RenderGlobal import RenderGlobal
if TYPE_CHECKING:
    from ....shader.Shader import Shader


class MSimple2D(MBase):
    def __init__(self):
        # === Projection ===
        self._projection = glm.mat4(1.0)

        # === View ===
        self._view = glm.mat4(1.0)

    # === Uniform Helper ===
    def setCameraUniforms(self, shader: "Shader" = None):
        if shader == None:
            shader = RenderGlobal.instance.using_shader
        shader.uniformMatrix4fv("projection", self._projection)
        shader.uniformMatrix4fv("view", self._view)

    def setCameraPosAndPYR(self, x: float, y: float, z: float, pitch: float, yaw: float, roll: float = 0.0) -> glm.vec3:
        return
