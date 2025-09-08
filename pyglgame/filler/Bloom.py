from ..shader.ShaderManager import ShaderManager
from ..render.TextureStorage2D import TextureStorage2D
from ..render.TextureBase import TextureBase
from ..RenderGlobal import RenderGlobal
from OpenGL.GL import *


class Bloom:
    def __init__(self, w: int, h: int):
        self.compute_shader = ShaderManager.loadComputeShader(
            "./res/shader/computeBloom")
        self.w = w
        self.h = h
        self.pingpong_tex1 = TextureStorage2D(int(w/2), int(h/2), unit=1)
        self.pingpong_tex2 = TextureStorage2D(int(w/2), int(h/2), unit=2)
        self.down_sample_tex1 = TextureStorage2D(int(w/4), int(h/4), unit=3)
        self.down_sample_tex2 = TextureStorage2D(int(w/4), int(h/4), unit=4)
        self.out_tex = TextureStorage2D(int(w), int(h), unit=5)

    def sefTexture(self, texture: TextureBase | int) -> None:
        if isinstance(texture, TextureBase):
            texture = texture.id

        glBindTexture(GL_TEXTURE_2D, texture)
        glBindImageTexture(0, texture, 0, GL_FALSE, 0,
                           GL_READ_ONLY, GL_RGBA32F)

    def bloom(self) -> TextureStorage2D:
        self.dis_shader = RenderGlobal.instance.using_shader

        
        # 2. 运行 compute shader
        self.compute_shader.use()
        # 下采样
        self.compute_shader.uniform1i("mode", 0)
        self.compute_shader.dispatch(
            self.down_sample_tex1.group_x, self.down_sample_tex1.group_y, 1)
        self.compute_shader.memoryBarrier()
        for _ in range(10):
            # 高斯
            self.compute_shader.uniform1i("mode", 4)
            self.compute_shader.dispatch(
                self.down_sample_tex2.group_x, self.down_sample_tex2.group_y, 1)
            self.compute_shader.memoryBarrier()
            # 高斯
            self.compute_shader.uniform1i("mode", 5)
            self.compute_shader.dispatch(
                self.down_sample_tex1.group_x, self.down_sample_tex1.group_y, 1)
            self.compute_shader.memoryBarrier()

        # 上采样
        self.compute_shader.uniform1i("mode", 1)
        self.compute_shader.dispatch(
            self.pingpong_tex1.group_x, self.pingpong_tex1.group_y, 1)
        self.compute_shader.memoryBarrier()
        for _ in range(10):
            # 高斯
            self.compute_shader.uniform1i("mode", 2)
            self.compute_shader.dispatch(
                self.pingpong_tex2.group_x, self.pingpong_tex2.group_y, 1)
            self.compute_shader.memoryBarrier()
            # 高斯
            self.compute_shader.uniform1i("mode", 3)
            self.compute_shader.dispatch(
                self.pingpong_tex1.group_x, self.pingpong_tex1.group_y, 1)
            self.compute_shader.memoryBarrier()
        self.compute_shader.uniform1i("mode", 6)
        self.compute_shader.dispatch(
            self.out_tex.group_x, self.out_tex.group_y, 1)
        self.compute_shader.memoryBarrier()
        # 3. 加载用于显示的 shader
        self.dis_shader.use()
        return self.out_tex
