from Map import *

class Maps:
    def __init__(self)->None:
        self.__maps__ = {}
        self.__idName__ = {}
        self.__nameId__ = {}
        self.__endId__ = 0

    def addMap(self,name:str,map:Map)->int:
        self.__maps__.update({self.__endId__:map})
        self.__idName__.update({self.__endId__:name})
        self.__nameId__.update({name:self.__endId__})
        id = self.__endId__
        self.__endId__ += 1
        return id

    def getMapFromId(self,id:int)->Map:
        return self.__maps__[id]

    def getIdFromName(self,name:str)->int:
        return self.__nameId__[name]

    def getNameFromId(self,id:str)->str:
        return self.__idName__[id]

    def getMapFromName(self,name:str)->Map:
        id = self.getIdFromName(name)
        return self.getMapFromId(id)