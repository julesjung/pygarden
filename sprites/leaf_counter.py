from pyglet.sprite import Sprite
from pyglet.text import Label

from resources import resources


class LeafCounter:
    def __init__(self, count, x, y):
        self.image = Sprite(resources["leaf_counter"], x, y)
        self.text = Label(str(count), x + 16, y + 2)

    def draw(self):
        self.image.draw()
        self.text.draw()
