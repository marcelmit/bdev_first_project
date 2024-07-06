import pygame

BASE_IMG_PATH = "assets/images/"

def load_image(path):
    image = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return image

# Rotate image based on movement direction
def rotate_image(image, direction):
    if direction == "up":
        return image
    elif direction == "down":
        return pygame.transform.rotate(image, 180)
    elif direction == "left":
        return pygame.transform.rotate(image, 90)
    elif direction == "right":
        return pygame.transform.rotate(image, -90)
    elif direction == "up_left":
        return pygame.transform.rotate(image, 45)
    elif direction == "down_left":
        return pygame.transform.rotate(image, 135)
    elif direction == "up_right":
        return pygame.transform.rotate(image, -45)
    elif direction == "down_right":
        return pygame.transform.rotate(image, -135)