from Assbmly import *
from Entity import *
from EntityPlayer import EntityPlayer
from ImageLoader import *
from KaBe import *
from Maps import *
from Map import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Que import *
from Event import *
from MPParticle import *
from HPMP import *
import threading


class Game():
    def __init__(self,gameLoop)->None:
        self.gameLoop = gameLoop
        self.gameLoop.asLoader.addImageAssbmlysFormPath("./data/o/test")
        self.camera = [0,0]
        self.maps = Maps()
        self.mapLoad()
        self.map = self.maps.getMapFromName("map")
        self.entityPlayer = EntityPlayer(self)

        self.events = Que()
        self.event = Event()

        self.particles = {}
        self.deadedParticles = set()
        self.particleTime = 0
        self.a = set()

        self.views = []
        self.view()
        def p_t(x):
            while True:
                print(len(x.particles),len(self.a),x.gameLoop._dTime)
                time.sleep(1)
        t = threading.Thread(target=p_t, name='LoopThread',args=(self,))
        t.start()



    def run(self)->None:
        self.particleTime += self.gameLoop._dTime
        if self.particleTime > 0.1:
            p = MPParticle(self)
            p.setPos(random.randint(int(self.entityPlayer.x)-self.gameLoop.window.x2disSizeX,int(self.entityPlayer.x)+self.gameLoop.window.x3disSizeX),random.randint(-self.map.h*2,0))
            self.createParticle(p)
            self.particleTime = 0


        
        for i in self.events:
            i()
        for i in self.map.kabes:
            i.forCamera()
        self.map.forCamera()
        self.entityPlayer.forCamera()

        self.map.renderSKY()
        self.map.renderBG()
        self.entityPlayer.updata()
        self.entityPlayer.render()
        
        self.a.clear()
        for i in self.particles:
            self.particles[i].forCamera()
            self.particles[i].render()
            self.particles[i].updata()
            if self.particles[i].isDead:
                self.deadedParticles.add(i)

            if self.particles[i].canLook:
                self.a.add(self.particles[i])

        for i in self.deadedParticles:
            self.particles.pop(i)
        self.deadedParticles.clear()

        
        self.map.renderMG()

        for i in self.views:
            i.render()
            i.updata()

    def getAss(self,name:str)->Assbmly:
        id = self.gameLoop.asLoader.getId(name)
        return self.gameLoop.asLoader.getAssbmly(id)

    def mapLoad(self):
        map1 = Map(self)
        map1.setBG("map.png")
        map1.setSKY("sky.png")
        kabe1 = KaBe(self)
        kabe1.setKaBe(-10000,-1040,1600000,5000)
        map1.kabes.append(kabe1)
        kabe2 = KaBe(self)
        kabe2.setKaBe(-1000,1000,990,5000)
        map1.kabes.append(kabe2)
        self.maps.addMap("map",map1)

    def view(self):
        self.views.append(HPMP(self))

    def createParticle(self,p:Particle):
        self.particles[id(p)] = p
