
import mido
import random
import math
import cProfile
from pyglgame.App import App
from pyglgame.gameobject.GameObject import GameObject
from pyglgame.render.RenderBuffer import RenderBuffer
from pyglgame.render.BufferBuilder import *
from pyglgame.gameobject.camera.Camera import Camera
from pyglgame.render.MSAAFrameBuffer import MSAAFrameBuffer
from OpenGL.GL import *
from pyglgame.KEYS import *
from pyglgame.gameobject.camera.m.MSimple2D import MSimple2D
from pyglgame.BaseWindow import BaseWindow
from pyglgame.openal.AudioResource import AudioResource
from pyglgame.openal.Player import Player

WIN_W = 960
WIN_H = 540


class Note:
    def __init__(self, pitch, velocity, start, duration):
        # 这里的 start 和 duration 已经是秒
        self.pitch = pitch
        self.velocity = velocity * random.random()
        self.start = start + 3  # 延迟3秒进入画面
        self.duration = duration

        l = 1.5
        self.colors = (
            0x00/255*l,
            0xFF/255*l,
            0xD9/255*l,
            1.0
        )
        self.played = False  # 防止重复播放
        freq = 440 * math.pow(2, (self.pitch - 69) / 12.0)
        self.audio = self.noteAudio(freq, self.duration, 1)

    def noteAudio(self, frequency, duration, volume, sample_rate=44100):
        return AudioResource.generateSmoothSine(frequency, duration, volume, sample_rate, channels=1)

    def play(self):
        Player.app_instance.play(self.audio)

    def update(self, dt, tps):
        self.start -= dt
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
        if x2 < -1 or x1 > 1:
            return
        r, g, b, a = self.colors
        buffer.pos(x1, y1, 0).col(r, g, b, a).end()
        buffer.pos(x1, y2, 0).col(r, g, b, a).end()
        buffer.pos(x2, y2, 0).col(r, g, b, 0).end()
        buffer.pos(x1, y1, 0).col(r, g, b, a).end()
        buffer.pos(x2, y2, 0).col(r, g, b, 0).end()
        buffer.pos(x2, y1, 0).col(r, g, b, 0).end()


class MidiNoteReader:
    def __init__(self, file_path: str):
        self.mid = mido.MidiFile(file_path)
        self.ticks_per_beat = self.mid.ticks_per_beat
        print(self.mid.ticks_per_beat)
        self.tempo = 50
        self.notes: list[Note] = []
        self.max_pitch = 0
        self.min_pitch = 127
        self.all_ticks = 0
        self._parseNotes()

    def _parseNotes(self):
        notes = []
        note_on_dict = {}
        current_ticks = 0
        for msg in self.mid:
            current_ticks += msg.time
            if msg.type == 'set_tempo':
                self.tempo = msg.tempo
            if msg.type == 'note_on' and msg.velocity > 0:
                note_on_dict[msg.note] = (current_ticks, msg.velocity)
            elif msg.type in ('note_off', 'note_on') and msg.velocity == 0:
                if msg.note in note_on_dict:
                    start_ticks, velocity = note_on_dict.pop(msg.note)
                    duration_ticks = current_ticks - start_ticks
                    start_sec = mido.tick2second(
                        start_ticks, self.ticks_per_beat, self.tempo*1000)
                    duration_sec = mido.tick2second(
                        duration_ticks, self.ticks_per_beat, self.tempo*1000)
                    duration_sec = max(duration_sec, 0.05)
                    notes.append(
                        Note(msg.note, velocity, start_sec, duration_sec))
                    self.max_pitch = max(self.max_pitch, msg.note)
                    self.min_pitch = min(self.min_pitch, msg.note)
                    self.all_ticks = max(self.all_ticks, current_ticks)
        self.notes = notes

    def getNotes(self):
        return self.notes


class TestObject(GameObject):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.midi = MidiNoteReader(
            r"D:\baidunetdiskdownload\远枫\远枫.mid")

    def start(self):
        glDisable(GL_CULL_FACE)
        glLineWidth(1)
        self.render_buffer_notes = RenderBuffer()
        self.render_particles = RenderBuffer()
        #Player.app_instance.play(AudioResource.fromWav(r"D:\NEW\gal\【豪華版】神様ちゅ～ず！\特典\期間限定追加特典 OPテーマ\神様の言う通り.wav"))
        

        self.render_buffer_line = RenderBuffer(GL_STATIC_DRAW)
        buffer_line = self.render_buffer_line.createBuffer(GL_LINES, POS | COL)
        buffer_line.pos(-1, +1, 0).col(1, 1, 1, 1).end()
        buffer_line.pos(-1, -1, 0).col(1, 1, 1, 1).end()
        lines = self.midi.max_pitch - self.midi.min_pitch + 1
        for i in range(lines + 1):
            if i % 12 == 0:
                a = 0.7
            elif i % 4 == 0:
                a = 0.2
            else:
                continue
            buffer_line.pos(-1, -1 + (2 / lines) * i,
                            -0.5).col(0.9, 0.9, 0.9, a).end()
            buffer_line.pos(+1, -1 + (2 / lines) * i,
                            -0.5).col(0.9, 0.9, 0.9, a).end()
        self.render_buffer_line.build()
        self.render_buffer_line.buffer_builder.buffer.clear()

    def renderLine(self, dt, fps):
        self.render_buffer_line.draw(re_build=False)

    def renderNotes(self, dt, fps):
        buffer_notes = self.render_buffer_notes.createBuffer(
            GL_TRIANGLES, POS | COL)
        lines = self.midi.max_pitch - self.midi.min_pitch + 1
        for note in self.midi.getNotes():
            note.render(dt, fps, buffer_notes, self.midi.min_pitch, lines)
            note.update(dt, fps)
        self.render_buffer_notes.draw()

    def render(self, dt, fps):
        print(fps)
        self.renderNotes(dt, fps)
        self.renderLine(dt, fps)
        return super().render(dt, fps)

    def update(self, dt, tps):
        pass


class TestCamera(Camera):
    def __new__(cls, msaa_val: int = 0):
        return super().__new__(cls, msaa_val)

    def createFrameBuffer(self):
        self.frame_buffer = MSAAFrameBuffer(
            self.size.w, self.size.h, use_depth=True, param=GL_LINEAR, samples=self._msaa_val)

    def __init__(self, msaa_val: int = 0):
        super().__init__(msaa_val)

    def renderStart(self):
        self.m.setCameraUniforms()
        self.frame_buffer.drawStart()

    def update(self, dt, tps):
        pass


profiler = cProfile.Profile()
profiler.enable()  # 开始采样


def onClose(self):
    profiler.disable()  # 停止采样
    profiler.dump_stats("profile.prof")


BaseWindow.onClose = onClose
app = App()
app.window.setWindownSize((WIN_W, WIN_H))

test_object = TestObject()
camera = TestCamera()
m = MSimple2D()
camera.setProjection(m)
camera.switch()
camera.useBloom()
app.start()
