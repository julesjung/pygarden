import pyglet
from pyglet.sprite import Sprite

from resources import resources
from scene import Scene
from scenes.game import GameScene


class LoadingScene(Scene):
    def __init__(self):
        super().__init__()
        self.logo = Sprite(
            x=256,
            y=280,
            img=resources["logo"],
        )
        self.logo.opacity = 0

        self.opacity = 0.0

        pyglet.clock.schedule_interval(self.fade_in, 1 / 60.0)

    def draw(self):
        self.logo.draw()

    def fade_in(self, dt):
        self.opacity = min(255.0, self.opacity + dt * 128.0)
        self.logo.opacity = int(self.opacity)
        if self.opacity == 255.0:
            pyglet.clock.unschedule(self.fade_in)
            pyglet.clock.schedule_once(
                lambda dt: pyglet.clock.schedule_interval(self.fade_out, 1 / 60.0), 5.0
            )

    def fade_out(self, dt):
        self.opacity = max(0.0, self.opacity - dt * 128.0)
        self.logo.opacity = int(self.opacity)
        if self.opacity == 0.0:
            pyglet.clock.unschedule(self.fade_out)
            self.manager.load(GameScene())
