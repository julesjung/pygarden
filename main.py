import pygame

screen = pygame.display.set_mode((640, 480), 0)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  pygame.display.update()