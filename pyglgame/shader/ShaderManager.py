import logging
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from io import BytesIO
from .Shader import Shader
from ..ResourceLocation import ResourceLocation
from ..xyazhServer.ConsoleMessage import ConsoleMessage


class ShaderManager:
    @staticmethod
    def loadShader(file: str):
        vertex_shader: int = 0
        fragment_shader: int = 0
        program: int = 0
        try:
            program = glCreateProgram()
            vertex_shader = glCreateShader(GL_VERTEX_SHADER)
            vertex_shader_source = ShaderManager.readFile(f"{file}.vert")
            glShaderSource(vertex_shader, vertex_shader_source)
            glCompileShader(vertex_shader)
            if glGetShaderiv(vertex_shader, GL_COMPILE_STATUS) == GL_FALSE:
                ConsoleMessage.printError(
                    str(glGetShaderInfoLog(vertex_shader), encoding="utf8"))
                raise RuntimeError(f"Error compiling vertex shader: {file}")

            fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
            fragment_shader_source = ShaderManager.readFile(f"{file}.frag")
            glShaderSource(fragment_shader, fragment_shader_source)
            glCompileShader(fragment_shader)
            if glGetShaderiv(fragment_shader, GL_COMPILE_STATUS) == GL_FALSE:
                ConsoleMessage.printError(
                    str(glGetShaderInfoLog(fragment_shader), encoding="utf8"))
                raise RuntimeError(f"Error compiling fragment shader: {file}")

            glAttachShader(program, vertex_shader)
            glAttachShader(program, fragment_shader)

            glLinkProgram(program)
            if glGetProgramiv(program, GL_LINK_STATUS) == GL_FALSE:
                ConsoleMessage.printError(
                    str(glGetProgramInfoLog(program), encoding="utf8"))
                raise RuntimeError(f"Error linking shader program: {file}")

            glDeleteShader(vertex_shader)
            glDeleteShader(fragment_shader)
            return Shader(program)

        except Exception as e:
            if vertex_shader:
                glDeleteShader(vertex_shader)
            if fragment_shader:
                glDeleteShader(fragment_shader)
            ConsoleMessage.printError(f"Failed to load shader: {file}")
            logging.exception(e)
            return Shader(0)

    @staticmethod
    def readFile(file):
        return ResourceLocation(file).toBytes()

    @staticmethod
    def loadComputeShader(file: str) -> Shader:
        compute_shader: int = 0
        program: int = 0
        try:
            program = glCreateProgram()
            compute_shader = glCreateShader(GL_COMPUTE_SHADER)
            compute_shader_source = ShaderManager.readFile(f"{file}.comp")
            glShaderSource(compute_shader, compute_shader_source)
            glCompileShader(compute_shader)

            if glGetShaderiv(compute_shader, GL_COMPILE_STATUS) == GL_FALSE:
                ConsoleMessage.printError(
                    str(glGetShaderInfoLog(compute_shader), encoding="utf8"))
                raise RuntimeError(f"Error compiling compute shader: {file}")

            glAttachShader(program, compute_shader)
            glLinkProgram(program)
            if glGetProgramiv(program, GL_LINK_STATUS) == GL_FALSE:
                ConsoleMessage.printError(
                    str(glGetProgramInfoLog(program), encoding="utf8"))
                raise RuntimeError(f"Error linking compute shader program: {file}")

            glDeleteShader(compute_shader)
            return Shader(program)

        except Exception as e:
            if compute_shader:
                glDeleteShader(compute_shader)
            ConsoleMessage.printError(f"Failed to load compute shader: {file}")
            logging.exception(e)
            return Shader(0)
    
