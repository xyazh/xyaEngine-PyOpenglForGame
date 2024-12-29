from pyglgame.App import App
from DemoGameObject import DemoGameObject
from DemoGameObject1 import DemoGameObject1
from DemoCamera import DemoCamera
from DemoCamera1 import DemoCamera1
app = App()



"""test_camera = DemoCamera()
test_obj = DemoGameObject()"""


test_camera = DemoCamera1()
test_obj = DemoGameObject1()


app.window.setWindownSize((1920, 1080))
app.start()
