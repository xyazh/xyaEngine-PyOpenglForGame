from .BaseWindow import BaseWindow
from .openal.Device import Device
from .openal.Player import Player


class App:
    instance = None

    def __new__(cls, size: tuple = (960, 540), position: tuple = (0, 0), is_full_screen: bool = False):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.__first_init__(
                size=size, position=position, is_full_screen=is_full_screen)
        return cls.instance

    def __first_init__(self, size: tuple = (960, 540), position: tuple = (0, 0), is_full_screen: bool = False):
        self.window: BaseWindow = BaseWindow(
            self,  size, position, is_full_screen)
        self.audio_device = Device()
        self.audio_player = Player(self.audio_device)
        Device.app_instance = self.audio_device
        Player.app_instance = self.audio_player
        self.progress_bar = 0
        self.init_fucs = []

    def __init__(self, size: tuple = (960, 540), position: tuple = (0, 0), is_full_screen: bool = False):
        pass

    def start(self, title: str = "New Functional") -> None:
        self.window.run(title)

    def onLoad(self, *args, call_back=None, **kwargs):
        def decorator(func):
            self.init_fucs.append((func, call_back, args, kwargs))
            return func
        return decorator

    def addInitFunc(self, func, *args, call_back=None, **kwargs):
        self.init_fucs.append((func, call_back, args, kwargs))
