import random
from Entity import *

class Particle(Entity):
    def __init__(self,game)->None:
        super().__init__(game)
        self.livingTime = 0
        self.maxLivingTime = 10
        self.canLook = False
        self.isAway = False

        self._temp()

    def _temp(self):
        self.__d__ = 0

    def __eq__(self,other):
        if id(self)==id(other):
            return True
        else:
            return False

    def __hash__(self):
        return id(self)

    def render(self)->None:
        if not self.canLook:
            return
        if self.isDead:
            return
        if 0<self.livingTime<0.5:
            self.__d__ = self.livingTime
        else:
            self.__d__ = self.maxLivingTime - self.livingTime
            if not 0 < self.__d__ < 0.5:
                self.__d__ = 0.5
        self.__d__ *= 2
        self.gameLoop.renderImgFromName("pt2.png",self.forCameraX,self.forCameraY,size=0.48*self.__d__,isCenter=True)

    def updata(self)->None:
        super().updata()

        #统计时间
        self.livingTime += self.gameLoop._dTime
        #超时死亡
        if self.livingTime>self.maxLivingTime:
            self.isDead = True
        #出界死亡
        elif self.game.map.w != 0 and self.game.map.h != 0:
            if self.x>self.game.map.x2w or self.x<-self.game.map.x2w or self.y>self.game.map.x2h or self.y<-self.game.map.x2h:
                self.isDead = True
        #死亡停止
        if self.isDead:
            return

        #判断距离
        self.isAway = False
        if 0 < self.forCameraX < self.gameLoop.window.x2disSizeX and 0 > self.forCameraY > -self.gameLoop.window.x2disSizeY:
            self.canLook = True
        else:
            self.canLook = False
            if -self.gameLoop.window.disSizeX>self.forCameraX or self.forCameraX>self.gameLoop.window.x3disSizeX:
                self.isAway = True
            elif self.gameLoop.window.disSizeY < self.forCameraY or self.forCameraY < -self.gameLoop.window.x3disSizeY:
                self.isAway = True

        #超距停止
        if self.isAway:
            self.isDead = True
            return

        
        if self.gameLoop.n%10 == 0:
            self.a[0] = random.randint(-5,10)*5
            self.a[1] = random.randint(-10,10)*5

        self.x += self.v[0]*self.gameLoop._dTime
        self.y += self.v[1]*self.gameLoop._dTime

    def setPos(self,x,y):
        self.x = x
        self.y = y