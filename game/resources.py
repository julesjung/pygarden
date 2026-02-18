import pyglet

pyglet.resource.path = ["assets"]
pyglet.resource.reindex()


def load_image(path: str) -> pyglet.image.Texture:
    return pyglet.resource.image(path)


def load_spritesheet(path: str, rows: int, columns: int) -> pyglet.image.ImageGrid:
    image = pyglet.resource.image(path)
    return pyglet.image.ImageGrid(image, rows, columns)


resources = {
    "tree": load_spritesheet("plants/tree.png", 1, 2),
    "pine_tree": load_spritesheet("plants/pine_tree.png", 1, 2),
    "fruit": load_image("collectibles/fruit.png"),
    "leaf": load_image("collectibles/leaf.png"),
}
