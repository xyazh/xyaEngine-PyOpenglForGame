from .BaseWindow import BaseWindow
from .openal.Device import Device
from .openal.Player import Player


class App:
    instance = None

    def __new__(cls, title: str = "New Function", size: tuple = (960, 540), position: tuple = (0, 0), is_full_screen: bool = False):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.__first_init__(title=title, size=size, position=position, is_full_screen=is_full_screen)
        return cls.instance

    def __first_init__(self, title: str = "New Function", size: tuple = (960, 540), position: tuple = (0, 0), is_full_screen: bool = False):
        self.window: BaseWindow = BaseWindow(self, title, size, position, is_full_screen)
        self.audio_device = Device()
        self.audio_player = Player(self.audio_device)
        self.audio_player.setPosition(0, 0, -5)
        Device.app_instance = self.audio_device
        Player.app_instance = self.audio_player

    def __init__(self, title: str = "New Function", size: tuple = (960, 540), position: tuple = (0, 0), is_full_screen: bool = False):
        pass

    def start(self):
        self.window.run()
