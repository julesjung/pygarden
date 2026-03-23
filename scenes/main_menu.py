import time

import pyglet
from pyglet.graphics import Batch
from pyglet.gui import PushButton
from pyglet.sprite import Sprite

from data import load_game
from resources import resources
from scene import Scene
from scenes.game import FadeOverlay, Game


class MainMenu(Scene):
    def __init__(self, window):
        super().__init__(window)

        self.logo = Sprite(
            x=256,
            y=500,
            img=resources["logo"],
        )
        self.logo.opacity = 0

        self.batch = Batch()
        self.buttons = []
        self.new_game_button = PushButton(
            100,
            400,
            resources["buttons"][7],
            resources["buttons"][6],
            batch=self.batch,
        )
        self.continue_button = PushButton(
            100,
            300,
            resources["buttons"][5],
            resources["buttons"][4],
            batch=self.batch,
        )
        self.load_game_button = PushButton(
            100,
            200,
            resources["buttons"][3],
            resources["buttons"][2],
            batch=self.batch,
        )
        self.quit_button = PushButton(
            100,
            100,
            resources["buttons"][1],
            resources["buttons"][0],
            batch=self.batch,
        )
        self.buttons.append(self.new_game_button)
        self.buttons.append(self.continue_button)
        self.buttons.append(self.load_game_button)
        self.buttons.append(self.quit_button)

        for button in self.buttons:
            button._sprite.opacity = 0

        self.elapsed = 0.0
        self.phase = "logo"

        self.new_game_button.set_handler("on_release", self.on_new_game_button_pressed)
        self.continue_button.set_handler("on_release", self.on_continue_button_pressed)
        self.quit_button.set_handler("on_release", self.on_quit_button_pressed)

    def on_enter(self):
        super().on_enter()

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def draw(self):
        self.logo.draw()
        self.batch.draw()

    def update(self, dt):
        if self.phase == "logo":
            if self.logo.opacity < 255:
                self.elapsed += dt
                self.logo.opacity = int(min(255, self.elapsed * 128))
                return
            else:
                self.phase = "buttons"

        if self.phase == "buttons":
            self.elapsed += dt
            new_opacity = int(min(255, (self.elapsed - 2) * 128))
            for button in self.buttons:
                button._sprite.opacity = new_opacity
            if new_opacity == 255:
                self.phase == "done"
            return

        if self.phase == "done":
            pyglet.clock.unschedule(self.update)

    def on_new_game_button_pressed(self, widget):
        pass

    def on_continue_button_pressed(self, widget):
        pass

    def on_quit_button_pressed(self, widget):
        pyglet.app.exit()

    def on_exit(self):
        super().on_exit()
