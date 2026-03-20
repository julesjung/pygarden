class Scene:
    def __init__(self):
        self.manager = None

    def on_enter(self):
        pass

    def draw(self):
        pass


class SceneManager:
    def __init__(self, window):
        self.window = window
        self.scene = None

    def load(self, scene: Scene):
        self.scene = scene
        self.scene.manager = self
        self.scene.on_enter()

    def draw(self):
        if self.scene:
            self.scene.draw()
