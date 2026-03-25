import random

from resources import resources
from utils import InteractiveSprite


class Tree(InteractiveSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(resources["hole"], *args, **kwargs)

        self.tree_type = None
        self.growth_state = 0

    def set_tree_type(self, tree_type):
        self.tree_type = tree_type
        self.growth_state = 0
        self.image = resources[self.tree_type][self.growth_state]

    def grow(self):
        if (
            self.tree_type is not None
            and len(resources[self.tree_type]) > self.growth_state + 1
        ):
            self.growth_state += 1
            self.image = resources[self.tree_type][self.growth_state]

    def on_hover_start(self):
        self.color = (255, 200, 200)

    def on_hover_end(self):
        self.color = (255, 255, 255)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.tree_type is None:
            self.set_tree_type(random.choice(["tree", "pine_tree", "bonsai"]))
        else:
            self.grow()
