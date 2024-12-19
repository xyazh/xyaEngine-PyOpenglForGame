import glm
from .Vec3 import Vec3

class Matrix:
    def __init__(self):
        # 初始化为单位矩阵
        self.mat = glm.mat4(1.0)

    def translate(self, x, y, z):
        """应用平移变换"""
        self.mat = glm.translate(self.mat, glm.vec3(x, y, z))
        return self

    def scale(self, x, y, z):
        """应用缩放变换"""
        self.mat = glm.scale(self.mat, glm.vec3(x, y, z))
        return self

    def rotate(self, angle:float, axis:tuple|list):
        """应用旋转变换"""
        axis = glm.vec3(*axis)  # 创建旋转轴向量
        self.mat = glm.rotate(self.mat, glm.radians(angle), axis)
        return self
    
    def perspective(self, fov, aspect_ratio, near, far):
        """应用透视投影变换"""
        self.mat = glm.perspective(glm.radians(fov), aspect_ratio, near, far)
        return self
    
    def lookAt(self, eye:Vec3, center:Vec3, up:Vec3):
        view = glm.lookAt(eye, center, up)
        self.mat = view
    
    def valuePtr(self):
        return glm.value_ptr(self.mat)