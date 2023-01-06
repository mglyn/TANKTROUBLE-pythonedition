import pygame
import numpy
import random
from .. import setup, tools, constants as C
from . import cell, shell


class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, theta, s, v, t, arena, player):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.theta = theta
        self.vx = v*C.BASE_ROUND_V*numpy.cos(self.theta)
        self.vy = v*C.BASE_ROUND_V*numpy.sin(self.theta)
        self.time = t*C.MAX_ROUND_TIME
        self.exist_timer = 0
        self.protection = True
        self.last_hit = None
        self.size = s
        self.arena = arena
        self.player = player
        self.load_image()

    def load_image(self):
        self.image = tools.get_image(
            setup.GRAPHICS['round'], 0, 0, C.ROUND_PX, C.ROUND_PY, C.WHITE, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x/C.MOTION_CALC_SCALE,
                            self.y/C.MOTION_CALC_SCALE)

    def update_collisions(self):
        if self.exist_timer == 0:
            self.exist_timer = self.player.arena.clock

        cells_idx = cell.calculate_cell_num(
            self.rect.center[0], self.rect.center[1])
        for i in range(0, 4):
            for wall in self.arena.cells[cells_idx[i]].walls:
                if pygame.sprite.collide_rect(self, wall):
                    if self.player.arena.clock-self.exist_timer >= self.time:
                        self.go_die()
                        return

                    if self.last_hit != None and self.last_hit is wall:
                        return
                    self.last_hit = wall
                    self.protection = False
                    if abs(wall.rect.top-self.rect.bottom) <= C.ROUND_COLLITION_EPS and self.vy > 0:
                        self.vy *= -1
                        return
                    if abs(wall.rect.bottom-self.rect.top) <= C.ROUND_COLLITION_EPS and self.vy < 0:
                        self.vy *= -1
                        return
                    if abs(wall.rect.right-self.rect.left) <= C.ROUND_COLLITION_EPS and self.vx < 0:
                        self.vx *= -1
                        return
                    if abs(wall.rect.left-self.rect.right) <= C.ROUND_COLLITION_EPS and self.vx > 0:
                        self.vx *= -1
                        return

    def update_hit(self):
        for aplayer in self.arena.players:
            if self.protection and aplayer is self.player:
                continue
            if abs(self.x-aplayer.x)/C.MOTION_CALC_SCALE > C.PLAYER_PX or abs(self.y-aplayer.y)/C.MOTION_CALC_SCALE > C.PLAYER_PX:
                continue
            hitbox = pygame.sprite.spritecollideany(
                self, aplayer.hitboxes)
            if hitbox:
                aplayer.go_die()
                self.go_die()
                return

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x/C.MOTION_CALC_SCALE,
                            self.y/C.MOTION_CALC_SCALE)
        self.update_collisions()
        self.update_hit()

    def go_die(self):
        self.player.round_num -= 1
        self.kill()


class Big_Shell(Shell):
    def __init__(self, x, y, theta, s, v, t, arena, player):
        Shell.__init__(self, x, y, theta, s, v, t, arena, player)

    def go_die(self):
        setup.SOUNDS['fire'+str(int(random.random()*4+1))].play()
        for i in range(30):
            self.player.rounds.add(Fragment(x=self.x, y=self.y, theta=random.random()*2*C.PI,
                                            s=0.7, v=1.5, t=0.05, arena=self.arena, player=self.player))
        self.kill()

    def update_collisions(self):
        if self.exist_timer == 0:
            self.exist_timer = self.player.arena.clock
        if self.player.arena.clock-self.exist_timer >= self.time:
            self.go_die()
            return
        cells_idx = cell.calculate_cell_num(
            self.rect.center[0], self.rect.center[1])
        for i in range(0, 4):
            for wall in self.arena.cells[cells_idx[i]].walls:
                if pygame.sprite.collide_rect(self, wall):
                    if self.last_hit != None and self.last_hit is wall:
                        return
                    self.last_hit = wall
                    self.protection = False
                    if abs(wall.rect.top-self.rect.bottom) <= C.ROUND_COLLITION_EPS and self.vy > 0:
                        self.vy *= -1
                        return
                    if abs(wall.rect.bottom-self.rect.top) <= C.ROUND_COLLITION_EPS and self.vy < 0:
                        self.vy *= -1
                        return
                    if abs(wall.rect.right-self.rect.left) <= C.ROUND_COLLITION_EPS and self.vx < 0:
                        self.vx *= -1
                        return
                    if abs(wall.rect.left-self.rect.right) <= C.ROUND_COLLITION_EPS and self.vx > 0:
                        self.vx *= -1
                        return


class Fragment(Shell):
    def __init__(self, x, y, theta, s, v, t, arena, player):
        Shell.__init__(self, x, y, theta, s, v, t, arena, player)
        self.protection = False

    def update_collisions(self):
        if self.exist_timer == 0:
            self.exist_timer = self.player.arena.clock
        if self.player.arena.clock-self.exist_timer >= self.time:
            self.go_die()
            return
        cells_idx = cell.calculate_cell_num(
            self.rect.center[0], self.rect.center[1])
        for i in range(0, 4):
            for wall in self.arena.cells[cells_idx[i]].walls:
                if pygame.sprite.collide_rect(self, wall):
                    if self.last_hit != None and self.last_hit is wall:
                        return
                    self.last_hit = wall
                    self.protection = False
                    if abs(wall.rect.top-self.rect.bottom) <= C.ROUND_COLLITION_EPS and self.vy > 0:
                        self.vy *= -1
                        return
                    if abs(wall.rect.bottom-self.rect.top) <= C.ROUND_COLLITION_EPS and self.vy < 0:
                        self.vy *= -1
                        return
                    if abs(wall.rect.right-self.rect.left) <= C.ROUND_COLLITION_EPS and self.vx < 0:
                        self.vx *= -1
                        return
                    if abs(wall.rect.left-self.rect.right) <= C.ROUND_COLLITION_EPS and self.vx > 0:
                        self.vx *= -1
                        return

    def go_die(self):
        self.kill()


def Shot_Gun(x, y, theta, s, v, t, arena, player):
    for i in range(20):
        player.rounds.add(Shot_Gun_Fragment(
            x=x, y=y, theta=theta+(random.random()-0.5)*C.PI/6,
            s=s, v=v, t=t, arena=arena, player=player))


class Shot_Gun_Fragment(Shell):
    def __init__(self, x, y, theta, s, v, t, arena, player):
        Shell.__init__(self, x, y, theta, s, v, t, arena, player)

    def go_die(self):
        self.kill()