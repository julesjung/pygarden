import pyglet
from .game import Game


if __name__ == "__main__":
    window = Game()
    player = pyglet.media.Player()
    player.queue(resources["SoundTrack#1"])
    player.play()
    pyglet.app.run()
