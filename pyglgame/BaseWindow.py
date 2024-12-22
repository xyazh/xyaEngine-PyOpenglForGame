import sys
import keyboard
from typing import TYPE_CHECKING
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .GameMainLoop import GameMainLoop
from .Size import Size
from .RenderGlobal import RenderGlobal

if TYPE_CHECKING:
    from .App import App


class BaseWindow:
    def __init__(self, app: "App", title: str, size: tuple[float], position: tuple[float], full_screen: bool) -> None:
        self.setWindownSize(size)
        self.app = app
        self.render_global = RenderGlobal(app, self)
        self.pos_x, self.pos_y = position
        self.full_screen: bool = full_screen
        self.title: str = title
        self.game_loop = GameMainLoop()


    def setWindownSize(self, size: tuple[float]) -> None:
        self.size = Size(*size)

    def setFullScreen(self) -> None:
        self.full_screen = True

    def run(self) -> None:
        glutInit(sys.argv)
        glutInitWindowPosition(self.pos_x, self.pos_y)
        glutInitWindowSize(self.size.w, self.size.h)
        glutCreateWindow(self.title)
        if self.full_screen:
            glutFullScreen()
        glutMouseFunc(self._mouseHit)
        glutMotionFunc(self._onMouseMove)
        glutPassiveMotionFunc(self._mouseMove)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA |
                            GLUT_DEPTH | GLUT_STENCIL)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glDepthMask(GL_TRUE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glutDisplayFunc(self.displayFunc)
        keyboard.hook(self._keyHook)
        self.render_global.start()
        self.game_loop.start()
        self.game_loop.run()
        glutMainLoop()

    def displayFunc(self) -> None:
        self.size_x = glutGet(GLUT_WINDOW_WIDTH)
        self.size_y = glutGet(GLUT_WINDOW_HEIGHT)
        self.size.updateSize(self.size_x, self.size_y)

    def _keyDown(self, key):
        pass

    def _keyUp(self, key):
        pass

    def _keyHook(self, t: keyboard.KeyboardEvent):
        pass

    def getKey(self, key) -> bool:
        return False

    def getKeyDown(self, key) -> bool:
        return False

    def _mouseHit(self, button, state, x, y):
        print(button, state, x, y)

    def getMouse(self) -> tuple:
        return (0, 0)

    def getOnMouse(self) -> tuple:
        return (0, 0)

    def getMiddleClickMouse(self) -> tuple | None:
        return None

    def getRightClickMouse(self) -> tuple | None:
        return None

    def getLeftClickMouse(self) -> tuple | None:
        return None

    def getLeftOnMouse(self) -> tuple | None:
        return None

    def getMiddleOnMouse(self) -> tuple | None:
        return None

    def getRightOnMouse(self) -> tuple | None:
        return None

    def _onMouseMove(self, x, y):
        pass

    def _mouseMove(self, x, y):
        pass
