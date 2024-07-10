import math

import pygame

from helper_functions import load_image

class Enemy(pygame.sprite.Sprite):
    def __init__(self, surface, enemy_projectile_group, player_position):
        super().__init__()
        self.surface = surface
        self.image = load_image("enemies/player_tank.png")
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)
        self.enemy_projectile_group = enemy_projectile_group
        self.player_position = player_position
        self.last_shot_time = 0
        self.fireball_interval = 2 # seconds

    def cast_fireball(self):
        current_time = pygame.time.get_ticks() / 500
        if current_time - self.last_shot_time > self.fireball_interval:
            fireball = Fireball(self.rect.center, self.player_position.rect.center)
            self.enemy_projectile_group.add(fireball)
            self.last_shot_time = current_time

    def update(self):
        self.surface.blit(self.image, self.rect)
        self.cast_fireball()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, enemy_position, player_position):
        super().__init__()
        self.original_image = load_image("enemies/enemy_fireball.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = enemy_position
        self.velocity = 3
        # Calculate player position
        direction_vector = pygame.math.Vector2(player_position) - pygame.math.Vector2(enemy_position)
        self.direction = direction_vector.normalize()
        # Rotate the image based on the shooting direction
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x)) + 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.center += self.direction * self.velocity
