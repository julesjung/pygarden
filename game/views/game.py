from random import choice
from arcade import View, SpriteList
from arcade.camera import Camera2D
from game.sprites import Tree


class GameView(View):
    def __init__(self):
        super().__init__()

        self.camera = None
        self.tree_list = None

    def setup(self):
        self.camera = Camera2D()
        self.tree_list = SpriteList()

        for x in range(4):
            for y in reversed(range(4)):
                tree = Tree(choice(["tree", "pine_tree"]))
                tree.position = (x * 128 + y * 64, y * 128 * 0.6)
                self.tree_list.append(tree)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.tree_list.draw()

    def on_update(self, delta_time):
        self.tree_list.update()

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.camera.position -= (dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        return super().on_mouse_press(x, y, button, modifiers)
