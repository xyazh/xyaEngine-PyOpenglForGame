from Particle import *
import math

class MPParticle(Particle):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.maxLivingTime = 5
        self._temp()

    def _temp(self):
        super()._temp()
        self.__px__ = 0
        self.__py__ = 0
        self.__dx__ = 0
        self.__dy__ = 0

    def updata(self):
        super().updata()

        #不可见停止
        if not self.canLook:
            return

        self.__px__ = self.game.entityPlayer.x
        self.__py__ = self.game.entityPlayer.y - self.game.entityPlayer.h/2
        self.__dx__ = self.x - self.__px__
        self.__dy__ = self.y - self.__py__
        l = math.sqrt(math.pow(self.__dx__,2)+math.pow(self.__dy__,2))
        if l<300:
            self.x -= self.__dx__/20
            self.y -= self.__dy__/20
            if l<40:
                self.game.entityPlayer.MP += 1
                self.isDead = True