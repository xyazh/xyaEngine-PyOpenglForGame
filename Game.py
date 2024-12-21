from pyglgame.App import App
from DemoGameObject import TestGameObject

app = App()
test_obj = TestGameObject()


app.window.setWindownSize((1920,1080))
app.start()