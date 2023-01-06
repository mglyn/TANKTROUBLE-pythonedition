import pygame
import sys
import os
from . import constants as C


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            player_num = self.state.player_num
            score = self.state.score
            next_state = self.state.next
            self.state = self.state_dict[next_state]
            self.state.setup(player_num, score)

        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()
            pygame.display.update()
            self.clock.tick(C.FRAME_RATE)


def load_graphics(path):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        img = pygame.image.load(os.path.join(path, pic))
        img = img.convert()
        graphics[name] = img
    return graphics


def load_sounds(path):
    sounds = {}
    for sound in os.listdir(path):
        name, ext = os.path.splitext(sound)
        asound = pygame.mixer.Sound(os.path.join(path, sound))
        sounds[name] = asound
    return sounds


def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(
        image, (int(width*scale), int(height*scale)))
    return image


def create_label(label, size=40, width_scale=1.25, height_scale=1):
    font = pygame.font.SysFont(C.FONT, size)
    label_image = font.render(label, 1, C.BLACK)
    rect = label_image.get_rect()
    label_image = pygame.transform.scale(
        label_image, (int(rect.width*width_scale), int(rect.height*height_scale)))
    return label_image