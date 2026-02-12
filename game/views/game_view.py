import arcade


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.scene = arcade.Scene()

        self.tree_sprite = arcade.Sprite("game/assets/plants/tree/tree.png", 2)
        self.tree_sprite.position = (640, 360)
        self.scene.add_sprite("Tree", self.tree_sprite)

    def on_draw(self):
        self.clear()

        self.scene.draw()
