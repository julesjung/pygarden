import random

import pyglet


class MusicPlayer(pyglet.media.Player):
    def __init__(self) -> None:
        super().__init__()

        tracks = [
            pyglet.media.load("assets/music/soundtrack_1.mp3"),
            pyglet.media.load("assets/music/soundtrack_2.mp3"),
            pyglet.media.load("assets/music/soundtrack_3.mp3"),
            pyglet.media.load("assets/music/soundtrack_4.mp3"),
        ]

        random.shuffle(tracks)

        self.queue(tracks)
        self.loop = True
