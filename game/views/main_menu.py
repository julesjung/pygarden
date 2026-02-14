from arcade import View, set_background_color
from arcade.color import PASTEL_GREEN
from arcade.gui import UIManager, UIAnchorLayout
from arcade.resources import load_kenney_fonts
from game.views.game import GameView
from game.widgets.button import Button


class MainMenuView(View):
    def __init__(self):
        super().__init__()

        load_kenney_fonts()

        self.manager = UIManager()

        anchor = self.manager.add(UIAnchorLayout())

        play_button = self.manager.add(Button(text="Play"))

        @play_button.event("on_click")
        def play_button_on_click(event):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=play_button,
        )

    def on_show_view(self):
        set_background_color(PASTEL_GREEN)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        self.manager.draw()
