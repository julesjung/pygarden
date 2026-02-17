import random
import pyglet
from game.tree import Tree, TREE_WIDTH, TREE_HEIGHT
from game.camera import Camera
from game.picker import pick_sprite_under_point

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")

        self.camera = Camera(self)

        self.tree_batch = pyglet.graphics.Batch()
        self.trees = []

        self.hovered = None

        for _ in range(20):
            x, y = (
                random.randint(0, SCREEN_WIDTH - TREE_WIDTH),
                random.randint(0, SCREEN_HEIGHT - TREE_HEIGHT),
            )
            group = pyglet.graphics.Group(order=-y)
            tree = Tree(
                tree_type=random.choice(["tree", "pine_tree"]),
                x=x,
                y=y,
                batch=self.tree_batch,
                group=group,
            )
            self.trees.append(tree)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.tree_batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        world_x, world_y = self.camera.screen_to_world(x, y)
        hovered = pick_sprite_under_point(self.trees, world_x, world_y)
        if self.hovered != hovered:
            if hovered is not None:
                hovered.color = (255, 200, 200)
            if self.hovered is not None:
                self.hovered.color = (255, 255, 255)
            self.hovered = hovered

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.camera.x -= dx
            self.camera.y -= dy


if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
