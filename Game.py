from pyglgame.App import App
from pyglgame.math.Size import Size
from DemoGameObject import TestGameObject
from pyglgame.gameobject.Camera3D import Camera3D
from DemoCamera import DemoCamera
app = App()

test_camera = DemoCamera()
#test_camera = DemoCamera1(Size(int(1920/2), 1080))
#test_camera = DemoCamera1(Size(1920, 1080))
#test_camera = Camera3D.test()
test_obj = TestGameObject()


app.window.setWindownSize((1920, 1080))
app.start()
