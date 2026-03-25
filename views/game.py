import json
import time

import arcade
import arcade.gui
import arcade.gui.experimental

from data import get_save_file
from music import MusicPlayer
from plants_properties import plants
from utils.format import format_number

BUTTON_STYLE = {
    "normal": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=16),
    "hover": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=16),
    "press": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=16),
    "disabled": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=16),
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

        self.shop = arcade.Sprite("assets/shop.png", center_x=1552, center_y=1216)
        self.foregroud_sprites.append(self.shop)

        self.plant_textures: list[list[arcade.Texture]] = []

        for plant in plants:
            sheet = arcade.load_spritesheet(plant["spritesheet"])
            self.plant_textures.append(sheet.get_texture_grid((192, 256), 3, 3))

        self.camera = arcade.Camera2D(position=(1024, 768))

        for x in range(4):
            for y in range(2):
                sprite = arcade.Sprite(
                    "assets/placement_dirt.png",
                    center_x=224 + x * 192,
                    center_y=1088 + y * 256,
                )
                self.foregroud_sprites.append(sprite)

        for x in range(4):
            for y in range(2):
                sprite = arcade.Sprite(
                    "assets/placement_water.png",
                    center_x=224 + x * 192,
                    center_y=320 + y * 256,
                )
                self.foregroud_sprites.append(sprite)

        for x in range(4):
            for y in range(2):
                sprite = arcade.Sprite(
                    "assets/placement_jungle.png",
                    center_x=1280 + x * 192,
                    center_y=320 + y * 256,
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

        self.shop_sprites = arcade.SpriteList()
        self.shop_plant_preview = arcade.BasicSprite(
            self.plant_textures[0][2], center_x=744, center_y=524
        )
        self.shop_sprites.append(self.shop_plant_preview)

        self.plant_widgets = []

        self.current_plant_index = 0

        self.shop_manager = arcade.gui.UIManager()

    def on_show_view(self) -> None:
        layout = arcade.gui.UILayout()

        self.shop_price_label = arcade.gui.UILabel(
            text=str(plants[0]["price"]),
            x=625,
            y=327,
            width=222,
            height=48,
            font_name="Do Hyeon",
            font_size=20,
            align="center",
        )

        layout.add(self.shop_price_label)

        shop_scroll_area = arcade.gui.experimental.UIScrollArea(
            x=130,
            y=89,
            width=350,
            height=371,
        )
        shop_plant_list = arcade.gui.UIBoxLayout(space_between=16)

        for index, plant in enumerate(plants):
            plant_widget = arcade.gui.UITextureButton(
                width=350,
                height=48,
                texture=arcade.load_texture("assets/shop/frame.png"),
                texture_disabled=arcade.load_texture("assets/shop/frame_clicked.png"),
                text=plant["name"],
                style=BUTTON_STYLE,
            )

            self.plant_widgets.append(plant_widget)

            @plant_widget.event
            def on_click(event, index=index, plant=plant):
                self.plant_widgets[self.current_plant_index].disabled = False
                self.plant_widgets[index].disabled = True
                self.shop_plant_preview.texture = self.plant_textures[index][2]
                self.shop_price_label.text = format_number(plant["price"])
                self.current_plant_index = index

            shop_plant_list.add(plant_widget)

        shop_scroll_area.add(shop_plant_list)
        shop_scroll_area.scroll_speed = 16
        shop_scroll_area.invert_scroll = True

        layout.add(shop_scroll_area)

        self.shop_manager.add(layout)

    def on_draw(self):
        self.clear()

        with self.camera.activate():
            self.background_sprites.draw()
            self.foregroud_sprites.draw()

        self.overlay_sprites.draw()

        if self.in_shop:
            arcade.draw_lbwh_rectangle_filled(0, 0, 1024, 768, (0, 0, 0, 192))
            self.shop_background_sprites.draw()
            self.shop_sprites.draw()
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
