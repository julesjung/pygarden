import arcade
import arcade.gui

from data import load_game
from views.game import GameView


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        self.background_color = arcade.uicolor.DARK_BLUE_MIDNIGHT_BLUE

        self.sprites = arcade.SpriteList()
        self.logo = arcade.Sprite(
            "assets/logo.png",
            center_x=512,
            center_y=604,
        )
        self.sprites.append(self.logo)

    def on_show_view(self):
        self.manager.enable()

        buttons = arcade.load_spritesheet("assets/gui/buttons.png").get_texture_grid(
            (192, 64), 2, 8
        )

        new_game_button = arcade.gui.UITextureButton(
            x=100,
            y=400,
            width=192,
            height=64,
            texture=buttons[0],
            texture_pressed=buttons[1],
        )
        continue_button = arcade.gui.UITextureButton(
            x=100,
            y=300,
            width=192,
            height=64,
            texture=buttons[2],
            texture_pressed=buttons[3],
        )
        load_game_button = arcade.gui.UITextureButton(
            x=100,
            y=200,
            width=192,
            height=64,
            texture=buttons[4],
            texture_pressed=buttons[5],
        )
        quit_button = arcade.gui.UITextureButton(
            x=100,
            y=100,
            width=192,
            height=64,
            texture=buttons[6],
            texture_pressed=buttons[7],
        )

        new_game_button.on_click = self.on_new_game_button_click
        quit_button.on_click = self.on_quit_button_click

        self.manager.add(new_game_button)
        self.manager.add(continue_button)
        self.manager.add(load_game_button)
        self.manager.add(quit_button)

    def on_new_game_button_click(self, event):
        self.window.show_view(GameView(load_game()))

    def on_quit_button_click(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()

        self.sprites.draw()
        self.manager.draw()
