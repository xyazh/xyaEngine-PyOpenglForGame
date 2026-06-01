
import cv2
import numpy as np
import mido
import random
import math
import cProfile
import glm
from line_profiler import profile
from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.render.BufferBuilder import *
from pyglgame.gameobject.camera.Camera import Camera
from pyglgame.render.MSAAFrameBuffer import MSAAFrameBuffer
from pyglgame.RenderGlobal import RenderGlobal
from OpenGL.GL import *
from pyglgame.KEYS import *
from pyglgame.gameobject.camera.m.MSimple2D import MSimple2D
from pyglgame.gameobject.camera.m.MPerspective import MPerspective
from pyglgame.BaseWindow import BaseWindow
from pyglgame.openal.AudioResource import AudioResource
from pyglgame.openal.Player import Player
from pyglgame.render.Image import Image
from pyglgame.ResourceLocation import ResourceLocation


WIN_W = int(1920)
WIN_H = int(1080)
LONG = 200
HLS = 1
# 视频参数
fps = 60
out_file = 'output.mp4'
global video_writer
video_writer = None



class Particle:
    alive_particles: list["Particle"] = []
    dead_particles: list["Particle"] = []

    def __new__(cls, x, y, z, color):
        if len(cls.dead_particles) > 0:
            obj = cls.dead_particles.pop()
        else:
            obj = super().__new__(cls)
        cls.alive_particles.append(obj)
        return obj

    def __init__(self, x, y, z, color):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.age = 0
        self.max_age = abs(random.gauss(0, 3))
        self.alive = True
        self.velocity_x = -random.uniform(0, 0.1)
        self.velocity_y = 0
        self.velocity_z = 0
        self.size = 30

    def update(self, dt, tps):
        self.age += dt
        if self.age > self.max_age:
            self.alive = False

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.z += self.velocity_z * dt
        self.velocity_x *= 0.999
        self.velocity_y *= 1.0
        self.velocity_z *= 1.0

    def render(self, dt, fps, buffer: "BufferBuilder"):
        if not self.alive:
            return
        buffer.pos(self.x, self.y, self.z).col(
            *self.color).siz(self.size*(self.max_age-self.age)/self.max_age).end()

    @classmethod
    def updates(cls, dt, tps):
        alive = []
        for p in cls.alive_particles:
            p.update(dt, tps)
            if p.alive:
                alive.append(p)
            else:
                cls.dead_particles.append(p)
        cls.alive_particles = alive


class Particle2:
    alive_particles: list["Particle2"] = []
    dead_particles: list["Particle2"] = []

    @staticmethod
    def build_basis(nx, ny, nz):
        # 任选一个不平行的向量
        if abs(nx) < 0.9:
            ax, ay, az = 1, 0, 0
        else:
            ax, ay, az = 0, 1, 0
        # U = N × A
        ux = ny * az - nz * ay
        uy = nz * ax - nx * az
        uz = nx * ay - ny * ax
        # 单位化 U
        length = math.sqrt(ux*ux + uy*uy + uz*uz)
        ux, uy, uz = ux/length, uy/length, uz/length
        # V = N × U
        vx = ny * uz - nz * uy
        vy = nz * ux - nx * uz
        vz = nx * uy - ny * ux

        return (ux, uy, uz), (vx, vy, vz)

    @staticmethod
    def emit_ring_particles(
        cx, cy, cz,           # 中心点
        nx, ny, nz,           # 法向量
        count,                # 粒子数量
        speed,
        color
    ):
        # 法向量单位化
        nl = math.sqrt(nx*nx + ny*ny + nz*nz)
        nx, ny, nz = nx/nl, ny/nl, nz/nl
        # 构造平面基
        (ux, uy, uz), (vx, vy, vz) = Particle2.build_basis(nx, ny, nz)
        for i in range(count):
            angle = 2.0 * math.pi * i / count
            # 圆周方向
            dx = math.cos(angle) * ux + math.sin(angle) * vx
            dy = math.cos(angle) * uy + math.sin(angle) * vy
            dz = math.cos(angle) * uz + math.sin(angle) * vz
            # 粒子初始位置（在圆上）
            p = Particle2(
                cx, cy, cz,
                color,
                dx, dy, dz,
                speed
            )

    def __new__(cls, x, y, z, color, dir_x, dir_y, dir_z, speed):
        if len(cls.dead_particles) > 0:
            obj = cls.dead_particles.pop()
        else:
            obj = super().__new__(cls)
        cls.alive_particles.append(obj)
        return obj

    def __init__(self, x, y, z, color, dir_x, dir_y, dir_z, speed):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.color = (color[0]*10, color[1]*10, color[2]*10)
        length = math.sqrt(dir_x*dir_x + dir_y*dir_y + dir_z*dir_z)
        if length == 0:
            length = 1.0
        self.velocity_x = dir_x / length * speed
        self.velocity_y = dir_y / length * speed
        self.velocity_z = dir_z / length * speed
        self.alive = True
        self.max_age = 1 + random.gauss(0, 0.5)
        self.age = 0
        self.size = 30

    def update(self, dt, tps):
        self.age += dt
        if self.age > self.max_age:
            self.alive = False
            return

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.z += self.velocity_z * dt
        self.velocity_x *= 0.99
        self.velocity_y *= 0.99
        self.velocity_z *= 0.99

    def render(self, dt, fps, buffer: "BufferBuilder"):
        if not self.alive:
            return
        buffer.pos(self.x, self.y, self.z).col(
            *self.color).siz(self.size*(self.max_age-self.age)/self.max_age).end()

    @classmethod
    def updates(cls, dt, tps):
        alive = []
        for p in cls.alive_particles:
            p.update(dt, tps)
            if p.alive:
                alive.append(p)
            else:
                cls.dead_particles.append(p)
        cls.alive_particles = alive


