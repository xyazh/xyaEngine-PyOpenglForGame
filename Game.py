from pyglgame.App import App
from pyglgame.Size import Size
from DemoGameObject import TestGameObject
from pyglgame.Camera3D import Camera3D
app = App()

#test_camera = DemoCamera(Size(int(1920/2), 1080))
#test_camera = DemoCamera1(Size(int(1920/2), 1080))
#test_camera = DemoCamera1(Size(1920, 1080))
test_camera = Camera3D.test()
test_obj = TestGameObject()


app.window.setWindownSize((1920, 1080))
app.start()
