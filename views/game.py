import json
import time

import arcade
import arcade.gui
import arcade.gui.experimental

from data import get_save_file
from music import MusicPlayer
from plants_properties import plants

BUTTON_STYLE = {
    "normal": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon"),
    "hover": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon"),
    "press": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon"),
    "disabled": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon"),
}


class GameView(arcade.View):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.background_sprites = arcade.SpriteList()
        self.foregroud_sprites = arcade.SpriteList()

        self.background = arcade.Sprite(
            "assets/background.png", center_x=1024, center_y=768
        )
        self.background_sprites.append(self.background)

        self.shop = arcade.Sprite("assets/shop.png", center_x=1360, center_y=912)
        self.foregroud_sprites.append(self.shop)

        self.camera = arcade.Camera2D(position=(512, 384))

        for x in range(4):
            for y in range(2):
                sprite = arcade.Sprite(
                    "assets/placement_dirt.png",
                    center_x=128 + x * 192,
                    center_y=192 + y * 256,
                )
                self.foregroud_sprites.append(sprite)

        for x in range(4):
            for y in range(2):
                sprite = arcade.Sprite(
                    "assets/placement_dirt.png",
                    center_x=128 + x * 192,
                    center_y=928 + y * 256,
                )
                self.foregroud_sprites.append(sprite)

        for x in range(4):
            for y in range(2):
                sprite = arcade.Sprite(
                    "assets/placement_dirt.png",
                    center_x=1184 + x * 192,
                    center_y=192 + y * 256,
                )
                self.foregroud_sprites.append(sprite)

        self.player = MusicPlayer()
        self.player.play()

        self.hovered = None

        self.overlay_sprites = arcade.SpriteList()

        self.in_shop = False
        self.shop_background_sprites = arcade.SpriteList()
        self.shop_background = arcade.BasicSprite(
            arcade.load_texture("assets/shop/background.png"),
            center_x=512,
            center_y=384,
        )
        self.shop_background_sprites.append(self.shop_background)

        self.shop_manager = arcade.gui.UIManager()

    def on_show_view(self) -> None:
        shop_scroll_area = arcade.gui.experimental.UIScrollArea(
            x=130,
            y=89,
            width=350,
            height=371,
        )
        shop_tree_list = arcade.gui.UIBoxLayout(space_between=16)

        for plant in plants:
            plant_widget = arcade.gui.UITextureButton(
                width=350,
                height=48,
                texture=arcade.load_texture("assets/shop/frame.png"),
                text=plant["name"],
                style=BUTTON_STYLE,
            )
            shop_tree_list.add(plant_widget)

        shop_scroll_area.add(shop_tree_list)
        shop_scroll_area.scroll_speed = 16
        shop_scroll_area.invert_scroll = True

        self.shop_manager.add(shop_scroll_area)

    def on_draw(self):
        self.clear()

        with self.camera.activate():
            self.background_sprites.draw()
            self.foregroud_sprites.draw()

        self.overlay_sprites.draw()

        if self.in_shop:
            arcade.draw_lbwh_rectangle_filled(0, 0, 1024, 768, (0, 0, 0, 192))
            self.shop_background_sprites.draw()
            self.shop_manager.draw()

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int
    ):
        if not self.in_shop:
            self.camera.position = (
                max(512, min(self.camera.position.x - dx, 1536)),
                max(384, min(self.camera.position.y - dy, 1152)),
            )

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.in_shop:
            (world_x, world_y, _) = self.camera.unproject((x, y))
            hovered = None
            for sprite in self.foregroud_sprites:
                if sprite.collides_with_point((world_x, world_y)):
                    hovered = sprite
                    break
            if hovered != self.hovered:
                if self.hovered is not None:
                    self.hovered.color = (255, 255, 255)
                if hovered is not None:
                    hovered.color = (255, 200, 200)
                self.hovered = hovered

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.in_shop:
            (world_x, world_y, _) = self.camera.unproject((x, y))
            if self.shop.collides_with_point((world_x, world_y)):
                self.in_shop = True
                self.shop_manager.enable()
        else:
            if not self.shop_background.collides_with_point((x, y)):
                self.in_shop = False
                self.shop_manager.disable()

    def save_game(self):
        self.data["last_played"] = time.time()
        with open(get_save_file(), "w") as f:
            json.dump(self.data, f)

    """
    def on_shop_press(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.dispatch_event("open_shop")
    """
