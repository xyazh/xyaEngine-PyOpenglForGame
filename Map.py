class Map:
    def __init__(self,game)->None:
        self.x = 0
        self.y = 0
        self.forCameraX = 0
        self.forCameraY = 0
        self.game = game
        self.gameLoop = game.gameLoop
        self.w = 0
        self.h = 0
        self.x2w = 0
        self.x2h = 0
        self.skyW = 0
        self.skyH = 0

        self.kabes = []

        self.bg = None
        self.sky = None

    def forCamera(self)->None:
        self.forCameraX = self.x - self.game.camera[0]
        self.forCameraY = self.y - self.game.camera[1]

    def renderSKY(self)->None:
        if self.sky != None:
            i = 1
            if self.w != 0 :
                i = self.w
            self.skyW,self.skyH = self.gameLoop.renderImgFromName(self.sky,(self.skyW-self.gameLoop.window.disSizeX)/i*self.forCameraX,0,type=3)

    def renderBG(self)->None:
        if self.bg != None:
            self.w,self.h = self.gameLoop.renderImgFromName(self.bg,self.forCameraX,self.forCameraY,type=3)
            self.x2w,self.x2h = self.w*2,self.h*2

    def renderMG(self)->None:
        pass

    def setBG(self,name:str)->None:
        self.bg = name

    def setSKY(self,name:str)->None:
        self.sky = name