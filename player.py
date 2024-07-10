import pygame
from pygame.locals import *

from helper_functions import load_image, rotate_image

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, player_projectile_group):
        super().__init__()
        self.original_image = load_image("player/player_tank.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)
        self.player_projectile_group = player_projectile_group
        self.direction = "up"
        self.health = 5
        # "Cooldown" for the shoot method
        self.last_shot_time = 0
        self.shoot_delay = 500
        # Player Invulnerability Duration after taking Damage
        self.invulnerability_duration = 2
        self.last_hit_time = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        direction_changed = False
        new_direction = None
        direction_x, direction_y = 0, 0
        
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

    def shoot(self, player_projectile_group, is_rocket=False):
        pressed_keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Create two bullets
        if pressed_keys[K_q] and current_time - self.last_shot_time > self.shoot_delay:
            offset_x, offset_y = 0, 0
            bullet_direction = self.direction

            if self.direction == "up":
                offset_x, offset_y = 8, -40
            elif self.direction == "down":
                offset_x, offset_y = 8, 40
            elif self.direction == "left":
                offset_x, offset_y = -35, 7
            elif self.direction == "right":
                offset_x, offset_y = 40, 15
            elif self.direction == "up_left":
                offset_x, offset_y = 8, -40
                bullet_direction = "up_left"
            elif self.direction == "down_left":
                offset_x, offset_y = -35, 7
                bullet_direction = "down_left"
            elif self.direction == "up_right":
                offset_x, offset_y = 8, -40
                bullet_direction = "up_right"
            elif self.direction == "down_right":
                offset_x, offset_y = 45, 7
                bullet_direction = "down_right"

            if self.direction == "up":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x, self.rect.centery + offset_y, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx - offset_x, self.rect.centery + offset_y, bullet_direction)
            elif self.direction == "down":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x, self.rect.centery + offset_y, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx - offset_x, self.rect.centery + offset_y, bullet_direction)
            elif self.direction == "left":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x, self.rect.centery + offset_y - 22, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx + offset_x, self.rect.centery - offset_y + 8, bullet_direction)
            elif self.direction == "right":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x + 10, self.rect.centery + offset_y - 15, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx + offset_x + 10, self.rect.centery - offset_y, bullet_direction)
            elif self.direction == "up_left":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x - 25, self.rect.centery + offset_y + 25, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx - offset_x, self.rect.centery + offset_y + 15, bullet_direction)
            elif self.direction == "down_left":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x + 16, self.rect.centery + offset_y + 28, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx - offset_x - 42, self.rect.centery + offset_y + 38, bullet_direction)
            elif self.direction == "up_right":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x + 48, self.rect.centery + offset_y + 23, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx - offset_x + 53, self.rect.centery + offset_y + 12, bullet_direction)
            elif self.direction == "down_right":
                bullet1 = PlayerProjectile(self.rect.centerx + offset_x + 9, self.rect.centery + offset_y + 28, bullet_direction)
                bullet2 = PlayerProjectile(self.rect.centerx - offset_x + 89, self.rect.centery + offset_y + 40, bullet_direction)
            player_projectile_group.add(bullet1, bullet2)
            self.last_shot_time = current_time

        # create one rocket
        if pressed_keys[K_e] and current_time - self.last_shot_time > self.shoot_delay:
            if self.direction == "up":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery, self.direction, is_rocket=True)
            elif self.direction == "down":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery, self.direction, is_rocket=True)
            elif self.direction == "left":
                rocket = PlayerProjectile(self.rect.centerx + 5, self.rect.centery - 8, self.direction, is_rocket=True)
            elif self.direction == "right":
                rocket = PlayerProjectile(self.rect.centerx + 5, self.rect.centery - 8, self.direction, is_rocket=True)
            elif self.direction == "up_left":
                rocket = PlayerProjectile(self.rect.centerx + 17, self.rect.centery + 9, self.direction, is_rocket=True)
            elif self.direction == "down_left":
                rocket = PlayerProjectile(self.rect.centerx + 17, self.rect.centery + 9, self.direction, is_rocket=True)
            elif self.direction == "up_right":
                rocket = PlayerProjectile(self.rect.centerx + 17, self.rect.centery + 9, self.direction, is_rocket=True)
            elif self.direction == "down_right":
                rocket = PlayerProjectile(self.rect.centerx + 17, self.rect.centery + 9, self.direction, is_rocket=True)
            player_projectile_group.add(rocket)
            self.last_shot_time = current_time

    def decrease_health(self):
        self.health -= 1
        print(f"Invulnerable for {self.invulnerability_duration} seconds")
        print(f"{self.health} health left")
        # Game over if health reaches 0
        if self.health <= 0:
            self.kill()
            print("Game Over")

    def update(self, surface):
        self.move()
        surface.blit(self.image, self.rect)

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_rocket=False):
        super().__init__()
        if is_rocket:
            self.original_image = load_image("player/player_tank_rocket.png")
        else:
            self.original_image = load_image("player/player_tank_bullet.png")
        self.image = rotate_image(self.original_image, direction)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def move(self):
        direction_x, direction_y = 0, 0

        if self.direction == "up":
            direction_y -= 5
        elif self.direction == "down":
            direction_y += 5
        elif self.direction == "left":
            direction_x -= 5
        elif self.direction == "right":
            direction_x += 5
        elif self.direction == "up_left":
            direction_x, direction_y = -5, -5
        elif self.direction == "down_left":
            direction_x, direction_y = -5, 5
        elif self.direction == "up_right":
            direction_x, direction_y = 5, -5
        elif self.direction == "down_right":
            direction_x, direction_y = 5, 5

        self.rect.move_ip(direction_x, direction_y)

        # Remove the projectile if it moves off-screen
        if (self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or 
            self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height()):
            self.kill()

    def update(self):
        self.move()