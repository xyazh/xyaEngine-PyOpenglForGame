from pyglgame.App import App
from DemoGameObject import TestGameObject

app = App()
test_obj = TestGameObject()


app.window.setWindownSize((192,108))
app.start()