import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0)
        pygame.display.set_caption("PyGarden")
        self.running = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            pygame.display.update()

    def quit(self):
        pygame.quit()
