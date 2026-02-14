from arcade import Sprite, load_spritesheet
from random import random


TEXTURES = {
    "tree": load_spritesheet("game/assets/plants/tree.png").get_texture_grid(
        (256, 384), 2, 2
    ),
    "pine_tree": load_spritesheet("game/assets/plants/pine_tree.png").get_texture_grid(
        (256, 384), 2, 2
    ),
}


class Tree(Sprite):
    def __init__(self, tree_type, scale=1, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(None, scale, center_x, center_y, angle, **kwargs)

        self.tree_type = tree_type
        self.textures = TEXTURES[self.tree_type]

        self.set_texture(0)

        self.growth_timer = 0
        self.growth_stage = 0

        self.fully_grown = False

    def update(self, delta_time=1 / 60):
        if not self.fully_grown:
            self.growth_timer += delta_time * random()

            if self.growth_timer > 5:
                self.grow()
                self.growth_timer = 0

    def grow(self):
        self.set_texture(self.cur_texture_index + 1)
        if self.cur_texture_index > len(self.textures):
            self.fully_grown = True
