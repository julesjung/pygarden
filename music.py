import random

from pyglet.media import Player

from resources import resources


class MusicPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

        tracks = [
            resources["soundtrack_1"],
            resources["soundtrack_2"],
            resources["soundtrack_3"],
            resources["soundtrack_4"],
        ]

        random.shuffle(tracks)

        self.queue(tracks)
        self.loop = True
