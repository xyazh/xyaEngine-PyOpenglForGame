import cv2
from PIL import Image
from ImageLoader import * 
import winsound,time

class VideoLoader:
    def __init__(self):
        self.path = ""
        self.video = None
        self.startTime = 0
        self.isEnd = False
        self.inTxId = None
        self.size = self.Size(960,720)
        self.audio = './data/a/1.wav'

    def loadfromPath(self,path:str):
        self.path = path


    def play(self): 
        if self.video == None:
            self.video = cv2.VideoCapture(self.path)
            self.auPlaying = winsound.PlaySound(self.audio,winsound.SND_ASYNC)
            time.sleep(1.5)

    def reset(self):
        self.video = None
        self.startTime = 0
        self.isEnd = False

    def risetto(self):
        print("[XX-XX-XX XX:XX:XX][XXXX]:ビデオ、リセット！")
        self.reset()

    def getNextFrameImg(self):
        success, frame = self.video.read()
        m = None
        if success:
            img=Image.fromarray(frame)
            m = self.MMImageLoader()
            m.loadfromImg(img)
        return success,m

    class Size:
        def __init__(self,w,h):
            self.w = w
            self.h = h
        
    class MMImageLoader(ImageLoader):
        def loadfromImg(self,img):
            self.image = img.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data = self.image.convert("RGBA").tobytes()

        def toTex(self):
            id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_BGRA, self.image.width, self.image.height, 0, GL_BGRA, GL_UNSIGNED_BYTE, self.img_data)
            return id
    