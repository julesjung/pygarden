from pyglet.window import Window


class Scene:
    def __init__(self, window: Window):
        self.window = window

    def on_enter(self):
        self.window.push_handlers(self)

    def on_exit(self):
        self.window.push_handlers(self)

    def draw(self):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass
