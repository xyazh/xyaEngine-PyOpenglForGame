from ..ResourceLocation import ResourceLocation
from .AudioResource import AudioResource
from .Player import Player

class Audio:
    @classmethod
    def playAudio(cls, resource:ResourceLocation,play: bool = False, loop: bool = False):
        obj = cls(AudioResource.fromWav(resource))
        if play:
            obj.play(loop)
        return obj

    @property
    def player(self):
        if Player.app_instance is None:
            raise Exception("Too early, player instance is not initialized")
        return Player.app_instance

    def __init__(self, resource: AudioResource):
        self.resource = resource
        self.src:int = -1

    def play(self, loop: bool = False):
        if self.src > 0:
            self.stop()
        self.src = self.player.play(self.resource, loop)
    
    def stop(self):
        if self.src <= 0:
            return
        self.player.stop(self.src)
        self.src = -1

    def stopLoop(self):
        if self.src <= 0:
            return
        self.player.stopLoop(self.src)

    def setLoop(self, loop: bool):
        if self.src <= 0:
            return
        self.player.setLoop(self.src, loop)

    def setPosition(self, x: float, y: float, z: float):
        if self.src <= 0:
            return
        self.player.setPosition(self.src, x, y, z)

    def __delete__(self):
        self.stop()

    def __del__(self):
        self.stop()
    
