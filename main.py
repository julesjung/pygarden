import random
import pyglet
from game.tree import Tree
from game.camera import Camera
from game.picker import pick_sprite_under_point

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")

        self.camera = Camera(self)

        self.batch = pyglet.graphics.Batch()
        self.trees = []
        self.grid = []

        self.hovered = None

        for x in range(8):
            for y in range(10):
                group = pyglet.graphics.Group(order=-y)
                tree = Tree(
                    tree_type=random.choice(["tree", "pine_tree"]),
                    x=x * 128,
                    y=y * 64,
                    batch=self.batch,
                    group=group,
                )
                self.trees.append(tree)

        grid_group = pyglet.graphics.Group(order=-8192)

        for x in range(9):
            line = pyglet.shapes.Line(
                x * 128,
                0,
                x * 128,
                SCREEN_HEIGHT,
                color=(63, 63, 63),
                batch=self.batch,
                group=grid_group,
            )
            self.grid.append(line)

        for y in range(13):
            line = pyglet.shapes.Line(
                0,
                y * 64,
                SCREEN_WIDTH,
                y * 64,
                color=(63, 63, 63),
                batch=self.batch,
                group=grid_group,
            )
            self.grid.append(line)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.batch.draw()

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
