from OpenGL.GL import *
from ..RenderGlobal import RenderGlobal
from .RenderBuffer import *


class MSAAFrameBuffer:
    def __init__(self, width: int, height: int, use_depth=False, param: int = GL_NEAREST,
                 data: list = None, samples: int = 0):
        self.width = width
        self.height = height
        self.size = RenderGlobal.instance.window.size
        self.use_depth = use_depth
        self.samples = samples
        self.is_dead = False

        self.framebuffer = 0
        self.texture_id = 0
        self.depth_texture_id = 0
        self.resolve_fbo = 0
        self.resolve_texture = 0

        # 多重采样处理
        if samples > 0:
            # 创建多重采样帧缓冲
            self.framebuffer = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

            # 创建多重采样颜色缓冲
            self.texture_id = glGenTextures(1)
            if samples > 1:
                glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, self.texture_id)
                glTexImage2DMultisample(
                    GL_TEXTURE_2D_MULTISAMPLE, samples, GL_RGBA32F, width, height, GL_TRUE
                )
                glFramebufferTexture2D(
                    GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                    GL_TEXTURE_2D_MULTISAMPLE, self.texture_id, 0
                )
            else:
                glBindTexture(GL_TEXTURE_2D, self.texture_id)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height,
                             0, GL_RGBA, GL_FLOAT, data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, param)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, param)
                glFramebufferTexture2D(
                    GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                    GL_TEXTURE_2D, self.texture_id, 0
                )

            # 创建多重采样深度/模板缓冲
            if use_depth:
                glEnable(GL_DEPTH_TEST)
                glEnable(GL_STENCIL_TEST)
                self.depth_texture_id = glGenRenderbuffers(1)
                glBindRenderbuffer(GL_RENDERBUFFER, self.depth_texture_id)
                if samples > 1:
                    glRenderbufferStorageMultisample(
                        GL_RENDERBUFFER, samples,
                        GL_DEPTH24_STENCIL8, width, height
                    )
                else:
                    glRenderbufferStorage(
                        GL_RENDERBUFFER,
                        GL_DEPTH24_STENCIL8, width, height
                    )
                glFramebufferRenderbuffer(
                    GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT,
                    GL_RENDERBUFFER, self.depth_texture_id
                )
        else:
            # 创建普通帧缓冲
            self.framebuffer = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

            # 创建颜色纹理附件
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height,
                         0, GL_RGBA, GL_FLOAT, data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, param)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, param)
            glFramebufferTexture2D(
                GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D, self.texture_id, 0
            )

            if use_depth:
                glEnable(GL_DEPTH_TEST)
                glEnable(GL_STENCIL_TEST)
                # 创建深度纹理附件
                self.depth_texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.depth_texture_id)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT24,
                             width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glFramebufferTexture2D(
                    GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                    GL_TEXTURE_2D, self.depth_texture_id, 0
                )

        # 检查帧缓冲完整性
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer is not complete")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 创建解析缓冲（用于多重采样）
        if samples > 1:
            self.resolve_fbo = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, self.resolve_fbo)

            self.resolve_texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.resolve_texture)
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA32F,
                width, height, 0, GL_RGBA, GL_FLOAT, None
            )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, param)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, param)
            glFramebufferTexture2D(
                GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                GL_TEXTURE_2D, self.resolve_texture, 0
            )

            if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
                raise RuntimeError("Resolve Framebuffer is not complete")

            glBindFramebuffer(GL_FRAMEBUFFER, 0)
        else:
            self.resolve_fbo = 0
            self.resolve_texture = 0

        self.render_buffer = RenderBuffer(GL_STATIC_DRAW)
        self.buf_builder = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | TEX)
        self.buf_builder.pos(-1, -1, 0).tex(0, 0).end()  # bottom left
        self.buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left
        self.buf_builder.pos(+1, -1, 0).tex(1, 0).end()   # bottom right
        self.buf_builder.pos(+1, +1, 0).tex(1, 1).end()    # top right
        self.buf_builder.pos(-1, +1, 0).tex(0, 1).end()   # top left

    def __del__(self):
        self.cleanup()

    def bindTexture(self):
        """绑定纹理对象"""
        if self.samples > 1:
            glBindTexture(GL_TEXTURE_2D, self.resolve_texture)
        else:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def unBindTexture():
        glBindTexture(GL_TEXTURE_2D, 0)

    def bindDepthTexture(self):
        """绑定深度纹理对象"""
        if self.samples > 1:
            glBindRenderbuffer(GL_RENDERBUFFER, self.depth_texture_id)
        else:
            glBindTexture(GL_TEXTURE_2D, self.depth_texture_id)

    def bind(self):
        """绑定帧缓冲对象"""
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

    def unbind(self):
        """解绑帧缓冲对象"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def drawStart(self):
        """将当前帧缓冲对象绑定为渲染目标，并绘制到纹理"""
        self.bind()
        glViewport(0, 0, self.width, self.height)
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT |
                GL_STENCIL_BUFFER_BIT)
        if self.use_depth:
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_STENCIL_TEST)

    def draw(self, fuc, *args, **kw):
        """将当前帧缓冲对象绑定为渲染目标，并绘制到纹理"""
        self.drawStart()
        fuc(*args, **kw)
        self.drawEnd()

    def drawEnd(self):
        """将当前帧缓冲对象解绑"""
        # 多重采样解析
        if self.samples > 1:
            glBindFramebuffer(GL_READ_FRAMEBUFFER, self.framebuffer)
            glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.resolve_fbo)
            glBlitFramebuffer(
                0, 0, self.width, self.height,
                0, 0, self.width, self.height,
                GL_COLOR_BUFFER_BIT, GL_NEAREST
            )
        self.unbind()
        glViewport(0, 0, self.size.w, self.size.h)

    def cleanup(self):
        """清理帧缓冲对象及其资源"""
        if self.is_dead:
            return
        self.is_dead = True
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        if self.framebuffer != 0:
            glDeleteFramebuffers(1, [self.framebuffer])
        if self.texture_id != 0:
            glDeleteTextures(1, [self.texture_id])
        if self.depth_texture_id != 0:
            glDeleteTextures(1, [self.depth_texture_id])
        if self.resolve_fbo != 0:
            glDeleteFramebuffers(1, [self.resolve_fbo])
        if self.resolve_texture != 0:
            glDeleteTextures(1, [self.resolve_texture])

    def drawToWindow(self):
        """将当前帧缓冲对象绘制到窗口"""
        if self.is_dead:
            return
        self.bindTexture()
        RenderGlobal.instance.using_shader.uniform1i("fuc", 1)
        self.render_buffer.draw(False)
