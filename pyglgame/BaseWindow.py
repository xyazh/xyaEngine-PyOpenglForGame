import sys
import keyboard
from typing import TYPE_CHECKING
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from .GameMainLoop import GameMainLoop
from .math.Size import Size
from .RenderGlobal import RenderGlobal

if TYPE_CHECKING:
    from .App import App


class BaseWindow:
    def __init__(self, app: "App", title: str, size: tuple[float], position: tuple[float], full_screen: bool) -> None:
        self.setWindownSize(size)
        self.app = app
        self.render_global = RenderGlobal(app=app, window=self)
        self.pos_x, self.pos_y = position
        self.full_screen: bool = full_screen
        self.title: str = title
        self.initMouse()
        self.key_set: set = set()
        self.key_down_set: set = set()
        self.game_loop = GameMainLoop()

    def setWindownSize(self, size: tuple[float]) -> None:
        self.size = Size(*size)

    def setFullScreen(self) -> None:
        self.full_screen = True

    def run(self) -> None:
        glutInit(sys.argv)
        glutInitWindowPosition(self.pos_x, self.pos_y)
        glutInitWindowSize(self.size.w, self.size.h)
        glutCreateWindow(self.title.encode())
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
        glEnable(GL_MULTISAMPLE)
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
        self.key_down_set.add(key)
        self.key_set.add(key)

    def _keyUp(self, key):
        if key in self.key_set:
            self.key_set.remove(key)

    def _keyHook(self, t: keyboard.KeyboardEvent):
        if t.event_type == "down":
            self._keyDown(t.name)
        else:
            self._keyUp(t.name)

    def clearKeyDown(self):
        self.key_down_set.clear()

    def getKey(self, key) -> bool:
        return key in self.key_set

    def getKeyDown(self, key) -> bool:
        return key in self.key_down_set

    def _mouseHit(self, button, state, x, y):
        self.on_mouse_x, self.on_mouse_y = x, y
        if button == 0:
            if state == 0:
                self.mouse_left_on_hit = True
                self.mouse_left_button_on = True
            else:
                self.mouse_left_button_on = False
            return
        if button == 1:
            if state == 0:
                self.mouse_middle_on_hit = True
                self.mouse_middle_button_on = True
            else:
                self.mouse_middle_button_on = False
            return
        if button == 2:
            if state == 0:
                self.mouse_right_on_hit = True
                self.mouse_right_button_on = True
            else:
                self.mouse_right_button_on = False
            return

    def _onMouseMove(self, x, y):
        self.on_mouse_x, self.on_mouse_y = x, y

    def _mouseMove(self, x, y):
        self.mouse_x, self.mouse_y = x, y

    def initMouse(self) -> None:
        self.mouse_left_button_on = False
        self.mouse_middle_button_on = False
        self.mouse_right_button_on = False
        self.mouse_left_on_hit = False
        self.mouse_middle_on_hit = False
        self.mouse_right_on_hit = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.on_mouse_x = 0
        self.on_mouse_y = 0

    def clearMouseHit(self):
        self.mouse_left_on_hit = False
        self.mouse_middle_on_hit = False
        self.mouse_right_on_hit = False

    def getMouse(self) -> tuple:
        return (self.mouse_x, self.mouse_y)

    def getOnMouse(self) -> tuple:
        return (self.on_mouse_x, self.on_mouse_y)

    def getMiddleClickMouse(self) -> tuple:
        if self.mouse_middle_on_hit:
            return (self.on_mouse_x, self.on_mouse_y)
        return None

    def getRightClickMouse(self) -> tuple:
        if self.mouse_right_on_hit:
            return (self.on_mouse_x, self.on_mouse_y)
        return None

    def getLeftClickMouse(self) -> tuple:
        if self.mouse_left_on_hit:
            return (self.on_mouse_x, self.on_mouse_y)
        return None

    def getLeftOnMouse(self) -> tuple:
        if self.mouse_left_button_on:
            return (self.on_mouse_x, self.on_mouse_y)
        return None

    def getMiddleOnMouse(self) -> tuple:
        if self.mouse_middle_button_on:
            return (self.on_mouse_x, self.on_mouse_y)
        return None

    def getRightOnMouse(self) -> tuple:
        if self.mouse_right_button_on:
            return (self.on_mouse_x, self.on_mouse_y)
        return None
