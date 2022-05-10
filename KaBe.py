class KaBe:
    def __init__(self,game)->None:
        self.x = 0
        self.w = 0
        self.y = 0
        self.h = 0
        self.center = [0,0]
        self.forCameraX = 0
        self.forCameraY = 0
        self.game = game

    def setKaBe(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center[0] = x + self.w/2
        self.center[1] = y + self.h/2
        return self

    def forCamera(self)->None:
        self.forCameraX = self.x - self.game.camera[0]
        self.forCameraY = self.y - self.game.camera[1]