import pygame
import random
from ..parts import player, cell, generate_maze, supply
from .. import tools, setup, constants as C


class Arena:
    def setup(self, player_num, score):
        self.finished = False
        self.player_num = player_num
        self.score = score
        self.next = 'arena'
        self.random = random.random()

        self.setup_states()
        self.setup_map()
        self.setup_players()
        self.setup_supplies()

    def setup_states(self):
        self.clock = 0
        self.can_pause = True
        self.pause = False
        self.ending = False
        self.ending_timer = 0
        self.celebrating = False
        self.celebrating_timer = 0

    def setup_map(self):
        self.cells = []
        self.map_surface = pygame.Surface((C.SCREEN_W, C.SCREEN_H)).convert()
        self.map_surface.fill(C.SCREEN_COLOR)

        generate_maze.predeal(self)
        generate_maze.Generage_Maze(self, 0, 0, C.COLUMN_NUM-1, C.ROW_NUM-1)

        for i in range(0, C.COLUMN_NUM*C.ROW_NUM):
            self.cells[i].draw_walls(self.map_surface)

    def setup_supplies(self):
        self.supply_num = 0
        self.supply_timer = 0
        self.last_supply_idx = -1
        self.supplies = pygame.sprite.Group()

    def setup_players(self):
        self.rest_player_num = self.player_num
        self.players = pygame.sprite.Group()

        vised = {}
        for i in range(3):
            if self.score[i] != -1:
                aplayer = player.player(i+1, self)
                x = int(random.random()*C.COLUMN_NUM)
                y = int(random.random()*C.ROW_NUM)
                while vised.get(generate_maze.get_idx(x, y), False):
                    x = int(random.random()*C.COLUMN_NUM)
                    y = int(random.random()*C.ROW_NUM)
                vised[generate_maze.get_idx(x, y)] = True
                aplayer.x = self.cells[generate_maze.get_idx(
                    x, y)].rect.centerx*C.MOTION_CALC_SCALE
                aplayer.y = self.cells[generate_maze.get_idx(
                    x, y)].rect.centery*C.MOTION_CALC_SCALE
                aplayer.theta = 2*C.PI*random.random()
                self.players.add(aplayer)

    def update_ending(self):
        if not self.ending and self.rest_player_num <= 1:
            self.ending = True
            self.ending_timer = self.clock
        if self.ending and self.clock-self.ending_timer >= C.ENDING_TIME:
            self.ending = False
            self.celebrating = True
            self.celebrating_timer = self.clock
            for aplayer in self.players:
                if not aplayer.dead:
                    aplayer.celebrate()

        if self.celebrating and self.clock-self.celebrating_timer >= C.CELEBRATING_TIME:
            for aplayer in self.players:
                if not aplayer.dead:
                    self.score = tuple(
                        self.score[i]+(aplayer.name-1 == i) for i in range(3))
            self.finished = True

    def draw_info(self, surface):
        surface.blit(tools.create_label('ESC  /  P', 28),
                     (C.SCREEN_W*0.11, C.SCREEN_H*0.9))
        if self.pause:
            surface.blit(tools.create_label('pause...', 28),
                         (C.SCREEN_W*0.215, C.SCREEN_H*0.9))
        if self.score[0] != -1:
            surface.blit(tools.create_label(str(self.score[0]), 32),
                         (C.SCREEN_W*0.46, C.SCREEN_H*0.9))
            surface.blit(tools.create_label('PLAYER1', 32),
                         (C.SCREEN_W*0.33, C.SCREEN_H*0.9))
        if self.score[1] != -1:
            surface.blit(tools.create_label(str(self.score[1]), 32),
                         (C.SCREEN_W*0.66, C.SCREEN_H*0.9))
            surface.blit(tools.create_label('PLAYER2', 32),
                         (C.SCREEN_W*0.53, C.SCREEN_H*0.9))
        if self.score[2] != -1:
            surface.blit(tools.create_label(str(self.score[2]), 32),
                         (C.SCREEN_W*0.86, C.SCREEN_H*0.9))
            surface.blit(tools.create_label('PLAYER3', 32),
                         (C.SCREEN_W*0.73, C.SCREEN_H*0.9))

    def update_states(self, keys):
        if keys[pygame.K_ESCAPE]:
            self.next = 'main_menu'
            self.finished = True

        if self.can_pause and keys[pygame.K_p]:
            self.pause = not self.pause

        if keys[pygame.K_p]:
            self.can_pause = False
        else:
            self.can_pause = True

    def update_supply(self):
        if self.supply_timer == 0:
            self.supply_timer = self.clock
        elif self.clock-self.supply_timer > C.SUPPLY_TIME and self.supply_num < 2:
            idx = int(self.random*C.COLUMN_NUM*C.ROW_NUM)
            while idx == self.last_supply_idx:
                idx = int(random.random()*C.COLUMN_NUM*C.ROW_NUM)
            self.last_supply_idx = idx
            self.supplies.add(supply.Supply(self.cells[idx].rect.center))
            self.supply_num += 1
            self.supply_timer = self.clock

        for asupply in self.supplies:
            for player in self.players:
                hitbox = pygame.sprite.spritecollide(
                    asupply, player.hitboxes, False)
                if hitbox:
                    setup.SOUNDS['pick'].play()
                    asupply.kill()
                    self.supply_num -= 1
                    self.supply_timer = self.clock
                    if asupply.type:
                        player.shotgun = True
                        player.biground = False
                    else:
                        player.biground = True
                        player.shotgun = False
                    return

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))
        self.draw_info(surface)
        self.supplies.draw(surface)

    def update(self, surface, keys):
        self.clock = pygame.time.get_ticks()
        self.random = random.random()
        self.draw_map(surface)

        if not self.pause and not self.celebrating:
            for aplayer in self.players:
                aplayer.update(keys)

            self.update_supply()

        if not self.pause:
            self.update_ending()

        if not self.celebrating:
            self.update_states(keys)

        for aplayer in self.players:
            aplayer.draw(surface)