import pygame
from pygame.locals import *

screen = pygame.display.set_mode((640, 480), 0)

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()

  pygame.display.update()