from .sprite import InteractiveSprite
from .resources import resources

TREE_WIDTH = 256
TREE_HEIGHT = 384
TREE_SCALE = 0.5


class Tree(InteractiveSprite):
    def __init__(self, tree_type, *args, **kwargs):
        self.tree_type = tree_type

        super().__init__(resources[self.tree_type][1], *args, **kwargs)
        self.scale = TREE_SCALE

    def grow(self):
        self.image = resources[self.tree_type][0]

    def on_hover_start(self):
        self.color = (255, 200, 200)

    def on_hover_end(self):
        self.color = (255, 255, 255)

    def on_mouse_press(self, x, y, button, modifiers):
        self.grow()
