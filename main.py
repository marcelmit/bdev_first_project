import sys
import time

import pygame
from pygame.locals import *
from enum import Enum

from player import PlayerTank
from enemies import Enemy
from ui_elements import MenuButton

WHITE = (255, 255, 255)

class GameState(Enum):
    MENU = 0
    GAMEPLAY = 1
    GAME_OVER = 2

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tank Game")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.current_state = GameState.MENU

        self.player_projectile_group = pygame.sprite.Group()
        self.enemy_projectile_group = pygame.sprite.Group()
        self.firewall_group = pygame.sprite.Group()

        self.player = PlayerTank(self.player_projectile_group)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.enemy = Enemy(self.screen, self.enemy_projectile_group, self.player, self.firewall_group)
        self.enemies_group = pygame.sprite.Group(self.enemy)
        
    def events(self):
        mouse_position = pygame.mouse.get_pos()
        esc = pygame.key.get_pressed()         
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and self.exit_button.rect.collidepoint(mouse_position) or event.type == pygame.QUIT or esc[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and self.play_button.rect.collidepoint(mouse_position):
                self.current_state = GameState.GAMEPLAY

    def collisions(self):
        current_time = time.time()
        # Collision - player > enemies triggers a 2 second invulnerability window
        if pygame.sprite.spritecollideany(self.player, self.enemies_group) or pygame.sprite.spritecollide(self.player, self.enemy_projectile_group, True):
            current_time = time.time()
            if current_time - self.player.last_hit_time > self.player.invulnerability_duration:
                self.player.decrease_health()
                self.player.last_hit_time = current_time           

        # Collision - player projectiles > enemies + delete any projectile hitting an enemy
        for projectile in self.player_projectile_group.sprites():
            if pygame.sprite.spritecollideany(projectile, self.enemies_group):
                projectile.kill()

        # Collision - player > firewall
        for firewall in self.firewall_group:
            if pygame.sprite.spritecollideany(self.player, firewall.collision_tiles):
                if current_time - self.player.last_hit_time > self.player.invulnerability_duration:
                    self.player.decrease_health()
                    self.player.last_hit_time = current_time

    def update(self):
        if self.current_state == GameState.GAMEPLAY:
            self.collisions()

            self.player_group.update(self.screen)
            self.player_projectile_group.update()
            self.player.shoot(self.player_projectile_group)

            self.enemy.update()
            self.enemy_projectile_group.update()
            self.firewall_group.update()

    def render(self):
        if self.current_state == GameState.MENU:
            self.render_menu()
        elif self.current_state == GameState.GAMEPLAY:
            self.render_gameplay()

        pygame.display.update()

    def render_menu(self):
        self.screen.fill(WHITE)

        main_menu_background = MenuButton("Box_Square", size=(500, 400), position=(960, 540))
        main_menu_background.update(self.screen)

        self.play_button = MenuButton("Button_Square", size=(250, 100), position=(960, 430), text="Play")
        self.play_button.change_color(pygame.mouse.get_pos())
        self.play_button.update(self.screen)

        self.options_button = MenuButton("Button_Square", size=(250, 100), position=(960, 545), text="Options")
        self.options_button.change_color(pygame.mouse.get_pos())
        self.options_button.update(self.screen)

        self.exit_button = MenuButton("Button_Square", size=(250, 100), position=(960, 660), text="Exit")
        self.exit_button.change_color(pygame.mouse.get_pos())
        self.exit_button.update(self.screen)

    def render_gameplay(self):
        self.screen.fill(WHITE)

        self.player_group.draw(self.screen)
        self.player_projectile_group.draw(self.screen)

        self.enemies_group.draw(self.screen)
        self.enemy_projectile_group.draw(self.screen)
        for firewall in self.firewall_group:
            firewall.draw(self.screen)

    def run(self):
        while True:
            self.events()
            self.update()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()