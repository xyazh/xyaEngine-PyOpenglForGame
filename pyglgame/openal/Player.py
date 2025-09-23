import ctypes
from .Device import Device
from .AudioResource import AudioResource


class Player:
    AL_PLAYING = 0x1012
    AL_SOURCE_STATE = 0x1010
    AL_BUFFER = 0x1009
    AL_POSITION = 0x1004

    def __init__(self, device: Device):
        self.device = device
        self.openal = device.openal
        self.sources = []
        self._initSourceFuncs()

    def _initSourceFuncs(self):
        al = self.openal
        self.alSourcePlay = al.alSourcePlay
        self.alSourcePlay.argtypes = [ctypes.c_uint]

        self.alSourceStop = al.alSourceStop
        self.alSourceStop.argtypes = [ctypes.c_uint]

        self.alSourcei = al.alSourcei
        self.alSourcei.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int]

        self.alSource3f = al.alSource3f
        self.alSource3f.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_float, ctypes.c_float, ctypes.c_float]

        self.alGetSourcei = al.alGetSourcei
        self.alGetSourcei.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]

        self.alGenSources = al.alGenSources
        self.alGenSources.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
        self.alGenSources.restype = None

        self.alDeleteSources = al.alDeleteSources
        self.alDeleteSources.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
        self.alDeleteSources.restype = None

    def _createSource(self):
        src = ctypes.c_uint(0)
        self.alGenSources(1, ctypes.byref(src))
        return src.value

    def play(self, resource: AudioResource):
        src = self._createSource()
        self.sources.append(src)
        # 绑定缓冲区，确保类型是 ctypes.c_uint.value
        buf_id = resource.buffer
        if isinstance(buf_id, ctypes.c_uint):
            buf_id = buf_id.value
        self.alSourcei(src, self.AL_BUFFER, buf_id)
        self.alSourcePlay(src)


    def setPosition(self, x, y, z):
        for src in self.sources:
            self.alSource3f(src, self.AL_POSITION, x, y, z)

    def stop_all(self):
        for src in self.sources:
            self.alSourceStop(src)
            self.alDeleteSources(1, ctypes.byref(ctypes.c_uint(src)))
        self.sources.clear()

    def update(self):
        """清理已经播放完毕的 source"""
        alive = []
        for src in self.sources:
            state = ctypes.c_int(0)
            self.alGetSourcei(src, self.AL_SOURCE_STATE, ctypes.byref(state))
            if state.value == self.AL_PLAYING:
                alive.append(src)
            else:
                self.alDeleteSources(1, ctypes.byref(ctypes.c_uint(src)))
        self.sources = alive

    def cleanup(self):
        self.stop_all()

    def __del__(self):
        self.cleanup()
