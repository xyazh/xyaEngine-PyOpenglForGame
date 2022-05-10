from EntityLiving import *
from Particle import *

class EntityPlayer(EntityLiving):
    def __init__(self,game):
        super().__init__(game)
        self.isLeft = False
        self.w = 138
        self.h = 264

        self.maxHP = 100
        self.HP = 100
        self.maxMP = 100
        self.MP = 0
        self.r = 0

    def updata(self):
        if self.MP > self.maxMP:
            self.MP = self.maxMP
        if self.MP < 0:
            self.MP = 0
        self.bindCamera()
        self.bindKey()
        super().updata()

    def render(self)->None:
        n = 0
        if self.v[0] != 0:
            i = self.gameLoop._runingTime%0.25
            if i<0.125:
                n = 1
            else:
                n = 2
        a = 3
        if self.isLeft:
            a = 0
        self.gameLoop.renderImgFromName("image%d.png"%(a+n),self.forCameraX,self.forCameraY-50,size=6,isCenter=True)

        l = 1000
        x,y,cax,cay = self.polarCoordinatesInCenter(self.r,l)
        self.r = 45
        self.gameLoop.renderImgFromNameR("test2.png",960,-540,self.r)
        self.r = -90
        self.gameLoop.renderImgFromNameR("test2.png",960,-540,self.r)

    def bindCamera(self):
        if self.x >= self.gameLoop.window.disSizeX and self.x+self.gameLoop.window.disSizeX<=self.game.map.w*2:
            self.game.camera[0] = self.x-self.gameLoop.window.disSizeX

    def bindKey(self):
        if self.gameLoop.window.keyIn("left"):
            self.v[0]=-1000
            self.isLeft = True
        elif self.gameLoop.window.keyIn("right"):
            self.v[0]=1000
            self.isLeft = False
        else:
            self.v[0]=0
        if self.canJump and self.gameLoop.window.keyIn("space"):
            self.v[1] = 3000

        if self.gameLoop.window.keyIn("1"):
            for i in range(5000):
                p = Particle(self.game)
                p.setPos(800,-500)
                self.game.createParticle(p)