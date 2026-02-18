import random
import pyglet
from game.tree import Tree
from game.camera import Camera

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")

        self.camera = Camera(self)

        self.batch = pyglet.graphics.Batch()
        self.interactive_sprites = []

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
                self.interactive_sprites.append(tree)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        world_x, world_y = self.camera.screen_to_world(x, y)
        hovered = None
        for sprite in self.interactive_sprites:
            if sprite.hit_test(world_x, world_y):
                hovered = sprite
                break
        if hovered != self.hovered:
            if self.hovered is not None:
                self.hovered.on_hover_end()
            if hovered is not None:
                hovered.on_hover_start()
            self.hovered = hovered

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self.camera.x -= dx
            self.camera.y -= dy

    def on_mouse_press(self, x, y, button, modifiers):
        world_x, world_y = self.camera.screen_to_world(x, y)
        for sprite in self.interactive_sprites:
            if sprite.hit_test(world_x, world_y):
                sprite.on_mouse_press(x, y, button, modifiers)
                break


if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
