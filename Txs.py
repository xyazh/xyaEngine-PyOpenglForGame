from AssbmlyLoader import *



class Txs:
    def __init__(self,assLoader:AssbmlysLoader):
        self.assLoader = assLoader
        self.imagesId = assLoader.getImagesId()
        self.texturesId = {}
        self.texturesSize = {}
        
    def getIdFromName(self,name:str):
        if not name in self.texturesId:
            assid = self.assLoader.getId(name)
            imgAss = self.assLoader.getAssbmly(assid)
            self.texturesId.update({imgAss.name:imgAss.data.toTex()})
            self.texturesSize.update({imgAss.name:imgAss.data.getSize()})
        return self.texturesId[name]

    def getSizeFromName(self,name:str):
        if not name in self.texturesSize:
            if not name in self.texturesId:
                self.getIdFromName(name)
            else:
                assid = self.assLoader.getId(name)
                imgAss = self.assLoader.getAssbmly(assid)
                self.texturesSize.update({imgAss.name:imgAss.data.getSize()})
        return self.texturesSize[name]