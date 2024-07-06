import sys

import pygame
from pygame.locals import *

from player import PlayerTank

WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tank Game")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = PlayerTank()

    def run(self):
        while True:
            self.screen.fill((WHITE))
            for event in pygame.event.get():
                esc = pygame.key.get_pressed()         
                if esc[K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update(self.screen)

            pygame.display.update()
            self.clock.tick(60)

Game().run()
            