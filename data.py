import json
import os

from platformdirs import user_data_dir


def get_save_file():
    local_data_path = os.path.join(os.getcwd(), "data")

    if os.path.isdir(local_data_path):
        return os.path.join(local_data_path, "save.json")
    else:
        save_dir = user_data_dir("PyGarden", appauthor=False)
        os.makedirs(save_dir, exist_ok=True)
        return os.path.join(save_dir, "save.json")


def load_game():
    with open(get_save_file(), "r") as file:
        return json.load(file)
