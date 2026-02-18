import pyglet
from .resources import resources


class LeafCounter(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(resources["leaf_counter"])
