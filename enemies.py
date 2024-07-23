import math
import random

import pygame

from helper_functions import load_image

class Enemy(pygame.sprite.Sprite):
    def __init__(self, surface, enemy_projectile_group, player_position, firewall_group):
        super().__init__()
        self.surface = surface
        self.image = load_image("enemies/player_tank")
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)
        self.enemy_projectile_group = enemy_projectile_group
        self.firewall_group = firewall_group
        self.player_position = player_position
        self.max_health = 1000
        self.health = 500
        # Fireball
        self.fireball_last_shot_time = 0
        self.fireball_interval = 2
        # Firewall
        self.firewall_last_shot_time = 0
        self.firewall_interval = 2

    def cast_fireball(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.fireball_last_shot_time > self.fireball_interval:
            fireball = Fireball(self.rect.center, self.player_position.rect.center)
            self.enemy_projectile_group.add(fireball)
            self.fireball_last_shot_time = current_time

    def cast_firewall(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.firewall_last_shot_time > self.firewall_interval:
            firewall = Firewall()
            self.firewall_group.add(firewall)
            self.firewall_last_shot_time = current_time

    def update(self):
        self.surface.blit(self.image, self.rect)
        self.cast_fireball()
        self.cast_firewall()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, enemy_position, player_position):
        super().__init__()
        self.original_image = load_image("enemies/enemy_fireball")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = enemy_position
        self.velocity = 6
        # Calculate player position
        direction_vector = pygame.math.Vector2(player_position) - pygame.math.Vector2(enemy_position)
        self.direction = direction_vector.normalize()
        # Rotate the image based on the shooting direction
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x)) + 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.center += self.direction * self.velocity

class Firewall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tile_width = 79
        self.velocity = 6
        self.start_position = [0, 0]
        self.empty_position = [0, 0]
        self.wall_tiles = []
        self.empty_tile_image = load_image("enemies/enemy_fireball")
        self.rect = pygame.Rect(self.start_position[0], self.start_position[1], 0, 0) # Dummy rect for collisions
        self.collision_tiles = pygame.sprite.Group()
        # Create random gaps towrds the center of the wall
        self.empty_wall_tiles_list = list(range(5, 20))
        self.empty_wall_tiles = random.sample(self.empty_wall_tiles_list, k=4)

        for i in range(25):
            if i in self.empty_wall_tiles:
                continue
            else:
                tile_image = load_image("enemies/enemy_firewall")
                tile_rect = tile_image.get_rect()
                tile_rect.topleft = (self.start_position[0] + i * self.tile_width, self.start_position[1])
                self.wall_tiles.append((tile_image, tile_rect))

            collision_tile = pygame.sprite.Sprite()
            collision_tile.image = tile_image
            collision_tile.rect = tile_rect
            self.collision_tiles.add(collision_tile)

    def update(self):
        for tile_image, tile_rect in self.wall_tiles:
            tile_rect.y += self.velocity
        
    def draw(self, surface):
        for tile_image, tile_rect in self.wall_tiles:
            surface.blit(tile_image, tile_rect)