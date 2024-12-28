from OpenGL.GL import *
from .RenderBuffer import *
from .FrameBuffer import FrameBuffer
from ..RenderGlobal import RenderGlobal



class FrameBufferMSAA(FrameBuffer):
    def __init__(self, width: int, height: int, use_depth=False, param:int = GL_NEAREST, samples=4):
        self.width = width
        self.height = height
        self.size = RenderGlobal.instance.window.size
        self.window_shader = RenderGlobal.instance.dis_shader_1
        self.use_depth = use_depth
        self.samples = samples  # 多重采样的数量，默认 4x
        # 创建帧缓冲对象
        self.framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        # 创建多重采样的颜色附件
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, self.texture_id)
        glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, self.samples, GL_RGBA, width, height, GL_TRUE)
        glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, 0)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D_MULTISAMPLE, self.texture_id, 0)
        if use_depth:
            glEnable(GL_DEPTH_TEST)  # 启用深度测试
            glEnable(GL_STENCIL_TEST)  # 启用模板测试
            # 创建多重采样的深度附件
            self.depth_texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, self.depth_texture_id)
            glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, self.samples, GL_DEPTH_COMPONENT24, width, height, GL_TRUE)
            glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, 0)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D_MULTISAMPLE, self.depth_texture_id, 0)
        # 检查帧缓冲是否完整
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer is not complete")
        # 解绑帧缓冲
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.render_buffer = RenderBuffer(GL_STATIC_DRAW)
        self.buf_builder = self.render_buffer.createBuffer(GL_TRIANGLES, POS | TEX)
        self.buf_builder.pos(-1, -1, 0).tex(0, 0).end()  # bottom left
        self.buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left
        self.buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(+1, +1, 0).tex(1, 1).end()    # top right
        self.buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left

        self.resolve()

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def resolve(self):
        # 创建一个普通的纹理来显示解析后的图像
        self.resolve_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.resolve_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        # 创建一个帧缓冲来解析多重采样结果
        self.resolve_fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.resolve_fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.resolve_texture, 0)
    
    def drawEnd(self):
        """将当前帧缓冲对象解绑"""
        self.unbind()
        glViewport(0, 0, self.size.w, self.size.h)
        # 从多重采样帧缓冲解析到普通帧缓冲
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.framebuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.resolve_fbo)
        glBlitFramebuffer(0, 0, self.width, self.height, 0, 0, self.width, self.height, GL_COLOR_BUFFER_BIT, GL_NEAREST)
        # 解绑
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

    def bindTexture(self):
        """绑定纹理对象"""
        glBindTexture(GL_TEXTURE_2D, self.resolve_texture)

