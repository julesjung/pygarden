import pygame


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0)
        pygame.display.set_caption("PyGarden")
        self.running = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


if __name__ == "__main__":
    app = App()
    app.run()
