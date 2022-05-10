from KaBe import *
import math

class Entity:
    def __init__(self,game)->None:
        self.x:float = 0
        self.y:float = 0
        self.w = 0
        self.h = 0
        self.g = 0
        self.v = [0,0]
        self.a = [0,0]
        self.forCameraX = 0
        self.forCameraY = 0
        self.isDead = 0

        self.game = game
        self.gameLoop = game.gameLoop

    def cartesianCoordinateInCenter(self,x,y):
        cx,cy = self.x+self.w/2,self.y+self.h/2
        forCameraCx,forCameraCy = self.forCameraX+cx/2,self.forCameraY+cy/2
        return cx+x,cy+y,forCameraCx,forCameraCy

    def polarCoordinatesInCenter(self,r,l):
        x = l*math.cos(r)
        y = l*math.sin(r)
        return self.cartesianCoordinateInCenter(x,y)

    def render(self)->None:
        pass

    def forCamera(self)->None:
        self.forCameraX = self.x - self.game.camera[0]
        self.forCameraY = self.y - self.game.camera[1]

    def updata(self)->None:
        self.v[0] += self.a[0] * self.gameLoop._dTime
        self.v[1] += (self.a[1]+self.g) * self.gameLoop._dTime
