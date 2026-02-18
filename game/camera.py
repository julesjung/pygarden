from pyglet.math import Vec3, Mat4


class Camera:
    def __init__(self, window):
        self.window = window
        self.x = 0
        self.y = 0
        self._previous_view = None

    def __enter__(self):
        self._previous_view = self.window.view
        self.window.view = Mat4.from_translation(Vec3(-self.x, -self.y, 0))

    def __exit__(self, type, value, traceback):
        self.window.view = self._previous_view

    def screen_to_world(self, x, y):
        return (x + self.x, y + self.y)

    def world_to_screen(self, x, y):
        return (x - self.x, y - self.y)
