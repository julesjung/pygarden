import pyglet
from pyglet.window import Window

from resources import resources
from scenes.game import Game

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

pyglet.options.dpi_scaling = "stretch"
pyglet.options.text_antialiasing = False

window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")
window.set_icon(resources["icon"])

game = Game(window, {"leaf_count": 0})
game.on_enter()


@window.event
def on_draw():
    window.clear()
    game.draw()


pyglet.app.run()
