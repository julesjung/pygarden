import pyglet
from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite
from pyglet.window import mouse

from camera import Camera
from music import MusicPlayer
from resources import resources
from scene import Scene
from sprites import Shop
from sprites.leaf_counter import LeafCounter
from sprites.tree import Tree


class GameScene(Scene):
    def __init__(self):
        super().__init__()
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

        self.leaf_counter = LeafCounter(x=0, y=0)

        self.player = MusicPlayer()
        self.player.play()

        pyglet.clock.schedule_interval(lambda dt: self.player.next_source, 1.0)

    def on_enter(self):
        if self.manager is not None:
            self.camera = Camera(self.manager.window)
            self.camera.x = 512
            self.camera.y = 384

    def draw(self):
        with self.camera:
            self.batch.draw()

        self.leaf_counter.draw()

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
