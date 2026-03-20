import random

import pyglet

from game.camera import Camera
from game.leaf_counter import LeafCounter
from game.resources import resources
from game.tree import Tree

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")

        self.player = pyglet.media.Player()
        self.player.queue(resources["soundtrack_1"])
        self.player.play()

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

        self.leaf_counter = LeafCounter(x=0, y=SCREEN_HEIGHT - 48)

        controllers = pyglet.input.get_controllers()

        self.controller = controllers[0] if controllers else None

        if self.controller is not None:
            self.controller.open()

            pyglet.clock.schedule(self.update)

    def on_draw(self):
        self.clear()

        with self.camera:
            self.batch.draw()

        self.leaf_counter.draw()

    def update(self, dt):
        self.camera.x += self.controller.leftx * dt * 60
        self.camera.y -= self.controller.lefty * dt * 60

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
