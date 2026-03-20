from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite

from game.camera import Camera
from game.resources import resources
from game.scene import Scene
from game.sprites import Shop
from game.sprites.leaf_counter import LeafCounter


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

    def on_enter(self):
        self.camera = Camera(self.manager.window)

    def draw(self):
        with self.camera:
            self.batch.draw()

        self.leaf_counter.draw()
