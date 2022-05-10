class View:
    def __init__(self,game):
        self.forCameraX = 0
        self.forCameraY = 0
        self.game = game

    def setPos(self,x,y):
        self.forCameraX = x
        self.forCameraY = y

    def render(self):
        pass

    def updata(self):
        pass