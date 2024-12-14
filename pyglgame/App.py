from .BaseWindow import BaseWindow

class App:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self,title:str="New Function",size:tuple=(960,540),position:tuple=(0,0),is_full_screen:bool=False):
        self.window:BaseWindow = BaseWindow(self,title,size,position,is_full_screen)

    def start(self):
        self.window.run()