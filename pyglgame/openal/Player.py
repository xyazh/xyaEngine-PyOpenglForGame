import ctypes
from .Device import Device
from .AudioResource import AudioResource


class Player:
    AL_PLAYING = 0x1012
    AL_SOURCE_STATE = 0x1010
    AL_BUFFER = 0x1009
    AL_POSITION = 0x1004
    AL_LOOPING = 0x1007
    app_instance:"Player" = None

    def __init__(self, device: Device):
        self.device = device
        self.openal = device.openal
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

    def play(self, resource: AudioResource, loop: bool = False):
        src = self._createSource()
        buf_id = resource.buffer
        if isinstance(buf_id, ctypes.c_uint):
            buf_id = buf_id.value
        self.alSourcei(src, self.AL_BUFFER, buf_id)
        self.alSourcei(src, self.AL_LOOPING, 1 if loop else 0)
        self.alSourcePlay(src)
        return src


    def setPosition(self,src:int, x:float, y:float, z:float):
        self.alSource3f(src, self.AL_POSITION, x, y, z)

    def stopLoop(self, src: int):
        self.alSourcei(src, self.AL_LOOPING, 0)

    def setLoop(self, src: int, loop: bool):
        self.alSourcei(src, self.AL_LOOPING, 1 if loop else 0)

    def stop(self, src: int):
        #self.stopLoop(src)
        self.alSourceStop(src)
        self.alDeleteSources(1, ctypes.byref(ctypes.c_uint(src)))

    def isPlaying(self, src: int):
        return self.alGetSourcei(src, self.AL_SOURCE_STATE) == self.AL_PLAYING
