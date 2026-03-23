from pyglet import gl
from pyglet.graphics import Group


class ScissorGroup(Group):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_state(self):
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(self.x, self.y, self.width, self.height)

    def unset_state(self):
        gl.glDisable(gl.GL_SCISSOR_TEST)
