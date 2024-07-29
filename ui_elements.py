import random

import pygame
from pygame.locals import *

from helper_functions import load_image

class Button():
    def __init__(self, image, position, size, text=None, text_position=None, interactive=False):
        self.main_font = pygame.font.SysFont("cambria", 50)
        self.mouse_position = pygame.mouse.get_pos()
        self.interactive = interactive
        
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=(position))

        self.text = text
        self.original_text = self.text
        if text and text_position:
            self.text = self.main_font.render(self.original_text, True, "white")
            self.text_rect = self.text.get_rect(center=(text_position))
        elif text:
            self.text = self.main_font.render(self.original_text, True, "white")
            self.text_rect = self.text.get_rect(center=(position))

    def update(self, surface):
        if self.interactive == True:
            self.change_color(self.mouse_position)

        surface.blit(self.image, self.rect)
        if self.text and self.text_rect:
            surface.blit(self.text, self.text_rect)

    def change_color(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            self.text = self.main_font.render(self.original_text, True, "green")
        else:
            self.text = self.main_font.render(self.original_text, True, "white")

    def mouse_input(self):
        return self.rect.collidepoint(self.mouse_position)

class HealthBar():
    def __init__(self, image, position, size, text=None, text_position=None):
        self.main_font = pygame.font.SysFont("cambria", 35)

        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=(position))
        self.rect.left = position[0]

        self.text = text
        self.original_text = self.text
        if text and text_position:
            self.text = self.main_font.render(self.original_text, True, "white")
            self.text_rect = self.text.get_rect(center=(text_position))

    def update(self, surface):
        surface.blit(self.image, self.rect)
        if self.text and self.text_rect:
            surface.blit(self.text, self.text_rect)   

class Cloud(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        rnd = random.randint(1, 8)
        image_path = f"ui/cloud{rnd}"

        self.original_image = load_image(image_path)
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.x += 2
        if self.rect.right > 2250:
            self.kill()

class CloudSpawner:
    def __init__(self, cloud_group):
        self.cloud_group = cloud_group
        self.create_initial_clouds(12)

        self.last_cloud = 0
        self.cloud_cooldown = 3

    def create_initial_clouds(self, count):
        step = 1980 // count
        for i in range(count):
            x_position = step * i + random.randint(- 50, 50)
            position = (x_position, random.randint(0, 200))
            size = (random.randint(50, 100), random.randint(25, 50))
            cloud = Cloud(position, size)
            self.cloud_group.add(cloud)

    def add_cloud(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_cloud > self.cloud_cooldown:
            position = (- 50, random.randint(0, 200))
            size = (random.randint(50, 100), random.randint(25, 50))
            cloud = Cloud(position, size)
            self.cloud_group.add(cloud)
            self.last_cloud = current_time