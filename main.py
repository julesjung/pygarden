import arcade

from game.views import MainMenuView
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = MainMenuView()
    window.show_view(game)
    window.run()


if __name__ == "__main__":
    main()
