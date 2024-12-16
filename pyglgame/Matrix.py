import glm
from .Vec3 import Vec3

class Matrix:
    def __init__(self):
        # 初始化为单位矩阵
        self.mat = glm.mat4(1.0)

    def translate(self, x, y, z):
        """应用平移变换"""
        translation = glm.translate(glm.mat4(1.0), glm.vec3(x, y, z))
        self.mat = translation * self.mat  # 更新模型矩阵
        return self

    def scale(self, x, y, z):
        """应用缩放变换"""
        scaling = glm.scale(glm.mat4(1.0), glm.vec3(x, y, z))
        self.mat = scaling * self.mat  # 更新模型矩阵
        return self

    def rotate(self, angle, axis):
        """应用旋转变换"""
        axis = glm.vec3(*axis)  # 创建旋转轴向量
        rotation = glm.rotate(glm.mat4(1.0), glm.radians(angle), axis)
        self.mat = rotation * self.mat  # 更新模型矩阵
        return self
    
    def perspective(self, fov, aspect_ratio, near, far):
        """应用透视投影变换"""
        projection = glm.perspective(glm.radians(fov), aspect_ratio, near, far)
        self.mat = projection
        return self
    
    def lookAt(self, eye:Vec3, center:Vec3, up:Vec3):
        view = glm.lookAt(eye, center, up)
        self.mat = view
    
    def disLookAt(self,n):
        self.mat = glm.lookAt(glm.vec3(0,0,n), glm.vec3(0,0,n-1), glm.vec3(0,1,0))
    
    def valuePtr(self):
        return glm.value_ptr(self.mat)