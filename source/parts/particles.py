import pygame
import numpy
import random
from .. import constants as C


class Particles(pygame.sprite.Sprite):
    def __init__(self, num, colors, size, x, y, vec_x, vec_y, arena, vertical):
        pygame.sprite.Sprite.__init__(self)
        self.particles = pygame.sprite.Group()
        for i in range(num):
            nx = vec_x+(random.random()-0.5)*3/5
            ny = vec_y+(random.random()-0.5)*3/5
            r = (nx**2+ny**2)**0.5
            theta = numpy.arccos(nx/r)
            if ny < 0:
                theta *= -1
            self.particles.add(Particle(
                x, y, theta, random.random()*arena*C.BASE_MOVE_V,
                random.random()*vertical*C.BASE_MOVE_V, colors[int(random.random()*len(colors))], size+(random.random()-0.5)*4))

    def update(self, surface):
        self.particles.update(surface)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, theta, v, vz, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.z = 0
        self.v = v
        self.theta = theta
        self.color = color
        self.size = size
        self.vz = vz

    def update(self, surface):
        self.x += self.v*numpy.cos(self.theta)
        self.y += self.v*numpy.sin(self.theta)
        self.z += self.vz
        self.v += -0.0002*self.v**2
        sign = self.vz/abs(self.vz)
        self.vz += -0.0002*self.vz**2*sign - C.GRAVI_ACC

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.width = self.size
        self.rect.height = self.size
        self.rect.center = (self.x/C.MOTION_CALC_SCALE,
                            (self.y-self.z)/C.MOTION_CALC_SCALE)
        pygame.draw.rect(surface, self.color, self.rect)

        if self.z < 0:
            self.kill()