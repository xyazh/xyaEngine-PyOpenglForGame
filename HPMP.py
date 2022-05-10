from numpy import size
from View import *
class HPMP(View):
    def __init__(self, game):
        super().__init__(game)
        self.player = game.entityPlayer
        self.gameLoop = game.gameLoop
        self.boxX = 0
        self.boxY = 0
        self.hpX = 0
        self.hpY = 0
        self.mpX = 0
        self.mpY = 0
        
    def render(self):
        hp = 1-self.player.HP/self.player.maxHP
        mp = 1-self.player.MP/self.player.maxMP
        self.gameLoop.renderImgFromName("HP.png",self.boxX-368-462*hp,self.boxY,size=2)
        self.gameLoop.renderImgFromName("MP.png",self.boxX-368-462*mp,self.boxY,size=2)

        self.gameLoop.renderImgFromName("HPMP.png",self.boxX-350,self.boxY,size=2)