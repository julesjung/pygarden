import json
import time

import arcade

from data import get_save_file
from music import MusicPlayer


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

        """
        self.shop_view = ShopView(self.window)
        self.in_shop = False

        @self.shop.event
        def on_mouse_press(x, y, buttons, modifiers):
            self.on_shop_press(x, y, buttons, modifiers)

        self.save_game()
        self.leaf_counter = LeafCounter(self.data["leaf_count"], 0, 0)
        """

    def on_draw(self):
        self.clear()

        with self.camera.activate():
            self.background_sprites.draw()
            self.foregroud_sprites.draw()

        self.overlay_sprites.draw()

        """
        self.leaf_counter.draw()

        if self.in_shop:
            self.shop_view.draw()
        """

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int
    ):
        self.camera.position = (
            max(512, min(self.camera.position.x - dx, 1536)),
            max(384, min(self.camera.position.y - dy, 1152)),
        )

    def on_mouse_motion(self, x, y, dx, dy):
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
        (world_x, world_y, _) = self.camera.unproject((x, y))
        for sprite in self.foregroud_sprites:
            if sprite.collides_with_point((world_x, world_y)):
                break

    def save_game(self):
        self.data["last_played"] = time.time()
        with open(get_save_file(), "w") as f:
            json.dump(self.data, f)

    """
    def on_shop_press(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.dispatch_event("open_shop")
    """
