import pygame
from pygame.locals import *

from helper_functions import load_menu_image

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, image, size, position, text=None):
        super().__init__()
        self.main_font = pygame.font.SysFont("cambria", 50)
        
        self.original_image = load_menu_image(image)
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=(position))

        self.original_text = text
        self.text = self.main_font.render(self.original_text, True, "white")
        self.text_rect = self.text.get_rect(center=(position))

    def update(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

    def change_color(self, mouse_position):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.main_font.render(self.original_text, True, "green")

    def mouse_input(self, mouse_position):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return
