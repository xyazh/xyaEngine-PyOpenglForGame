from Entity import *


class EntityLiving(Entity):
    def __init__(self,game):
        super().__init__(game)
        self.g = -30000
        self.v = [0,0]
        self.a = [0,0]
        self.forCameraX = 0
        self.forCameraY = 0
        self.canJump = False

        self.HP = 1
        self.maxHP = 1

    def updata(self)->None:
        super().updata()

        if self.HP<=0:
            self.isDead = True
            self.HP = 0
        else:
            self.isDead = False

        if self.HP > self.maxHP:
            self.HP = self.maxHP

        if self.v[0] != 0 or self.a[0] != 0:
            self.x += 1
            if self.checkAABB():
                self.x-=1
                self.a[0] = 0
                self.v[0] = 0
            else:
                self.x-=1
                dx = self.v[0]*self.gameLoop._dTime
                self.x += dx
                if self.checkAABB():
                    self.x -= dx
                    self.v[0] = 0
                    self.a[0] = 0

        if self.v[1] != 0 or self.a[1] != 0 or self.g != 0:
            self.y += 1
            if self.checkAABB():
                self.y -= 1
                self.a[1] = 0
                self.v[1] = 0
            else:
                self.y-=1
                dy = self.v[1]*self.gameLoop._dTime
                self.y += dy
                if self.checkAABB():
                    self.y -= dy
                    self.v[1] = 0
                    self.a[1] = 0

    def checkAABB(self)->bool:
        flag = False
        self.canJump = False
        for i in self.game.map.kabes:
            if i.x < self.x < i.x+i.w and i.y - i.h < self.y < i.y:
                flag = True
            if i.x < self.x + self.w < i.x+i.w and i.y - i.h < self.y < i.y:
                flag = True
            elif i.x < self.x < i.x+i.w and i.y - i.h < self.y - self.h < i.y:
                flag = True
                self.canJump = True
            elif i.x < self.x + self.w < i.x+i.w and i.y - i.h < self.y - self.h < i.y:
                flag = True
                self.canJump = True
        return flag

    def kage(self):
        for i in self.game.map.kabes:
            flag = 0
            if i.x < self.x < i.x+i.w and i.y - i.h < self.y - self.h-500 < i.y:
                flag = i.y
            if i.x < self.x + self.w < i.x+i.w and i.y - i.h < self.y - self.h-500 < i.y:
                flag = i.y
        return flag