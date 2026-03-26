import json
import os

from utils.path import BASE_DIR


def game_data_file():
    local_data_path = BASE_DIR / "data"

    os.makedirs(local_data_path, exist_ok=True)
    return local_data_path / "game.json"


def game_exists():
    return os.path.exists(game_data_file())


def default_game_data():
    return {
        "leaf_count": 100,
        "plants": [
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
        ],
    }


def load_game_data():
    with open(game_data_file(), "r") as file:
        return json.load(file)


def save_game_data(data):
    with open(game_data_file(), "w") as file:
        json.dump(data, file)
