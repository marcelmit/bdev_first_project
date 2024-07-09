import sys
import time

import pygame
from pygame.locals import *

from player import PlayerTank
from enemies import Enemy

WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tank Game")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()      
        self.player = PlayerTank()
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.rocket_group = pygame.sprite.Group()
        self.enemy = Enemy()
        self.enemies_group = pygame.sprite.Group()
        self.enemies_group.add(self.enemy)
        self.all_sprites_group = pygame.sprite.Group()
        self.all_sprites_group.add(self.player)

    def run(self):
        while True:
            self.screen.fill((WHITE))
            for event in pygame.event.get():
                esc = pygame.key.get_pressed()         
                if esc[K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player_group.update(self.screen)
            self.player.shoot(self.bullet_group, self.rocket_group)
            self.enemy.update(self.screen)
            self.bullet_group.draw(self.screen)
            self.bullet_group.update()
            self.rocket_group.draw(self.screen)
            self.rocket_group.update()

            # Collision - player > enemies triggers a 2 second invulnerability window
            if pygame.sprite.spritecollideany(self.player, self.enemies_group):
                current_time = time.time()
                if current_time - self.player.last_hit_time > self.player.invulnerability_duration:
                    self.player.decrease_health()
                    self.player.last_hit_time = current_time                
            # Collision player projectiles > enemies + delete any projectile hitting an enemy
            for projectile in self.bullet_group.sprites() + self.rocket_group.sprites():
                hits = pygame.sprite.spritecollideany(projectile, self.enemies_group)
                if hits:
                    projectile.kill()

            pygame.display.update()
            self.clock.tick(60)

Game().run()
            