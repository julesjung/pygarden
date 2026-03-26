import time

import arcade
import arcade.gui
import arcade.gui.experimental

from music import MusicPlayer
from placements import (
    placements,
    plains_placements,
    savannah_placements,
    water_placements,
)
from plants_properties import plants
from utils import format_time, save_game_data
from utils.format import format_number

BUTTON_STYLE = {
    "normal": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=20),
    "hover": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=20),
    "press": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=20),
    "disabled": arcade.gui.UITextureButton.UIStyle(font_name="Do Hyeon", font_size=20),
}


class GameView(arcade.View):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.player = MusicPlayer()
        self.player.play()

        self.background_sprites = arcade.SpriteList()
        self.background = arcade.Sprite(
            ":assets:background.png", center_x=1024, center_y=768
        )
        self.background_sprites.append(self.background)

        self.foregroud_sprites: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.shop = arcade.Sprite(":assets:shop.png", center_x=1552, center_y=1216)
        self.foregroud_sprites.append(self.shop)

        self.plant_textures: list[list[arcade.Texture]] = []

        for plant in plants:
            sheet = arcade.load_spritesheet(plant["spritesheet"])
            self.plant_textures.append(sheet.get_texture_grid((192, 256), 3, 3))

        self.camera = arcade.Camera2D(position=(1024, 768))

        self.plains_plants: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.water_plants: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.savannah_plants: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.progress_bars: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        bar_texture = arcade.load_texture(":assets:progress_bar.png")

        for placement in plains_placements:
            self.plains_plants.append(
                arcade.Sprite(center_x=placement[0], center_y=placement[1])
            )
            self.progress_bars.append(
                arcade.Sprite(bar_texture, center_x=placement[0], center_y=placement[1])
            )

        for placement in water_placements:
            self.water_plants.append(
                arcade.Sprite(center_x=placement[0], center_y=placement[1])
            )
            self.progress_bars.append(
                arcade.Sprite(bar_texture, center_x=placement[0], center_y=placement[1])
            )

        for placement in savannah_placements:
            self.savannah_plants.append(
                arcade.Sprite(center_x=placement[0], center_y=placement[1])
            )
            self.progress_bars.append(
                arcade.Sprite(bar_texture, center_x=placement[0], center_y=placement[1])
            )

        self.needs_render = True

        self.hovered = None

        self.leaf_counter = arcade.Sprite(
            ":assets:leaf_counter.png", center_x=928, center_y=744
        )

        self.in_shop = False
        self.shop_background_sprites = arcade.SpriteList()
        self.shop_background = arcade.BasicSprite(
            arcade.load_texture(":assets:shop/background.png"),
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

        self.planting: tuple[int, int] | None = None
        self.planting_sprite = arcade.Sprite()

    def on_show_view(self) -> None:
        layout = arcade.gui.UILayout()

        buy_button_textures = arcade.load_spritesheet(
            ":assets:shop/buy_button.png"
        ).get_texture_grid((222, 48), 3, 3)

        self.shop_buy_button = arcade.gui.UITextureButton(
            text=str(plants[0]["price"]),
            x=625,
            y=339,
            width=222,
            height=48,
            texture=buy_button_textures[1],
            texture_pressed=buy_button_textures[2],
            texture_disabled=buy_button_textures[0],
            style=BUTTON_STYLE,
        )
        self.shop_buy_button.disabled = self.data["leaf_count"] < plants[0]["price"]

        properties = arcade.gui.UIBoxLayout(
            x=608,
            width=256,
            y=108,
            height=207,
            space_between=10,
            align="left",
        )
        self.shop_properties_name = arcade.gui.UILabel(
            text=f"- Nom : {plants[0]['name']}",
            font_name="Do Hyeon",
            align="left",
        )
        properties.add(self.shop_properties_name)
        self.shop_properties_price = arcade.gui.UILabel(
            text=f"- Prix : {format_number(plants[0]['price'])}",
            font_name="Do Hyeon",
            align="left",
        )
        properties.add(self.shop_properties_price)
        self.shop_properties_yield = arcade.gui.UILabel(
            text=f"- Production : {format_number(plants[0]['yield'])}",
            font_name="Do Hyeon",
            align="left",
        )
        properties.add(self.shop_properties_yield)
        growth_time = format_time(plants[0]["time_to_grow_adult"])
        self.shop_properties_growth = arcade.gui.UILabel(
            text=f"- Temps de croissance : {growth_time}",
            font_name="Do Hyeon",
            align="left",
        )
        properties.add(self.shop_properties_growth)
        production_time = format_time(plants[0]["time_to_grow_leaves"])
        self.shop_properties_production = arcade.gui.UILabel(
            text=f"- Temps de production : {production_time}",
            font_name="Do Hyeon",
            align="left",
        )
        properties.add(self.shop_properties_production)
        layout.add(properties)

        @self.shop_buy_button.event("on_click")
        def on_shop_buy_button_click(event: arcade.gui.UIOnClickEvent):
            self.in_shop = False
            self.shop_manager.disable()
            self.planting = (
                self.current_plant_index,
                plants[self.current_plant_index]["ground_type"],
            )
            if self.planting is not None:
                self.camera.position = [(512, 1152), (512, 384), (1536, 384)][
                    self.planting[1]
                ]
                self.planting_sprite.texture = self.plant_textures[self.planting[0]][0]
                self.planting_sprite.position = (event.x, event.y)

        layout.add(self.shop_buy_button)

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
                texture=arcade.load_texture(":assets:shop/frame.png"),
                texture_disabled=arcade.load_texture(":assets:shop/frame_clicked.png"),
                text=plant["name"],
                style=BUTTON_STYLE,
            )

            self.plant_widgets.append(plant_widget)

            @plant_widget.event
            def on_click(event, index=index, plant=plant):
                self.plant_widgets[self.current_plant_index].disabled = False
                self.plant_widgets[index].disabled = True
                self.shop_plant_preview.texture = self.plant_textures[index][2]
                self.shop_properties_name.text = f"- Nom : {plants[index]['name']}"
                self.shop_properties_price.text = (
                    f"- Prix : {format_number(plants[index]['price'])}"
                )
                self.shop_properties_yield.text = (
                    f"- Production : {format_number(plants[index]['yield'])}"
                )
                growth_time = format_time(plants[index]["time_to_grow_adult"])
                self.shop_properties_growth.text = (
                    f"- Temps de croissance : {growth_time}"
                )
                production_time = format_time(plants[index]["time_to_grow_leaves"])
                self.shop_properties_production.text = (
                    f"- Temps de production : {production_time}"
                )
                self.shop_buy_button.text = format_number(plant["price"])
                self.shop_buy_button.disabled = self.data["leaf_count"] < plant["price"]
                self.current_plant_index = index

            shop_plant_list.add(plant_widget)

        self.plant_widgets[0].disabled = True

        shop_scroll_area.add(shop_plant_list)
        shop_scroll_area.scroll_speed = 16
        shop_scroll_area.invert_scroll = True

        layout.add(shop_scroll_area)

        self.shop_manager.add(layout)

    def update_plant_sprites(self):
        for index, plant in enumerate(self.plains_plants):
            plant_data = self.data["plants"][0][index]
            if plant_data is None:
                plant.texture = arcade.load_texture(":assets:placements/plains.png")
            else:
                plant.textures = self.plant_textures[plant_data["type"]]
                plant.set_texture(plant_data["growth_stage"])

        for index, plant in enumerate(self.water_plants):
            plant_data = self.data["plants"][1][index]
            if plant_data is None:
                plant.texture = arcade.load_texture(":assets:placements/water.png")
            else:
                plant.textures = self.plant_textures[plant_data["type"]]
                plant.set_texture(plant_data["growth_stage"])

        for index, plant in enumerate(self.savannah_plants):
            plant_data = self.data["plants"][2][index]
            if plant_data is None:
                plant.texture = arcade.load_texture(":assets:placements/savannah.png")
            else:
                plant.textures = self.plant_textures[plant_data["type"]]
                plant.set_texture(plant_data["growth_stage"])

    def on_draw(self):
        self.clear()

        with self.camera.activate():
            self.background_sprites.draw()
            self.plains_plants.draw()
            self.water_plants.draw()
            self.savannah_plants.draw()
            self.foregroud_sprites.draw()
            current_time = time.time()
            for list_index, plant_list in enumerate(self.data["plants"]):
                for index, plant in enumerate(plant_list):
                    if plant is not None and plant["growth_stage"] != 2:
                        value = 0.0
                        if plant["growth_stage"] == 0:
                            value = min(
                                1.0,
                                (current_time - plant["last_stage_time"])
                                / plants[plant["type"]]["time_to_grow_adult"],
                            )
                        elif plant["growth_stage"] == 1:
                            value = min(
                                1.0,
                                (current_time - plant["last_stage_time"])
                                / plants[plant["type"]]["time_to_grow_leaves"],
                            )
                        arcade.draw_sprite(self.progress_bars[list_index * 8 + index])
                        (center_x, center_y) = placements[list_index][index]
                        arcade.draw_lbwh_rectangle_filled(
                            center_x - 54,
                            center_y - 118,
                            int(value * 91),
                            5,
                            (255, 255, 235),
                        )

        arcade.draw_sprite(self.leaf_counter)
        arcade.draw_text(
            format_number(self.data["leaf_count"]),
            x=1000,
            y=744,
            font_name="Do Hyeon",
            font_size=20,
            anchor_x="right",
            anchor_y="center",
        )

        if self.in_shop:
            arcade.draw_lbwh_rectangle_filled(0, 0, 1024, 768, (0, 0, 0, 192))
            self.shop_background_sprites.draw()
            self.shop_sprites.draw()
            self.shop_manager.draw()
            arcade.draw_text(
                format_number(self.data["leaf_count"]),
                x=464,
                y=552,
                font_name="Do Hyeon",
                font_size=20,
                anchor_x="right",
                anchor_y="center",
            )
        elif self.planting is not None:
            arcade.draw_sprite(self.planting_sprite, alpha=128)

    def on_update(self, delta_time: float):
        self.grow_plants()

        if self.needs_render:
            self.update_plant_sprites()
            save_game_data(self.data)
            self.needs_render = False

    def grow_plants(self):
        current_time = time.time()
        for plant_list in self.data["plants"]:
            for plant in plant_list:
                if plant is not None:
                    if plant["growth_stage"] == 0:
                        elapsed = current_time - plant["last_stage_time"]
                        time_to_grow_adult = plants[plant["type"]]["time_to_grow_adult"]
                        if elapsed >= time_to_grow_adult:
                            time_to_grow_leaves = plants[plant["type"]][
                                "time_to_grow_leaves"
                            ]
                            if elapsed >= time_to_grow_adult + time_to_grow_leaves:
                                plant["growth_stage"] = 2
                                plant["last_stage_time"] = current_time
                            else:
                                plant["growth_stage"] = 1
                                plant["last_stage_time"] = (
                                    plant["last_stage_time"] + time_to_grow_adult
                                )
                            self.needs_render = True
                    elif plant["growth_stage"] == 1:
                        elapsed = current_time - plant["last_stage_time"]
                        time_to_grow_leaves = plants[plant["type"]][
                            "time_to_grow_leaves"
                        ]
                        if elapsed >= time_to_grow_leaves:
                            plant["growth_stage"] = 2
                            plant["last_stage_time"] = current_time
                            self.needs_render = True

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int
    ):
        if not self.in_shop and self.planting is None:
            self.camera.position = (
                max(512, min(self.camera.position.x - dx, 1536)),
                max(384, min(self.camera.position.y - dy, 1152)),
            )

    def on_mouse_motion(self, x, y, dx, dy):
        if self.planting is not None:
            self.planting_sprite.position = (x, y)
        elif not self.in_shop:
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
        if self.in_shop:
            if not self.shop_background.collides_with_point((x, y)):
                self.in_shop = False
                self.shop_manager.disable()
        elif self.planting is not None:
            (world_x, world_y, _) = self.camera.unproject((x, y))
            for index, plant in enumerate(
                [self.plains_plants, self.water_plants, self.savannah_plants][
                    self.planting[1]
                ]
            ):
                if plant.collides_with_point((world_x, world_y)):
                    self.data["plants"][self.planting[1]][index] = {
                        "type": self.planting[0],
                        "growth_stage": 0,
                        "last_stage_time": time.time(),
                    }
                    self.data["leaf_count"] -= plants[self.planting[0]]["price"]
                    self.needs_render = True
                    self.planting = None
                    return
        else:
            (world_x, world_y, _) = self.camera.unproject((x, y))
            if self.shop.collides_with_point((world_x, world_y)):
                self.in_shop = True
                self.shop_buy_button.disabled = (
                    self.data["leaf_count"] < plants[self.current_plant_index]["price"]
                )
                self.shop_manager.enable()
            for list_index, plant_list in enumerate(
                [self.plains_plants, self.water_plants, self.savannah_plants]
            ):
                for index, plant in enumerate(plant_list):
                    if plant.collides_with_point((world_x, world_y)):
                        plant_data = self.data["plants"][list_index][index]
                        if plant_data is not None and plant_data["growth_stage"] == 2:
                            plant_data["growth_stage"] = 1
                            self.data["leaf_count"] += plants[plant_data["type"]][
                                "yield"
                            ]
                            plant_data["last_stage_time"] = time.time()
                            self.needs_render = True
                        return

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE and self.planting is not None:
            self.planting = None