class Note:
    def __init__(self, pitch, velocity, start, duration, seed):
        self.speed = 16
        # 这里的 start 和 duration 已经是秒
        self.pitch = pitch
        self.velocity = velocity/127
        self.start = start * self.speed + 12  # 延迟3秒进入画面
        self.duration = duration * self.speed
        self.flag = False

        l = 2 * self.velocity
        self.colors = (
            (math.sin((start+seed)/5+51)/2+1) * l,
            (math.sin((start+seed)/7+71)/2+1) * l,
            (math.sin((start+seed)/11+91)/2+1) * l,
            1.0
        )
        self.z = (random.random()-0.5)/100
        self.color = self.colors
        self.played = False  # 防止重复播放
        freq = 440 * math.pow(2, (self.pitch - 69) / 12.0)
        self.audio = self.noteAudio(
            freq, self.duration / self.speed, self.velocity)

    def noteAudio(self, frequency, duration, volume, sample_rate=44100):
        return AudioResource.generateNaturalSine(frequency, duration, volume, sample_rate, channels=1)

    def play(self):
        Player.app_instance.play(self.audio)

    def update(self, dt, tps):
        self.start -= dt * self.speed
        if not self.played and self.start <= -2:
            self.played = True
            self.play()

    def render(self, dt, fps, buffer: "BufferBuilder", offset, lines):
        pitch = self.pitch - offset
        start = self.start
        duration = self.duration
        x1 = start - 1
        x2 = (duration + start) - 1
        y1 = pitch * 2 / lines - 1
        y2 = y1 + 2 / lines
        x1 /= 3
        x2 /= 3
        if x2 < -1 or x1 > 1 + LONG:
            return
        a1 = 1
        a2 = 0
        r, g, b, _ = self.colors
        if x1 < -1:
            a1 = (x2+1)/(x2-x1)
            x1 = -1
            r *= 3
            g *= 3
            b *= 3

        self.color = (r, g, b)
        y1 *= HLS
        y2 *= HLS
        z = self.z
        buffer.pos(x1, y1, z).col(r, g, b, a1).end()
        buffer.pos(x1, y2, z).col(r, g, b, a1).end()
        buffer.pos(x2, y2, z).col(r, g, b, a2).end()
        buffer.pos(x1, y1, z).col(r, g, b, a1).end()
        buffer.pos(x2, y2, z).col(r, g, b, a2).end()
        buffer.pos(x2, y1, z).col(r, g, b, a2).end()
        if x1 > -1:
            return
        """if random.random() < 0.5:
            Particle2(x1, random.uniform(y1, y2), 0, self.colors)"""
        l = 2
        Particle(x1, random.uniform(y1, y2), z, (r*l, g*l, b*l))
        if not self.flag:
            self.flag = True
            Particle2.emit_ring_particles(
                x1, (y1+y2)/2, 0,
                1, 0, 0,
                100, 0.2 + self.duration/100, self.colors)


