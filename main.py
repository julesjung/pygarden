import random
import pyglet
from game.tree import Tree
from game.camera import Camera


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(1024, 768, "PyGarden")

        self.camera = Camera()

        self.tree_batch = pyglet.graphics.Batch()
        self.trees = []

        for y in reversed(range(4)):
            for x in range(4):
                tree = Tree(
                    tree_type=random.choice(["tree", "pine_tree"]),
                    x=x * 128 + y * 64,
                    y=y * 128,
                    batch=self.tree_batch,
                )

                self.trees.append(tree)

    def on_draw(self):
        self.clear()

        self.view = self.camera.get_view_matrix()

        self.tree_batch.draw()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.camera.x -= dx
            self.camera.y -= dy


if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
