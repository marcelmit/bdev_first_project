import pygame
from pygame.locals import *

from helper_functions import load_image, rotate_image

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = load_image("player/player_tank.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.direction = "up"

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        direction_changed = False
        new_direction = None
        direction_x = 0
        direction_y = 0
        
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            direction_y -= 5
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            direction_y += 5
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            direction_x -= 5
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            direction_x += 5

        self.rect.move_ip(direction_x, direction_y)

        if direction_x == 0 and direction_y < 0:
            new_direction = "up"
        elif direction_x == 0 and direction_y > 0:
            new_direction = "down"
        elif direction_x < 0 and direction_y == 0:
            new_direction = "left"
        elif direction_x > 0 and direction_y == 0:
            new_direction = "right"
        elif direction_x < 0 and direction_y < 0:
            new_direction = "up_left"
        elif direction_x < 0 and direction_y > 0:
            new_direction = "down_left"
        elif direction_x > 0 and direction_y < 0:
            new_direction = "up_right"
        elif direction_x > 0 and direction_y > 0:
            new_direction = "down_right"
        
        # Update direction if changed
        if new_direction and new_direction != self.direction:
            self.direction = new_direction
            direction_changed = True
        
        # Rotate image if direction changed
        if direction_changed:
            self.image = rotate_image(self.original_image, self.direction)

    def update(self, surface):
        surface.blit(self.image, self.rect)
        PlayerTank.move(self)
