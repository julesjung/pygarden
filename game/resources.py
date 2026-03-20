import pyglet

pyglet.resource.path = ["assets"]
pyglet.resource.reindex()


def load_image(path: str) -> pyglet.image.Texture:
    return pyglet.resource.image(path)


def load_spritesheet(path: str, rows: int, columns: int) -> pyglet.image.ImageGrid:
    image = pyglet.resource.image(path)
    return pyglet.image.ImageGrid(image, rows, columns)


def load_music(path: str) -> pyglet.media.Source:
    return pyglet.resource.media(path)


resources = {
    "tree": load_spritesheet("plants/tree.png", 1, 3),
    "pine_tree": load_spritesheet("plants/pine_tree.png", 1, 3),
    "bonzai_tree": load_spritesheet("plants/bonzai_tree.png", 1, 3),
    "fruit": load_image("collectibles/fruit.png"),
    "leaf": load_image("collectibles/leaf.png"),
    "leaf_counter": load_image("gui/count.png"),
    "shop": load_image("shop.png"),
    "soundtrack_1": load_music("music/soundtrack_1.mp3"),
}
