import pygame

BASE_IMG_PATH = "assets/images/"

def load_image(path):
    image = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return image