import sys
import time

import pygame
from pygame.locals import *
from enum import Enum

from player import PlayerTank
from enemies import Enemy
from ui_elements import Button, HealthBar

WHITE = (255, 255, 255)

class GameState(Enum):
    MENU = 0
    OPTIONS = 1
    GAMEPLAY = 2
    GAME_OVER = 3

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
        esc = pygame.key.get_pressed()         
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and self.exit_button.mouse_input() or event.type == pygame.QUIT or esc[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and self.options_button.mouse_input():
                self.current_state = GameState.OPTIONS
            elif event.type == MOUSEBUTTONDOWN and self.play_button.mouse_input():
                self.new_game()
            elif self.current_state == GameState.GAME_OVER and event.type == MOUSEBUTTONDOWN and self.retry_button.mouse_input():
                self.new_game()

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
        if self.player.health <= 0:
            self.current_state = GameState.GAME_OVER

        if self.current_state == GameState.MENU:
            self.render_menu()
        elif self.current_state == GameState.OPTIONS:
            self.render_options()
        elif self.current_state == GameState.GAMEPLAY:
            self.render_gameplay()
        elif self.current_state == GameState.GAME_OVER:
            self.render_game_over()

        pygame.display.update()

    def render_menu(self):
        self.screen.fill(WHITE)

        ui_elements = [
            Button("ui/Box_Square", position=(960, 540), size=(480, 400)),
            Button("ui/Button_Square", position=(960, 430), size=(240, 100), text="Play", interactive=True),
            Button("ui/Button_Square", position=(960, 545), size=(240, 100), text="Options", interactive=True),
            Button("ui/Button_Square", position=(960, 660), size=(240, 100), text="Exit", interactive=True),
            Button("ui/Box_Blue_Square", position=(360, 450), size=(360, 275), text="Move"),
            Button("ui/W", position=(360, 400), size=(50, 50)),
            Button("ui/Up", position=(360, 350), size=(50, 50)),
            Button("ui/S", position=(360, 500), size=(50, 50)),
            Button("ui/Down", position=(360, 550), size=(50, 50)),
            Button("ui/A", position=(265, 450), size=(50, 50)),
            Button("ui/Left", position=(215, 450), size=(50, 50)),
            Button("ui/D", position=(455, 450), size=(50, 50)),
            Button("ui/Right", position=(505, 450), size=(50, 50)),
            Button("ui/Box_Blue_Square", position=(360, 750), size=(400, 175), text="Shoot", text_position=(360, 700)),
            Button("ui/Space_Left", position=(200, 760), size=(50, 50)),
            Button("ui/Space_Middle", position=(250, 760), size=(50, 50), text="Bullet", text_position=(250, 810)),
            Button("ui/Space_Right", position=(300, 760), size=(50, 50)),
            Button("ui/CTRL_Left", position=(435, 760), size=(50, 50), text="Rocket", text_position=(450, 810)),
            Button("ui/CTRL_Right", position=(485, 760), size=(50, 50))
        ]
        
        for element in ui_elements:
            element.update(self.screen)

        self.play_button = ui_elements[1]
        self.options_button = ui_elements[2]
        self.exit_button = ui_elements[3]

    def render_options(self):
        self.screen.fill(WHITE)

        ui_elements = [
            Button("ui/Box_Square", position=(960, 540), size=(700, 700))
        ]

        for element in ui_elements:
            element.update(self.screen)

    def render_gameplay(self):
        self.screen.fill(WHITE)

        ui_elements = [
            Button("ui/Button_Square", position=(68, 925), size=(125, 60)), # Player ammo 
            Button("ui/Rocket_Icon", position=(38, 926), size=(40, 40), text=self.player.ammo, text_position=(90, 926)),
            Button("ui/Button_Square", position=(175, 1000), size=(345, 80)), # Player health bar
            HealthBar("ui/HP_Bar", position=(33, 1000), size=(290 * (self.player.health / self.player.max_health), 50)),
            HealthBar("ui/HP_Bar_Frame", position=(30, 1000), size=(300, 50), text=(f"{self.player.health}" + "/" + f"{self.player.max_health}"), text_position=(180, 1000)),
            HealthBar("ui/Heart_Icon", position=(14, 998), size=(55, 55)),
            Button("ui/Button_Square", position=(1590, 45), size=(640, 80)), # Enemy health bar
            HealthBar("ui/HP_Bar", position=(1300, 45), size=(590 * (self.enemy.health / self.enemy.max_health), 50)),
            HealthBar("ui/HP_Bar_Frame", position=(1300, 45), size=(590, 50), text=(f"{self.enemy.health}" + "/" + f"{self.enemy.max_health}"), text_position=(1605, 45)),
            HealthBar("ui/Heart_Icon", position=(1280, 47), size=(70, 70))
        ]

        for element in ui_elements:
            element.update(self.screen)

        self.player_group.draw(self.screen)
        self.player_projectile_group.draw(self.screen)

        self.enemies_group.draw(self.screen)
        self.enemy_projectile_group.draw(self.screen)
        for firewall in self.firewall_group:
            firewall.draw(self.screen)

    def render_game_over(self):
        self.screen.fill(WHITE)

        ui_elements = [
            Button("ui/Box_Square", position=(960, 540), size=(500, 400)),
            Button("ui/Button_Square", position=(568, 925), size=(125, 60), text="Retry", interactive=True),
            Button("ui/Button_Square", position=(568, 525), size=(125, 60), text="Exit", interactive=True),
            Button("ui/Button_Square", position=(68, 925), size=(125, 60))
        ]

        for element in ui_elements:
            element.update(self.screen)

        self.retry_button = ui_elements[1]
        self.exit_button = ui_elements[2]

    def new_game(self):
        self.player = PlayerTank(self.player_projectile_group)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemy = Enemy(self.screen, self.enemy_projectile_group, self.player, self.firewall_group)
        self.enemies_group = pygame.sprite.Group(self.enemy)
        self.player_projectile_group.empty()
        self.enemy_projectile_group.empty()
        self.firewall_group.empty()
        self.current_state = GameState.GAMEPLAY

    def run(self):
        while True:
            self.events()
            self.update()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()