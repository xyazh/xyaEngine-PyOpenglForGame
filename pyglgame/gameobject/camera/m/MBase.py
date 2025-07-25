from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....shader.Shader import Shader


class MBase:
    def setCameraUniforms(self, shader: "Shader" = None):
        raise NotImplementedError("Method setCameraUniforms not implemented")
    
    def setCameraPosAndPYR(self, x: float, y: float, z: float, pitch: float, yaw: float, roll: float = 0.0):
        raise NotImplementedError("Method setCameraPosAndPYR not implemented")
