import pygame

from helper_functions import load_image

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("enemies/player_tank.png")
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)

    def update(self, surface):
        surface.blit(self.image, self.rect)