import arcade
from arcade.gui import UITextureButton


class Button(UITextureButton):
    def __init__(self, *, x=0, y=0, width=None, height=None, text="", multiline=False):

        texture = arcade.load_texture(
            ":resources:/gui_basic_assets/button/red_normal.png"
        )
        texture_hovered = arcade.load_texture(
            ":resources:/gui_basic_assets/button/red_hover.png"
        )
        texture_pressed = arcade.load_texture(
            ":resources:/gui_basic_assets/button/red_press.png"
        )
        texture_disabled = arcade.load_texture(
            ":resources:/gui_basic_assets/button/red_disabled.png"
        )

        arcade.resources.load_liberation_fonts()

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            texture=texture,
            texture_hovered=texture_hovered,
            texture_pressed=texture_pressed,
            texture_disabled=texture_disabled,
            text=text,
            multiline=multiline,
        )
