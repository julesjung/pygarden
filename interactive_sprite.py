import pyglet

_image_cache = {}


class InteractiveSprite(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_image_rgba(self):
        image = self.image
        if image in _image_cache:
            return _image_cache[image]
        data = image.get_image_data()
        width, height = (
            image.width,
            image.height,
        )
        rgba = data.get_data("RGBA", width * 4)
        _image_cache[image] = (width, height, rgba)
        return _image_cache[image]

    def _is_over_bounding_box(self, world_x, world_y):
        left = self.x
        bottom = self.y
        right = self.x + self.width
        top = self.y + self.height

        return left <= world_x < right and bottom <= world_y < top

    def _world_to_sprite(self, world_x, world_y):
        sprite_x = int(world_x - self.x)
        sprite_y = int(world_y - self.y)
        return sprite_x, sprite_y

    def _pixel_alpha_at(self, sprite_x, sprite_y):
        width, height, rgba = self._get_image_rgba()
        return rgba[
            (int(sprite_y / self.scale * width) + int(sprite_x / self.scale)) * 4 + 3
        ]

    def hit_test(self, world_x, world_y):
        if not self._is_over_bounding_box(world_x, world_y):
            return False

        sprite_x, sprite_y = self._world_to_sprite(world_x, world_y)

        alpha = self._pixel_alpha_at(sprite_x, sprite_y)

        if alpha > 0:
            return True
        return False

    def on_hover_start(self):
        self.dispatch_event("on_hover_start")

    def on_hover_end(self):
        self.dispatch_event("on_hover_end")

    def on_mouse_press(self, x, y, button, modifiers):
        self.dispatch_event("on_mouse_press", x, y, button, modifiers)


InteractiveSprite.register_event_type("on_hover_start")
InteractiveSprite.register_event_type("on_hover_end")
InteractiveSprite.register_event_type("on_mouse_press")
