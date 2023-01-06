import pygame
import numpy
import random
from .. import tools, setup, constants as C
from . import shell, cell, particles


class player(pygame.sprite.Sprite):
    def __init__(self, name, arena):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.arena = arena
        self.setup_states()
        self.setup_hitboxes()
        self.load_material()

    def setup_states(self):
        self.fire = False
        self.fire_timer = 0
        self.fire_cool_down_timer = 0
        self.not_stuck = True
        self.moving = False
        self.stuking_timer = 0
        self.dead = False
        self.can_fire = True
        self.shotgun = False
        self.biground = False
        self.random = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.round_num = 0
        self.exploding = False
        self.rounds = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

    def setup_hitboxes(self):
        self.hitboxes = pygame.sprite.Group()
        self.relapositions = []
        x = C.PLAYER_PX*C.PLAYER_MULTI/2-3
        y = -C.PLAYER_PY*C.PLAYER_MULTI/2+2
        d = C.PLAYER_PX*C.PLAYER_MULTI/12
        for i in range(8):
            r = numpy.sqrt(x**2+y**2)
            alpha = numpy.arccos(x/r)
            if y < 0:
                alpha = -alpha
            self.relapositions.append((r, alpha))
            self.relapositions.append((r, C.PI-alpha))
            y += d
        x = C.PLAYER_PX*C.PLAYER_MULTI/2-3
        y = C.PLAYER_PY*C.PLAYER_MULTI/2-2
        for i in range(11):
            r = numpy.sqrt(x**2+y**2)
            alpha = numpy.arccos(x/r)
            self.relapositions.append((r, alpha))
            self.relapositions.append((r, -alpha))
            x += -d

    def load_material(self):
        if self.name == 1:
            self.image = tools.get_image(
                setup.GRAPHICS['red'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.PLAYER_MULTI)
            self.fire_image = tools.get_image(
                setup.GRAPHICS['red_s'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.PLAYER_MULTI)
        elif self.name == 2:
            self.image = tools.get_image(
                setup.GRAPHICS['green'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.PLAYER_MULTI)
            self.fire_image = tools.get_image(
                setup.GRAPHICS['green_s'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.PLAYER_MULTI)
        elif self.name == 3:
            self.image = tools.get_image(
                setup.GRAPHICS['blue'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.PLAYER_MULTI)
            self.fire_image = tools.get_image(
                setup.GRAPHICS['blue_s'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.PLAYER_MULTI)
        self.display_image = self.image

    def update_position(self, keys):
        if self.x/C.MOTION_CALC_SCALE < C.LEFT_SPACE:
            self.x = (C.BLOCK_SIZE/2+C.LEFT_SPACE)*C.MOTION_CALC_SCALE
        if self.y/C.MOTION_CALC_SCALE < C.TOP_SPACE:
            self.y = (C.BLOCK_SIZE/2+C.TOP_SPACE)*C.MOTION_CALC_SCALE
        if self.x/C.MOTION_CALC_SCALE > C.LEFT_SPACE+C.COLUMN_NUM*C.BLOCK_SIZE:
            self.x = (C.LEFT_SPACE+(C.COLUMN_NUM-0.5) *
                      C.BLOCK_SIZE)*C.MOTION_CALC_SCALE
        if self.y/C.MOTION_CALC_SCALE > C.TOP_SPACE+C.ROW_NUM*C.BLOCK_SIZE:
            self.y = (C.TOP_SPACE+(C.ROW_NUM-0.5) *
                      C.BLOCK_SIZE)*C.MOTION_CALC_SCALE

        self.moving = False
        if self.name == 1:
            if not keys[pygame.K_w] or not keys[pygame.K_s]:
                if keys[pygame.K_w]:
                    self.moving = True
                    self.x += C.BASE_MOVE_V * \
                        numpy.cos(self.theta)*self.not_stuck
                    self.y += C.BASE_MOVE_V * \
                        numpy.sin(self.theta)*self.not_stuck
                if keys[pygame.K_s]:
                    self.moving = True
                    self.x += -C.BACKWARD_V * \
                        numpy.cos(self.theta)*self.not_stuck
                    self.y += -C.BACKWARD_V * \
                        numpy.sin(self.theta)*self.not_stuck

            if not keys[pygame.K_a] or not keys[pygame.K_d]:
                if keys[pygame.K_a]:
                    self.moving = True
                    self.theta += -C.BASE_TURN_W*self.not_stuck
                if keys[pygame.K_d]:
                    self.moving = True
                    self.theta += C.BASE_TURN_W*self.not_stuck

        elif self.name == 2:
            if not keys[pygame.K_i] or not keys[pygame.K_k]:
                if keys[pygame.K_i]:
                    self.moving = True
                    self.x += C.BASE_MOVE_V * \
                        numpy.cos(self.theta)*self.not_stuck
                    self.y += C.BASE_MOVE_V * \
                        numpy.sin(self.theta)*self.not_stuck
                if keys[pygame.K_k]:
                    self.moving = True
                    self.x += -C.BACKWARD_V * \
                        numpy.cos(self.theta)*self.not_stuck
                    self.y += -C.BACKWARD_V * \
                        numpy.sin(self.theta)*self.not_stuck

            if not keys[pygame.K_j] or not keys[pygame.K_l]:
                if keys[pygame.K_j]:
                    self.moving = True
                    self.theta += -C.BASE_TURN_W*self.not_stuck
                if keys[pygame.K_l]:
                    self.moving = True
                    self.theta += C.BASE_TURN_W*self.not_stuck

        elif self.name == 3:
            if not keys[pygame.K_UP] or not keys[pygame.K_DOWN]:
                if keys[pygame.K_UP]:
                    self.moving = True
                    self.x += C.BASE_MOVE_V * \
                        numpy.cos(self.theta)*self.not_stuck
                    self.y += C.BASE_MOVE_V * \
                        numpy.sin(self.theta)*self.not_stuck
                if keys[pygame.K_DOWN]:
                    self.moving = True
                    self.x += -C.BACKWARD_V * \
                        numpy.cos(self.theta)*self.not_stuck
                    self.y += -C.BACKWARD_V * \
                        numpy.sin(self.theta)*self.not_stuck

            if not keys[pygame.K_LEFT] or not keys[pygame.K_RIGHT]:
                if keys[pygame.K_LEFT]:
                    self.moving = True
                    self.theta += -C.BASE_TURN_W*self.not_stuck
                if keys[pygame.K_RIGHT]:
                    self.moving = True
                    self.theta += C.BASE_TURN_W*self.not_stuck

        if self.theta >= 2*C.PI:
            self.theta -= 2*C.PI
        if self.theta < 0:
            self.theta += 2*C.PI

    def update_image(self):
        if self.fire:
            self.display_image = pygame.transform.rotate(
                self.fire_image, (1.5*C.PI-self.theta)*180/C.PI)
        else:
            self.display_image = pygame.transform.rotate(
                self.image, (1.5*C.PI-self.theta)*180/C.PI)

    def update_fire(self, keys):
        if not self.can_fire:
            if self.arena.clock-self.fire_cool_down_timer >= C.FIRE_COOL_DOWN:
                self.can_fire = True

        flag = False
        if self.name == 1 and keys[pygame.K_q]:
            flag = True
        if self.name == 2 and keys[pygame.K_u]:
            flag = True
        if self.name == 3 and keys[pygame.K_DELETE]:
            flag = True

        if flag and self.can_fire and not self.fire:
            if self.round_num < C.MAX_ROUND_NUM or self.shotgun or self.biground:
                self.fire = True
                self.fire_timer = self.arena.clock

        if self.fire:
            self.fire_cool_down_timer = self.arena.clock
            self.can_fire = False
            if self.arena.clock-self.fire_timer >= C.FIRE_TICK:
                setup.SOUNDS['fire'+str(int(self.random*4+1))].play()

                if self.shotgun:
                    setup.SOUNDS['fire'+str(int(self.random*4+1))].play()
                    shell.Shot_Gun(self.x+0.32*C.MPX*numpy.cos(self.theta), self.y + 0.32*C.MPY*numpy.sin(
                        self.theta), theta=self.theta, s=0.7, v=1.4, t=0.08, arena=self.arena, player=self)
                    self.shotgun = False

                elif self.biground:
                    self.rounds.add(shell.Big_Shell(x=self.x+0.32*C.MPX*numpy.cos(self.theta), y=self.y+0.32*C.MPY * numpy.sin(self.theta),
                                                    theta=self.theta, s=1.5, v=1.4, t=0.11, arena=self.arena, player=self))
                    self.biground = False

                else:
                    self.rounds.add(shell.Shell(x=self.x+0.32*C.MPX*numpy.cos(self.theta),
                                    y=self.y+0.32*C.MPY*numpy.sin(self.theta),
                                    theta=self.theta, s=1, v=1, t=1,
                                    arena=self.arena, player=self))
                    self.round_num += 1

                self.fire = False

    def calculate_hitboxes(self):
        self.hitboxes.empty()
        for pos in self.relapositions:
            hitbox = pygame.sprite.Sprite()
            hitbox.image = pygame.Surface(
                (C.PLAYER_PX*C.PLAYER_MULTI/12+2, C.PLAYER_PX*C.PLAYER_MULTI/12+2)).convert()
            hitbox.rect = hitbox.image.get_rect()
            hitbox.rect.center = (pos[0]*numpy.cos(pos[1]+self.theta) +
                                  self.x/100, pos[0]*numpy.sin(pos[1]+self.theta)+self.y/100)
            hitbox.image.fill((0, 0, 0))
            self.hitboxes.add(hitbox)

    def update_collisions(self):
        self.not_stuck = True
        cells_idx = cell.calculate_cell_num(
            self.x/C.MOTION_CALC_SCALE, self.y/C.MOTION_CALC_SCALE)
        for acell in cells_idx:
            for wall in self.arena.cells[acell].walls:
                hitbox = pygame.sprite.spritecollideany(
                    wall, self.hitboxes)
                if hitbox:
                    self.not_stuck = False
                    self.adjust_position(hitbox, 0.1, True)
                    return

        self.stuking_timer = self.arena.clock

        for player in self.arena.players:
            if player is self:
                continue
            if abs(player.x-self.x)/C.MOTION_CALC_SCALE > C.PLAYER_PX or abs(player.y-self.y)/C.MOTION_CALC_SCALE > C.PLAYER_PX:
                continue
            for self_hitbox in self.hitboxes:
                hitbox = pygame.sprite.spritecollideany(
                    self_hitbox, player.hitboxes)
                if hitbox:
                    self.not_stuck = False
                    self.adjust_position(hitbox, 1, False)
                    return

    def adjust_position(self, hitbox, k, time_matters):
        x = hitbox.rect.center[0] - \
            self.x/C.MOTION_CALC_SCALE
        y = hitbox.rect.center[1] - \
            self.y/C.MOTION_CALC_SCALE
        alpha = numpy.arccos(x/numpy.sqrt(x**2+y**2))
        if y < 0:
            alpha = -alpha

        if (time_matters):
            self.x -= numpy.cos(alpha-self.theta)*min((self.arena.clock-self.stuking_timer), 10)*k * \
                C.MOTION_CALC_SCALE * \
                numpy.cos(self.theta) + (self.random-0.5) * \
                (self.arena.clock-self.stuking_timer)
            self.y -= numpy.cos(alpha-self.theta)*min(0.1*(self.arena.clock-self.stuking_timer), 10)*k * \
                C.MOTION_CALC_SCALE * \
                numpy.sin(self.theta) + (random.random()-0.5) * \
                (self.arena.clock-self.stuking_timer)
            self.x -= numpy.sin(alpha-self.theta) * min((self.arena.clock-self.stuking_timer), 100)*k * \
                C.MOTION_CALC_SCALE*-numpy.sin(self.theta)
            self.y -= numpy.sin(alpha-self.theta) * min((self.arena.clock-self.stuking_timer), 100)*k * \
                C.MOTION_CALC_SCALE*numpy.cos(self.theta)
        else:
            self.x -= numpy.cos(alpha-self.theta)*k * \
                C.MOTION_CALC_SCALE * \
                numpy.cos(self.theta) + (self.random-0.5) * \
                (self.arena.clock-self.stuking_timer)
            self.y -= numpy.cos(alpha-self.theta)*k * \
                C.MOTION_CALC_SCALE * \
                numpy.sin(self.theta) + (random.random()-0.5) * \
                (self.arena.clock-self.stuking_timer)
            self.x -= numpy.sin(alpha-self.theta) * k * \
                C.MOTION_CALC_SCALE*-numpy.sin(self.theta)
            self.y -= numpy.sin(alpha-self.theta) * k * \
                C.MOTION_CALC_SCALE*numpy.cos(self.theta)

    def go_die(self):
        setup.SOUNDS['explosion'+str(int(self.random*6+1))].play()
        self.hitboxes.empty()

        self.dead = True
        self.arena.rest_player_num -= 1
        self.arena.ending_timer = self.arena.clock

        if self.name == 1:
            color = C.RED
        elif self.name == 2:
            color = C.GREEN
        elif self.name == 3:
            color = C.BLUE

        self.particles.add(particles.Particles(
            20, (C.GRAY, C.DARK_GRAY, color), 9, self.x, self.y, 0, 0, 6, 6))
        self.exploding = True

    def update_moving_particles(self):
        if not self.not_stuck and random.randint(1, 2) == 1:
            sign = int(self.random+0.5)*2-1
            self.particles.add(particles.Particles(
                1, (C.GRAY, C.DARK_GRAY, C.BLACK), 6, (self.x+sign*0.4*C.PLAYER_PY*C.MOTION_CALC_SCALE*numpy.sin(self.theta))-0.4*C.PLAYER_PX*C.MOTION_CALC_SCALE*numpy.cos(
                    self.theta), (self.y-sign*0.4*C.PLAYER_PY*C.MOTION_CALC_SCALE*numpy.cos(self.theta))-0.4*C.PLAYER_PX*C.MOTION_CALC_SCALE*numpy.sin(self.theta),
                -numpy.cos(self.theta), -numpy.sin(self.theta), 0.8, 0.8))
            return
        if self.moving and random.randint(1, 64) == 1:
            sign = int(self.random+0.5)*2-1
            self.particles.add(particles.Particles(
                1, (C.GRAY, C.DARK_GRAY), 4, (self.x+sign*0.4*C.PLAYER_PY*C.MOTION_CALC_SCALE*numpy.sin(self.theta))-0.4*C.PLAYER_PX*C.MOTION_CALC_SCALE*numpy.cos(
                    self.theta), (self.y-sign*0.4*C.PLAYER_PY*C.MOTION_CALC_SCALE*numpy.cos(self.theta))-0.4*C.PLAYER_PX*C.MOTION_CALC_SCALE*numpy.sin(self.theta),
                -numpy.cos(self.theta), -numpy.sin(self.theta), 0.8, 0.8))

    def update(self, keys):
        self.random = self.arena.random
        self.rounds.update()
        if not self.dead:
            self.update_position(keys)
            self.update_fire(keys)
            self.update_image()
            self.calculate_hitboxes()
            if self.moving:
                self.update_collisions()
                self.update_moving_particles()

    def celebrate(self):
        setup.SOUNDS['fire'+str(int(self.random*4+1))].play()
        self.particles.add(particles.Particles(
            20, (C.PURPLE, C.RED, C.YELLOW), 6, self.x+0.32*C.PLAYER_PX*C.MOTION_CALC_SCALE*numpy.cos(
                self.theta), self.y+0.32*C.PLAYER_PX*C.MOTION_CALC_SCALE*numpy.sin(self.theta),
            numpy.cos(self.theta), numpy.sin(self.theta), 12, 2))

    def draw(self, surface):
        if not self.dead:
            surface.blit(self.display_image, self.display_image.get_rect(
                center=(self.x/C.MOTION_CALC_SCALE, self.y/C.MOTION_CALC_SCALE)))
        self.rounds.draw(surface)
        self.particles.update(surface)