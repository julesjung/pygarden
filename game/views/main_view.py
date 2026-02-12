import arcade
import arcade.gui
from game.views.game_view import GameView


class MainView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.CAMEL

        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        play_button = self.manager.add(arcade.gui.UIFlatButton(text="Play"))

        @play_button.event("on_click")
        def play_button_on_click(event):
            game_view = GameView()
            self.window.show_view(game_view)
        
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=play_button,
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.CAMEL)
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        self.manager.draw()