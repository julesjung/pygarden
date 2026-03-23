import json
import time

import pyglet
from pyglet.graphics import Batch, Group
from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite
from pyglet.window import Window, mouse

from camera import Camera
from data import get_save_file
from music import MusicPlayer
from resources import resources
from scene import Scene
from scenes.shop import ShopView
from sprites import Shop
from sprites.leaf_counter import LeafCounter
from sprites.tree import Tree


class FadeOverlay:
    def __init__(self, window):
        self.rectangle = Rectangle(
            0,
            0,
            width=window.width,
            height=window.height,
            color=(0, 0, 0),
        )
        self.rectangle.opacity = 255
        self.elapsed = 0.0
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def update(self, dt):
        if self.rectangle.opacity > 0:
            self.elapsed += dt
            self.rectangle.opacity = int(max(0, 255 - self.elapsed * 128))
            return

        if self.elapsed >= 2.0:
            pyglet.clock.unschedule(self.update)

    def draw(self):
        self.rectangle.draw()


class Game(Scene):
    def __init__(self, window: Window, data):
        super().__init__(window)

        self.window = window
        self.data = data

        self.batch = Batch()

        self.background = Sprite(
            img=resources["background"], batch=self.batch, group=Group(order=-127)
        )
        self.soil = Sprite(
            img=resources["soil"], batch=self.batch, group=Group(order=-128)
        )

        self.interactive_sprites = []

        self.hovered = None
        self.shop = Shop(x=1456, y=1040, batch=self.batch)
        self.interactive_sprites.append(self.shop)

        self.camera = Camera(self.window)
        self.camera.x = 512
        self.camera.y = 384

        for x in range(4):
            for y in range(2):
                sprite = Tree(x=128 + x * 192, y=192 + y * 256, batch=self.batch)
                self.interactive_sprites.append(sprite)

        for x in range(4):
            for y in range(2):
                sprite = Tree(x=128 + x * 192, y=928 + y * 256, batch=self.batch)
                self.interactive_sprites.append(sprite)

        for x in range(4):
            for y in range(2):
                sprite = Tree(x=1184 + x * 192, y=192 + y * 256, batch=self.batch)
                self.interactive_sprites.append(sprite)

        self.player = MusicPlayer()
        self.player.play()

        self.shop_view = ShopView(self.window)
        self.in_shop = False

        self.shop.set_handler("on_mouse_press", self.on_shop_press)

        self.save_game()
        self.leaf_counter = LeafCounter(self.data["leaf_count"], 0, 0)

        pyglet.clock.schedule_interval(lambda dt: self.player.next_source, 1.0)

    def on_enter(self):
        super().on_enter()
        self.fade_overlay = FadeOverlay(self.window)

    def on_exit(self):
        super().on_exit()

    def draw(self):
        with self.camera:
            self.batch.draw()

        self.leaf_counter.draw()
        self.fade_overlay.draw()

        if self.in_shop:
            self.shop_view.draw()

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
        if buttons & mouse.LEFT:
            self.camera.x = max(0, min(self.camera.x - dx, 1024))
            self.camera.y = max(0, min(self.camera.y - dy, 768))

    def on_mouse_press(self, x, y, button, modifiers):
        world_x, world_y = self.camera.screen_to_world(x, y)
        for sprite in self.interactive_sprites:
            if sprite.hit_test(world_x, world_y):
                sprite.on_mouse_press(x, y, button, modifiers)
                break

    def save_game(self):
        self.data["last_played"] = time.time()
        with open(get_save_file(), "w") as f:
            json.dump(self.data, f)

    def on_shop_press(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.in_shop = True
            self.shop_view.on_enter()
