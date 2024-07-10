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

        self.player_projectile_group = pygame.sprite.Group()
        self.enemy_projectile_group = pygame.sprite.Group()

        self.player = PlayerTank(self.player_projectile_group)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.enemy = Enemy(self.screen, self.enemy_projectile_group, self.player)
        self.enemies_group = pygame.sprite.Group(self.enemy)              
        
    def events(self):
        for event in pygame.event.get():
            esc = pygame.key.get_pressed()         
            if esc[K_ESCAPE] or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def collisions(self):
        # Collision - player > enemies triggers a 2 second invulnerability window
        if pygame.sprite.spritecollideany(self.player, self.enemies_group) or pygame.sprite.spritecollide(self.player, self.enemy_projectile_group, True):
            current_time = time.time()
            if current_time - self.player.last_hit_time > self.player.invulnerability_duration:
                #self.player.decrease_health()
                self.player.last_hit_time = current_time                

        # Collision - player projectiles > enemies + delete any projectile hitting an enemy
        for projectile in self.player_projectile_group.sprites():
            if pygame.sprite.spritecollideany(projectile, self.enemies_group):
                projectile.kill()

    def update(self):
        self.collisions()

        self.player_group.update(self.screen)
        self.player_projectile_group.update()
        self.player.shoot(self.player_projectile_group)

        self.enemy.update()
        self.enemy_projectile_group.update()

    def draw(self):
        self.screen.fill(WHITE)

        self.player_group.draw(self.screen)
        self.player_projectile_group.draw(self.screen)

        self.enemies_group.draw(self.screen)
        self.enemy_projectile_group.draw(self.screen)

        pygame.display.update()

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()