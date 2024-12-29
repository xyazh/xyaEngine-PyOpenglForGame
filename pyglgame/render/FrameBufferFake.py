from OpenGL.GL import *
from ..RenderGlobal import RenderGlobal
from .RenderBuffer import *
from .FrameBuffer import FrameBuffer


class FrameBufferFake:
    """用于在Camera中直接渲染到屏幕，以提升性能"""
    def __init__(self, width: int, height: int, use_depth=False,param:int = GL_NEAREST):
        self.width = width
        self.height = height
        self.size = RenderGlobal.instance.window.size
        self.window_shader = RenderGlobal.instance.dis_shader_1
        self.use_depth = use_depth
        self.param = param
       

    def __del__(self):
        self.cleanup()

    def bindTexture(self):
        """绑定纹理对象"""
        pass

    def bindDepthTexture(self):
        """绑定深度纹理对象"""
        pass

    def bind(self):
        """绑定帧缓冲对象"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def unbind(self):
        """解绑帧缓冲对象"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def drawStart(self):
        """将当前帧缓冲对象绑定为渲染目标，并绘制到纹理"""
        self.bind()
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        if self.use_depth:
            glEnable(GL_DEPTH_TEST)  # 启用深度测试
            glEnable(GL_STENCIL_TEST)  # 启用模板测试

    def draw(self, fuc, *args, **kw):
        """将当前帧缓冲对象绑定为渲染目标，并绘制到纹理"""
        self.drawStart()
        fuc(*args, **kw)
        self.drawEnd()

    def drawEnd(self):
        """将当前帧缓冲对象解绑"""
        self.unbind()


    def cleanup(self):
        """清理帧缓冲对象及其资源"""
        pass

    def drawToWindow(self):
        """将当前帧缓冲对象绘制到窗口"""
        pass
