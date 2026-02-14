import arcade
import random
from game.sprites import Tree


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.camera = None
        self.tree_list = None
        self.hovered_tree = None

    def setup(self):
        self.camera = arcade.Camera2D()
        self.tree_list = arcade.SpriteList(use_spatial_hash=True)

        for y in reversed(range(4)):
            for x in range(4):
                tree = Tree(random.choice(["tree", "pine_tree"]))
                tree.position = (x * 128 + y * 64, y * 128)
                self.tree_list.append(tree)

    def on_draw(self):
        self.clear()

        self.camera.use()

        original_scale = None

        if self.hovered_tree:
            original_scale = self.hovered_tree.scale
            self.hovered_tree.multiply_scale(1.1)

        self.tree_list.draw()

        if self.hovered_tree:
            self.hovered_tree.scale = original_scale

    def on_update(self, delta_time):
        self.tree_list.update()

    def on_mouse_motion(self, x, y, dx, dy):
        world_coordinate = self.camera.unproject((x, y))
        world_x, world_y = world_coordinate[0], world_coordinate[1]
        hits = arcade.get_sprites_at_point((world_x, world_y), self.tree_list)
        self.hovered_tree = (
            sorted(hits, key=lambda hit: hit.position[1] - hit.position[0] * 0.5)[0]
            if hits
            else None
        )

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.camera.position -= (dx, dy)
