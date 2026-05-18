import glm
import cProfile
from pyglgame.BaseWindow import BaseWindow
from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.RenderGlobal import RenderGlobal
from pyglgame.render.BufferBuilder import *
from pyglgame.gameobject.camera.Camera import Camera
from pyglgame.render.MSAAFrameBuffer import MSAAFrameBuffer
from pyglgame.gameobject.camera.m.MPerspective import MPerspective
from OpenGL.GL import *
from pyglgame.KEYS import *
from pyglgame.gameobject.camera.m.MOrthographic import MOrthographic

app = App()
app.window.setWindownSize((1920, 1080))

CHUNK_SIZE = 16
CHUNK_LOAD_RADIUS = 16

class Chunk:
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.changed = True
        self.blocks = [[[1 for _ in range(CHUNK_SIZE)] for _ in range(
            CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]

        self.render_buffer = RenderBuffer()
        self.build()

    def setBlock(self, x, y, z, block_type: int):
        self.blocks[x][y][z] = block_type
        self.changed = True

    def build(self):
        if not self.changed:
            return
        self.chunk_buffer = self.render_buffer.createBuffer(
            GL_TRIANGLES, POS | COL)
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    block_type = self.blocks[x][y][z]
                    if block_type == 0:
                        continue
                    self.renderCube(x, y, z)
        self.render_buffer.build()

    def getBlock(self, x, y, z):
        return self.blocks[x][y][z]

    def up(self, x, y, z):
        if y+1 >= CHUNK_SIZE:
            return 0
        return self.blocks[x][y+1][z]

    def down(self, x, y, z):
        if y-1 < 0:
            return 0
        return self.blocks[x][y-1][z]

    def right(self, x, y, z):
        if z+1 >= CHUNK_SIZE:
            return 0
        return self.blocks[x][y][z+1]

    def left(self, x, y, z):
        if z-1 < 0:
            return 0
        return self.blocks[x][y][z-1]

    def front(self, x, y, z):
        if x+1 >= CHUNK_SIZE:
            return 0
        return self.blocks[x+1][y][z]

    def back(self, x, y, z):
        if x-1 < 0:
            return 0
        return self.blocks[x-1][y][z]

    def renderCube(self, x, y, z):
        # 世界坐标偏移
        cx = self.x * CHUNK_SIZE + x
        cy = self.y * CHUNK_SIZE + y
        cz = self.z * CHUNK_SIZE + z
        # 顶点定义（x,y,z）
        vertices = [
            (-0.5, -0.5, -0.5),  # 0 后左下
            (+0.5, -0.5, -0.5),  # 1 后右下
            (+0.5, +0.5, -0.5),  # 2 后右上
            (-0.5, +0.5, -0.5),  # 3 后左上
            (-0.5, -0.5, +0.5),  # 4 前左下
            (+0.5, -0.5, +0.5),  # 5 前右下
            (+0.5, +0.5, +0.5),  # 6 前右上
            (-0.5, +0.5, +0.5),  # 7 前左上
        ]
        # 根据邻块剔除空面
        faces = []
        if self.up(x, y, z) == 0:
            faces.append((3, 2, 6, 7))
        if self.down(x, y, z) == 0:
            faces.append((0, 1, 5, 4))
        if self.left(x, y, z) == 0:
            faces.append((0, 1, 2, 3))
        if self.right(x, y, z) == 0:
            faces.append((4, 5, 6, 7))
        if self.front(x, y, z) == 0:
            faces.append((1, 5, 6, 2))
        if self.back(x, y, z) == 0:
            faces.append((0, 4, 7, 3))
        # 遍历要渲染的面
        for a, b, c, d in faces:
            # 每个面两个三角形
            self.chunk_buffer.pos(
                cx + vertices[a][0], cy + vertices[a][1], cz + vertices[a][2]).col(1, 1, 0, 1).end()
            self.chunk_buffer.pos(
                cx + vertices[b][0], cy + vertices[b][1], cz + vertices[b][2]).col(1, 0, 1, 1).end()
            self.chunk_buffer.pos(
                cx + vertices[c][0], cy + vertices[c][1], cz + vertices[c][2]).col(0, 1, 1, 1).end()
            self.chunk_buffer.pos(
                cx + vertices[a][0], cy + vertices[a][1], cz + vertices[a][2]).col(0, 0, 1, 1).end()
            self.chunk_buffer.pos(
                cx + vertices[c][0], cy + vertices[c][1], cz + vertices[c][2]).col(0, 1, 0, 1).end()
            self.chunk_buffer.pos(
                cx + vertices[d][0], cy + vertices[d][1], cz + vertices[d][2]).col(1, 0, 0, 1).end()

    def render(self, dt, fps):
        self.build()
        self.render_buffer.draw(re_build=self.changed)
        self.changed = False


class World(GameObject):

    def start(self):
        render_buffer = RenderBuffer()
        self.render_buffer = render_buffer
        self.cube_light = 2
        self.player: GameObject = None
        self.chunks: dict[tuple[int, int, int], Chunk] = {}
        glDisable(GL_CULL_FACE)

    def render(self, dt, fps):
        self.genChunk(dt, fps)
        for chunk in self.chunks.values():
            chunk.render(dt, fps)
        print(fps)
        return super().render(dt, fps)
    
    def genChunk(self, dt, fps):
        if self.player is None:
            return
        player_chunk_x = int(self.player.x // CHUNK_SIZE)
        player_chunk_y = int(self.player.y // CHUNK_SIZE)
        player_chunk_z = int(self.player.z // CHUNK_SIZE)
        to_remove = []
        count = 0
        for pos, chunk in self.chunks.items():
            dx = chunk.x - player_chunk_x
            dy = chunk.y - player_chunk_y
            dz = chunk.z - player_chunk_z
            if dx*dx + dz*dz > (CHUNK_LOAD_RADIUS*1.5)**2:
                to_remove.append(pos)
        for pos in to_remove:
            del self.chunks[pos]
        for dx in range(-CHUNK_LOAD_RADIUS, CHUNK_LOAD_RADIUS+1):
            for dz in range(-CHUNK_LOAD_RADIUS, CHUNK_LOAD_RADIUS+1):
                    cx = player_chunk_x + dx
                    cz = player_chunk_z + dz
                    if (cx, 0, cz) not in self.chunks:
                        self.chunks[(cx, 0, cz)] = Chunk(cx, 0, cz)
                        count += 1
                        if count > 1:
                            return
    
    def update(self, dt, tps):
        return super().update(dt, tps)
    
    def setPlayer(self, game_object: GameObject):
        self.player = game_object


class TestCamera(Camera):
    def __new__(cls, msaa_val: int = 4):
        return super().__new__(cls, msaa_val=8)

    def __init__(self, msaa_val: int = 4):
        super().__init__(msaa_val)
        self.last_mouse = None
        self.forward = None
        self.right = None
        self.world = World()

    def renderStart(self):
        if self.m is not None:
            self.forward = self.m.setCameraPosAndPYR(
                self.x, self.y, self.z, self.p, self.t, self.r)
            self.right = glm.cross(self.forward, glm.vec3(0.0, 1.0, 0.0))
            self.m.setCameraUniforms()
        self.frame_buffer.drawStart()
        self.world.setPlayer(self)

    def update(self, dt, tps):
        if self.forward is None or self.right is None:
            return super().update(dt, tps)
        move_x, move_y, move_z = 0, 0, 0

        window = self.render_global.window
        speed = 10 * dt
        if window.getKey("w") or window.getKey("W"):
            move_x += self.forward.x * speed
            move_y += self.forward.y * speed
            move_z += self.forward.z * speed
        if window.getKey("s") or window.getKey("S"):
            move_x -= self.forward.x * speed
            move_y -= self.forward.y * speed
            move_z -= self.forward.z * speed
        if window.getKey("d") or window.getKey("D"):
            move_x += self.right.x * speed
            move_z += self.right.z * speed
        if window.getKey("a") or window.getKey("A"):
            move_x -= self.right.x * speed
            move_z -= self.right.z * speed
        if window.getKey(KEY_SPACE):
            move_y += speed
        if window.getKey(KEY_SHIFT):
            move_y -= speed

        # 更新位置
        self.x += move_x
        self.y += move_y
        self.z += move_z

        # 鼠标控制旋转（保持不变）
        mouse = window.getOnMouse()
        if self.last_mouse is not None and window.mouse_left_button_on:
            self.t -= (mouse[0] - self.last_mouse[0]) * dt * 5
            self.p -= (mouse[1] - self.last_mouse[1]) * dt * 5
        self.last_mouse = mouse
        if not window.mouse_left_button_on:
            self.last_mouse = None
            return super().update(dt, tps)


profiler = cProfile.Profile()
profiler.enable()  # 开始采样
def onClose(self):
    profiler.disable()  # 停止采样
    profiler.dump_stats("profile.prof")

BaseWindow.onClose = onClose

camera = TestCamera()
m = MPerspective()
m.updateAspectFromSize(1920, 1080)
camera.setProjection(m)
camera.switch()
camera.useBloom()

app.start()
