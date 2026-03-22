import pyglet
from pyglet.window import Window

from resources import resources
from scene import SceneManager
from scenes import MainMenu

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

pyglet.options.dpi_scaling = "stretch"

window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")
window.set_icon(resources["icon"])

scene_manager = SceneManager(window)
scene_manager.set_scene(MainMenu())


@window.event
def on_draw():
    window.clear()
    scene_manager.draw()


@window.event
def on_mouse_motion(x: int, y: int, dx: int, dy: int):
    scene_manager.on_mouse_motion(x, y, dx, dy)


@window.event
def on_mouse_drag(x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
    scene_manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


@window.event
def on_mouse_press(x: int, y: int, button: int, modifiers: int):
    scene_manager.on_mouse_press(x, y, button, modifiers)


pyglet.app.run()
