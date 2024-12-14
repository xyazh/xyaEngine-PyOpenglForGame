from io import BytesIO
from .xyazhServer.ConsoleMessage import ConsoleMessage


class ResourceLocation:
    @property
    def data(self) -> bytes:
        if self._data is None:
            self.load()
        return self._data
    
    @data.setter
    def data(self, value: bytes) -> None:
        self._data = value

    @data.deleter
    def data(self):
        del self._data

    def __init__(self, path: str, preload: bool = False) -> None:
        self.path = path
        self.preload = preload
        self._data: bytes = None
        if preload:
            self.load()

    def load(self):
        if self.path[:5] == "blob:":
            self.data = b""
            return
        try:
            with open(self.path, "rb") as f:
                self.data = f.read()
        except FileNotFoundError:
            ConsoleMessage.printError(f"File not found: {self.path}")

    def release(self):
        self._data = None

    def toBytes(self) -> bytes:
        return self.data

    def tryToString(self, e: str = "utf-8") -> str:
        try:
            return self.data.decode(e)
        except UnicodeDecodeError:
            ConsoleMessage.printError(f"File {self.path} is not a text file")
        return ""
    
    def getIO(self) -> BytesIO:
        return BytesIO(self.data)
    
    def __str__(self) -> str:
        return f"ResourceLocation<{self.path}>"
