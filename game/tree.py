import pyglet
import random

TREE_WIDTH = 256
TREE_HEIGHT = 384
TREE_SCALE = 0.5


def load_tree_images():
    image_grids = {
        "tree": pyglet.image.load("game/resources/plants/tree.png"),
        "pine_tree": pyglet.image.load("game/resources/plants/pine_tree.png"),
    }

    return {
        "tree": pyglet.image.ImageGrid(image_grids["tree"], 1, 2),
        "pine_tree": pyglet.image.ImageGrid(image_grids["pine_tree"], 1, 2),
    }


tree_images = load_tree_images()


class Tree(pyglet.sprite.Sprite):
    def __init__(self, tree_type, *args, **kwargs):
        self.tree_type = tree_type

        super().__init__(tree_images[self.tree_type][1], *args, **kwargs)
        self.scale = TREE_SCALE

        pyglet.clock.schedule_once(self.grow, 10.0 + random.uniform(-1.0, 1.0))

    def grow(self, _delta_time):
        self.image = tree_images[self.tree_type][0]
