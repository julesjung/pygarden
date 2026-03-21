import pyglet

from resources import resources
from scene import SceneManager
from scenes import LoadingScene

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")
        self.set_icon(resources["leaf"])

        self.scene_manager = SceneManager(self)
        self.scene_manager.load(LoadingScene())

        self.player = pyglet.media.Player()
        self.player.queue(resources["soundtrack_1"])
        self.player.play()

    def on_draw(self):
        self.clear()

        self.scene_manager.draw()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.scene_manager.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int
    ):
        self.scene_manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.scene_manager.on_mouse_press(x, y, button, modifiers)
