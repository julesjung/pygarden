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


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.logo = Sprite(img=resources["logo"])

        self.batch = Batch()
        self.interactive_sprites = []

        self.hovered = None

        self.background = Sprite(
            img=resources["background"], batch=self.batch, group=Group(order=-127)
        )
        self.soil = Sprite(
            img=resources["soil"], batch=self.batch, group=Group(order=-128)
        )
        self.shop = Shop(
            x=896, y=512, img=resources["shop"], batch=self.batch, group=Group(order=0)
        )
        self.interactive_sprites.append(self.shop)

        self.leaf_counter = LeafCounter(x=0, y=0)

        self.player = MusicPlayer()
        self.player.play()

        pyglet.clock.schedule_interval(lambda dt: self.player.next_source, 1.0)

    def on_enter(self):
        self.camera = Camera(self.manager.window)

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
