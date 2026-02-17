from pyglet.math import Vec3, Mat4


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0

    def get_view_matrix(self):
        return Mat4.from_scale(Vec3(self.zoom, self.zoom, 1)) @ Mat4.from_translation(
            Vec3(-self.x, -self.y, 0)
        )
