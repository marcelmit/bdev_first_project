import pygame
from pygame.locals import *

from helper_functions import load_image

class PlayerTank():
    def __init__(self):
        super().__init__()
        self.image = load_image("player/player_tank.png")
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)  

    def update(self, surface):
        surface.blit(self.image, self.rect)
        PlayerTank.move(self)
