from pyglet.math import Vec3, Mat4


class Camera:
    def __init__(self, window):
        self.window = window
        self.x = 0
        self.y = 0

    def use(self):
        self.window.view = Mat4.from_translation(Vec3(-self.x, -self.y, 0))

    def screen_to_world(self, x, y):
        return (x + self.x, y + self.y)

    def world_to_screen(self, x, y):
        return (x - self.x, y - self.y)
