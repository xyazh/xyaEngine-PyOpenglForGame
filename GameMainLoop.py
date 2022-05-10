from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from AssbmlyLoader import *
from ImageLoader import *
from Assbmly import *
from Txs import *
from Game import *
import math


class GameMainLoop:
    def __init__(self, window)->None:
        #FPS = 100
        self.loopTime = 1

        self.window = window

        self._time = 0
        self._dTime = self.loopTime/1000
        self._runingTime = 0


        self.asLoader = AssbmlysLoader()
        self.texture = Txs(self.asLoader)

        self.game = Game(self)
        self.n = 0

        self.rlistID = glGenLists(1000)

    
    def renderListBegin(self):
        glNewList(self.rlistID,GL_COMPILE)
        return self.rlistID

    def renderListEnd(self,id):
        glEndList()
        glCallList(id)

    def timeLoopFPS(self)->None:
        glutTimerFunc(self.loopTime, self.main, 1)

    def run(self)->None:
        self.timeLoopFPS()
        self._time = time.time()

    def main(self, id:int)->None:
        beginTime = time.time()
        if self.window.stop:
            self._dTime = 0
            self.window.stop = False
        self.gameRun()

        self._dTime = time.time() - beginTime
        if self._dTime <= self.loopTime/1000:
            self._dTime = self.loopTime/1000
        self._runingTime += self._dTime

        self.timeLoopFPS()

    def set_2d(self):
        # 2d模式
        width, height = self.window.disSizeX,self.window.disSizeY
        glDisable(GL_DEPTH_TEST)
        viewport = [self.window.disSizeX,self.window.disSizeY]
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        # 3d模式
        width, height = self.window.disSizeX,self.window.disSizeY
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)


    def drawPlane(self, x: float, y:float,h:float,w:float)->None:
        glBegin(GL_TRIANGLE_STRIP)
        #右上角点
        glTexCoord2f(1.0, 1.0)
        #x,z,y
        glVertex3f(x+w,y,-1.0)
        #左上角点x
        glTexCoord2f(0.0, 1.0)
        #x,z,y
        glVertex3f(x,  y,-1.0,)
        #右下角点
        glTexCoord2f(1.0, 0.0)
        #x,z,y
        glVertex3f(x+w, y-h, -1.0)
        #左下角点
        glTexCoord2f(0.0, 0.0)
        #x,z,y
        glVertex3f(x, y-h, -1.0)
        glEnd()

    def drawPlaneR(self, x: float, y:float,h:float,w:float,r)->None:
        glBegin(GL_TRIANGLE_STRIP)
        #右上角点
        glTexCoord2f(1.0, 1.0)
        #x,z,y
        glVertex3f(x+w,y,-1.0)
        #左上角点x
        glTexCoord2f(0.0, 1.0)
        #x,z,y
        glVertex3f(x,  y,-1.0,)
        #右下角点
        glTexCoord2f(1.0, 0.0)
        #x,z,y
        glVertex3f(x+w, y-h, -1.0)
        #左下角点
        glTexCoord2f(0.0, 0.0)
        #x,z,y
        glVertex3f(x, y-h, -1.0)
        glEnd()

    def renderImgFromNameR(self,name:str, x:float,y:float,r:float):
        texId = self.texture.getIdFromName(name)
        texSize = self.texture.getSizeFromName(name)
        w = texSize.w
        h = texSize.h
        dl = self.window.disSizeX/self.window.disSizeY
        #self.renderR(texId, x/self.window.disSizeX-1, y/self.window.disSizeY+1, 16/(self.window.disSizeX*math.cos(r)+self.window.disSizeY*math.sin(r))*5,16/(self.window.disSizeX*math.sin(r)+self.window.disSizeY*math.cos(r))*5,r)
        self.renderR(texId, x/self.window.disSizeX-1, y/self.window.disSizeY+1, 0.5,0.5,r)


    def renderR(self,texId: int,x:float,y:float,w:float,h:float,r:float)->None:
        glLoadIdentity()
        glTranslatef(x, y, 0)
        glRotatef(r,0.0 ,0.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, texId)
        self.drawPlaneR(0.0,0.0,h, w,r)

    def render(self,texId: int,x:float,y:float,w:float,h:float)->None:
        #x = x-w/2
        glLoadIdentity()
        #glPushMatrix()
        glTranslatef(x, y, 0)
        glBindTexture(GL_TEXTURE_2D, texId)
        self.drawPlane(0.0, 1.0, h, w)
        #glPopMatrix()


    def renderImgFromName(self,name:str, x:float,y:float,sizeW:float=None,sizeH:float=None,size:float=1.0,type:int=0,isCenter:bool=False)->tuple[2]:
        texId = self.texture.getIdFromName(name)
        texSize = self.texture.getSizeFromName(name)
        w = texSize.w
        h = texSize.h
        if sizeW == None:
            sizeW = size
        if sizeH == None:
            sizeH = size

        if isCenter:
            x = x-w*sizeW/2
        #尺寸跟随窗口变化
        if type == 0:
            self.render(texId, x/self.window.disSizeX-1, y/self.window.disSizeY, w/self.window.disSizeX*sizeW,h/self.window.disSizeY*sizeH)
        #尺寸不跟随窗口变化
        elif type == 1:
            self.render(texId, x/self.window.sizeX-1, y/self.window.sizeY, w/self.window.sizeX*sizeW,h/self.window.sizeY*sizeH)
        #宽占满屏幕
        elif type == 2:
            h = h*self.window.disSizeX/w
            self.render(texId, x/self.window.disSizeX-1, y/self.window.disSizeY, 2*sizeW,h/self.window.disSizeY*sizeH*2)
            w = self.window.disSizeX
        #高占满屏幕
        elif type == 3:
            w = w*self.window.disSizeY/h
            self.render(texId, x/self.window.disSizeX-1, y/self.window.disSizeY, w/self.window.disSizeX*sizeW*2,2*sizeH)
            h = self.window.disSizeY
        return (w*sizeW,h*sizeH)
        

    def renderVideoFromName(self,name:str, x:float,y:float,sizeW:float=None,sizeH:float=None,size:float=1.0,fps:int=28)->None:
        id = self.asLoader.getId(name)
        ass = self.asLoader.getAssbmly(id)
        if sizeW == None:
            sizeW = size
        if sizeH == None:
            sizeH = size
        if not ass.data.isEnd:
            ass.data.play()
            if ass.data.startTime >= 1/fps:
                ass.data.startTime = ass.data.startTime-1/fps
                b,f = ass.data.getNextFrameImg()
                if b:
                    if ass.data.inTxId != None:
                        glDeleteTextures(1,int(ass.data.inTxId))
                    ass.data.inTxId = f.toTex()
                else:
                    ass.data.isEnd = True
            ass.data.startTime += self._dTime
        if ass.data.inTxId != None:
            self.render(ass.data.inTxId, x/self.window.sizeX-1, y/self.window.sizeY, 1440/self.window.sizeX*sizeW,1080/self.window.sizeY*sizeH)

    def load(self)->None:
        self.game.run()

    def gameRun(self)->None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1.0)
        self.load()
        glutSwapBuffers()
        self.n += 1