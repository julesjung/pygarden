""" import arcade

from game.views.game_view import GameView
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    window.run() """

import pickle

def main():
    with open("game_data.pkl", "rb") as data:
        print(pickle.load(data))

if __name__ == "__main__":
    main()
