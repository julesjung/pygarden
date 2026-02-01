import arcade


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.CAMEL

    def on_draw(self):
        self.clear()
