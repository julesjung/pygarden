_image_cache = {}


def _get_image_rgba(sprite):
    image = sprite.image
    if image in _image_cache:
        return _image_cache[image]
    data = image.get_image_data()
    width, height = image.width, image.height
    rgba = data.get_data("RGBA", width * 4)
    _image_cache[image] = (width, height, rgba)
    return _image_cache[image]


def _is_over_bounding_box(sprite, world_x, world_y):
    left = sprite.x
    bottom = sprite.y
    right = sprite.x + sprite.width
    top = sprite.y + sprite.height

    return left <= world_x < right and bottom <= world_y < top


def _world_to_sprite(sprite, world_x, world_y):
    sprite_x = int(world_x - sprite.x)
    sprite_y = int(world_y - sprite.y)
    return sprite_x, sprite_y


def _pixel_alpha_at(sprite, sprite_x, sprite_y):
    width, height, rgba = _get_image_rgba(sprite)
    return rgba[(sprite_y * width + sprite_x) * 4 + 3]


def pick_sprite_under_point(sprites, world_x, world_y):
    for sprite in sorted(sprites, key=lambda sprite: sprite.y):
        if not _is_over_bounding_box(sprite, world_x, world_y):
            continue

        sprite_x, sprite_y = _world_to_sprite(sprite, world_x, world_y)
        alpha = _pixel_alpha_at(sprite, sprite_x, sprite_y)
        if alpha > 0:
            return sprite
    return None
