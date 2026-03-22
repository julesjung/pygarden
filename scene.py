class Scene:
    def __init__(self):
        self.manager = None

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def draw(self):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass


class SceneManager:
    def __init__(self, window):
        self.window = window
        self.scene = None

    def set_scene(self, scene: Scene):
        if self.scene is not None:
            self.scene.on_exit()
        self.scene = scene
        self.scene.manager = self
        self.scene.on_enter()

    def draw(self):
        if self.scene:
            self.scene.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.scene is not None:
            self.scene.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.scene is not None:
            self.scene.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.scene is not None:
            self.scene.on_mouse_press(x, y, button, modifiers)
