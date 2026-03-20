import pyglet

from game.resources import resources
from game.scene import SceneManager
from game.scenes.loading import LoadingScene

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "PyGarden")
        self.set_icon(resources["leaf"])

        self.scene_manager = SceneManager(self)
        self.scene_manager.load(LoadingScene())

        self.player = pyglet.media.Player()
        self.player.queue(resources["soundtrack_1"])
        self.player.play()

    def on_draw(self):
        self.clear()

        self.scene_manager.draw()

        """


    def on_mouse_motion(self, x, y, dx, dy):
        world_x, world_y = self.camera.screen_to_world(x, y)
        hovered = None
        for sprite in self.interactive_sprites:
            if sprite.hit_test(world_x, world_y):
                hovered = sprite
                break
        if hovered != self.hovered:
            if self.hovered is not None:
                self.hovered.on_hover_end()
            if hovered is not None:
                hovered.on_hover_start()
            self.hovered = hovered

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.camera.x = max(0, min(self.camera.x - dx, 1024))
            self.camera.y = max(0, min(self.camera.y - dy, 768))

    def on_mouse_press(self, x, y, button, modifiers):
        world_x, world_y = self.camera.screen_to_world(x, y)
        for sprite in self.interactive_sprites:
            if sprite.hit_test(world_x, world_y):
                sprite.on_mouse_press(x, y, button, modifiers)
                break
                """
