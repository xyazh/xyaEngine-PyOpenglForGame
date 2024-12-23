from pyglgame.App import App
from pyglgame.Size import Size
from DemoGameObject import TestGameObject
from DemoCamera import DemoCamera
from DemoCamera1 import DemoCamera1
app = App()

#test_camera = DemoCamera(Size(int(1920/2), 1080))
#test_camera = DemoCamera1(Size(int(1920/2), 1080))
test_camera = DemoCamera1(Size(1920, 1080))
test_obj = TestGameObject()


app.window.setWindownSize((1920, 1080))
app.start()