class MidiNoteReader:
    def __init__(self, file_path: str):
        self.mid = mido.MidiFile(file_path)
        merged = mido.merge_tracks(self.mid.tracks)
        self.ticks_per_beat = self.mid.ticks_per_beat
        self.tempo = 50
        self.notes: list[Note] = []
        self.max_pitch = 0
        self.min_pitch = 127
        self.all_second = 0
        self._parseNotes()

    def _parseNotes(self):
        notes = []
        note_on_dict = {}
        current_second = 0.0
        seed = random.randint(0, 1000000)

        for msg in self.mid:

            d_second = msg.time
            current_second += d_second

            if msg.type == 'set_tempo':
                continue

            if msg.type == 'note_on' and msg.velocity > 0:
                note_on_dict[msg.note] = (current_second, msg.velocity)

            elif msg.type in ('note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in note_on_dict:
                    start_second, velocity = note_on_dict.pop(msg.note)
                    duration_second = current_second - start_second
                    duration_second = max(duration_second, 0.05)

                    notes.append(
                        (msg.note, velocity, start_second, duration_second, seed)
                    )

                    self.max_pitch = max(self.max_pitch, msg.note)
                    self.min_pitch = min(self.min_pitch, msg.note)
                    self.all_second = max(self.all_second, current_second)
        self.notes = []
        for pitch, velocity, start, duration, seed in notes:
            self.notes.append(Note(pitch, velocity, start, duration, seed))

    def getNotes(self):
        return self.notes


class TestObject(GameObject):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.midi = MidiNoteReader(
            r"c:\Users\33023\Desktop\4\TextAsset\Secret_God_Matara_Phantasm.mid")

    def start(self):
        glDisable(GL_CULL_FACE)
        glLineWidth(1)
        self.render_buffer_notes = RenderBuffer()
        self.render_particles = RenderBuffer()
        self.light_strip = RenderBuffer()
        Player.app_instance.play(AudioResource.fromWav(r"D:\NEW\gal\【豪華版】神様ちゅ～ず！\特典\期間限定追加特典 OPテーマ\神様の言う通り.wav"))
        self.star_tex = Image(ResourceLocation(
            r"c:\Users\33023\Desktop\112.png")).getTexture()
        self.render_buffer_line = RenderBuffer(GL_STATIC_DRAW)
        buffer_line = self.render_buffer_line.createBuffer(GL_LINES, POS | COL)
        LIGHT_STRIP_COLOR = [2, 2, 2]
        buffer_line.pos(-1, +HLS, 0).col(*LIGHT_STRIP_COLOR).end()
        buffer_line.pos(-1, -HLS, 0).col(*LIGHT_STRIP_COLOR).end()
        lines = self.midi.max_pitch - self.midi.min_pitch + 1
        for i in range(lines + 1):
            if i % 12 == 0:
                a = 0.2
            elif i % 4 == 0:
                a = 0.2
            else:
                continue
            buffer_line.pos(-5, (-1 + (2 / lines) * i)*HLS,
                            0).col(0.9, 0.9, 0.9, a).end()
            buffer_line.pos(+1 + LONG, (-1 + (2 / lines) * i)*HLS,
                            0).col(0.9, 0.9, 0.9, -0.1).end()
        self.render_buffer_line.build()
        self.render_buffer_line.buffer_builder.buffer.clear()

        self.bg = RenderBuffer(GL_STATIC_DRAW)
        bg_builder = self.bg.createBuffer(
            GL_TRIANGLES, POS | TEX | COL)
        c = (0.2, 0.2, 0.2)
        bg_builder.pos(-1, -1, 0).col(*c).tex(0, 1).end()  # bottom left
        bg_builder.pos(+1, -1, 0).col(*c).tex(1, 1).end()  # bottom right
        bg_builder.pos(-1, +1, 0).col(*c).tex(0, 0).end()  # top left
        bg_builder.pos(+1, -1, 0).col(*c).tex(1, 1).end()  # bottom right
        bg_builder.pos(+1, +1, 0).col(*c).tex(1, 0).end()  # top right
        bg_builder.pos(-1, +1, 0).col(*c).tex(0, 0).end()  # top left

    def renderLine(self, dt, fps):
        self.render_buffer_line.draw(re_build=False)

    def renderBackground(self, dt, fps):
        glDisable(GL_DEPTH_TEST)
        render = self.bg
        self.star_tex.bind()
        RenderGlobal.instance.using_shader.uniform1i("fuc", 1)
        render.draw(re_build=False)
        RenderGlobal.instance.using_shader.uniform1i("fuc", 0)
        glEnable(GL_DEPTH_TEST)

    def renderNotes(self, dt, fps):
        buffer_notes = self.render_buffer_notes.createBuffer(
            GL_TRIANGLES, POS | COL)

        lines = self.midi.max_pitch - self.midi.min_pitch + 1
        for note in self.midi.getNotes():
            note.render(dt, fps, buffer_notes,
                        self.midi.min_pitch, lines)
            note.update(dt, fps)
        self.render_buffer_notes.draw()

    def renderParticle(self, dt, fps):
        buffer_star = self.render_particles.createBuffer(
            GL_POINTS, POS | COL | SIZ)
        for p in Particle.alive_particles:
            p.render(dt, fps, buffer_star)

        for p in Particle2.alive_particles:
            p.render(dt, fps, buffer_star)
        self.render_particles.draw()

    def render(self, dt, fps):
        print(fps)
        self.renderBackground(dt, fps)
        self.renderNotes(dt, fps)
        self.renderLine(dt, fps)
        self.renderParticle(dt, fps)
        Particle.updates(dt, fps)
        Particle2.updates(dt, fps)
        return super().render(dt, fps)

    def update(self, dt, tps):
        """Particle.updates(dt, tps)
        Particle2.updates(dt, tps)"""


class TestCamera(Camera):
    def __new__(cls, msaa_val: int = 0):
        return super().__new__(cls, msaa_val)

    def createFrameBuffer(self):
        self.frame_buffer = MSAAFrameBuffer(
            WIN_W, WIN_H, use_depth=True, param=GL_LINEAR, samples=32)

    def __init__(self, msaa_val: int = 0):
        super().__init__(msaa_val)
        self.last_mouse = None
        self.forward = glm.vec3(1, 0, 0.02)
        self.right = None
        self.x = -7.85
        self.y = 0
        self.z = 2.70
        self.p = 0
        self.t = 93.27
        self.r = 0

    def renderStart(self):
        if self.m is not None:
            self.forward = self.m.setCameraPosAndPYR(
                self.x, self.y, self.z, self.p, self.t, self.r)
            self.right = glm.cross(self.forward, glm.vec3(0.0, 1.0, 0.0))
            self.m.setCameraUniforms()
        self.frame_buffer.drawStart()


    def renderEnd(self):
        self.frame_buffer.drawEnd()
        self.bloomed_texture = self.bloom.bloom()
        tex = self.bloomed_texture
        width = self.bloom.w
        height = self.bloom.h
        # 创建 numpy 数组存储 RGBA8 数据
        data = np.zeros((height, width, 4), dtype=np.uint8)
        # 使用 DSA 直接读取纹理
        glGetTextureImage(tex.id, 0, GL_RGBA, GL_UNSIGNED_BYTE, data.nbytes, data)
        img = np.frombuffer(data, dtype=np.uint8).reshape(height, width, 4)
        img = np.flipud(img)  # OpenGL 的 y 轴向下，需要翻转
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        img = cv2.bilateralFilter(img, d=5, sigmaColor=75, sigmaSpace=75)
        global video_writer
        if video_writer is None:
            video_writer = cv2.VideoWriter(
                out_file,
                cv2.VideoWriter_fourcc(*'avc1'),
                fps,
                (width, height),
                params=[cv2.VIDEOWRITER_PROP_QUALITY, 100]  # 最大质量
            )
        video_writer.write(img)

    def update(self, dt, tps):
        if self.forward is None or self.right is None:
            return super().update(dt, tps)

        # print(self.x, self.y, self.z,self.p, self.t, self.r)

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
    video_writer.release()

BaseWindow.onClose = onClose


"""def onClose(self):
    video_writer.release()


BaseWindow.onClose = onClose"""

app = App()
app.window.setWindownSize((WIN_W, WIN_H))

test_object = TestObject()
camera = TestCamera(msaa_val=16)
m = MSimple2D()
m = MPerspective()
m.setPerspective(fov=22.5, aspect=WIN_W/WIN_H)
camera.setProjection(m)
camera.switch()
camera.useBloom(level1=4, level2=8)
app.start()
