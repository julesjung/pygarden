from game.interactive_sprite import InteractiveSprite


class Shop(InteractiveSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = 0.5

    def on_hover_start(self):
        self.color = (255, 200, 200)

    def on_hover_end(self):
        self.color = (255, 255, 255)
