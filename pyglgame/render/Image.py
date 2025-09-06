import numpy as np
from PIL import Image as PILImage
from ..ResourceLocation import ResourceLocation
from .Texture import Texture

class Image:

    @property
    def width(self) -> int:
        return self.image.width
    
    @property
    def height(self) -> int:
        return self.image.height
    
    @width.setter
    def width(self,value:int):
        pass

    @height.setter
    def height(self,value:int):
        pass

    def __init__(self,resource_location:ResourceLocation,use_hdr: bool = False):
        self.image:PILImage = PILImage.open(resource_location.getIO()).convert("RGBA")
        if use_hdr:
            self.data = np.array(self.image,dtype=np.float32)
            #self.data = np.divide(self.data,255.0)
        else:
            self.data = np.array(self.image)
        self.use_hdr:bool = use_hdr

    def getTexture(self) -> Texture:
        return Texture.createFromImage(self)