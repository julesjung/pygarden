from pyglet.sprite import Sprite
from pyglet.text import Label

from resources import resources


class LeafCounter:
    def __init__(self, x, y):
        self.image = Sprite(resources["leaf_counter"], x, y)
        self.text = Label(
            f"{890231:.2e}",
            x + 176,
            y + 24,
            width=128,
            anchor_x="right",
            anchor_y="center",
            font_name="Do Hyeon",
            font_size=20,
        )

    def draw(self):
        self.image.draw()
        self.text.draw()
