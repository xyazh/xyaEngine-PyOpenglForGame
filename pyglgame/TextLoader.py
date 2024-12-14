from PIL import ImageFont,ImageDraw,Image
from .ImageLoader import ImageLoader
class TextLoader:
    def __init__(self,game_main_loop, text:str=None, size:int = 10) -> None:
        self.path:str = None
        self.is_loaded = None
        self.color = "white"
        self.font_path:str='C:\\Windows\\Fonts\\simhai.ttf'
        self.size = 10
        self.game_main_loop = game_main_loop
        self.text = text
        if text:
            self.is_loaded = True
            self.craftFromText(text)
            self.setSize(size)
            self.setColor()
            self.setFont()

    def getText(self)->str:
        if self.is_loaded:
            return self.text
        self.is_loaded = True
        return self.openText()

    def openText(self)->str:
        with open(self.path,"r",encoding="utf8") as f:
            self.text = f.read()
        return self.text
    def craftFromPath(self,path)->None:
        self.path = path
        
    def craftFromText(self,text:str)->None:
        self.text = text

    def setSize(self,size:int)->None:
        self.size = size
    
    def setFont(self,font_path:str='C:\\Windows\\Fonts\\simkai.ttf')->None:
        self.font_path = font_path

    def setColor(self,color:str="white")->None:
        self.color = color

    def textToImageLoader(self)->ImageLoader:
        im = Image.new("RGB", (1, 1), 'white')
        draw= ImageDraw.Draw(im)
        font = ImageFont.truetype(self.font_path, self.size)
        im_size=draw.textsize(self.getText(),font=font)
        im = Image.new("RGBA", im_size, (0,0,0,0))
        draw= ImageDraw.Draw(im)
        draw.text((0,0), self.getText(), font=font, fill=self.color)
        self.im = im
        image_loader = ImageLoader(self.game_main_loop)
        image_loader.loadfromImg(self.im)
        return image_loader
