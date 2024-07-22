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
            self.text = self.main_font.render(self.original_text, True, "black")
            self.text_rect = self.text.get_rect(center=(text_position))

    def update(self, surface):
        surface.blit(self.image, self.rect)
        if self.text and self.text_rect:
            surface.blit(self.text, self.text_rect)