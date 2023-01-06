import pygame
from . import constants as C
from . import tools

pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.display.set_caption('TANK TROUBLE PYTHON EDITION')
pygame.display.set_mode(C.SCREEN_SIZE)
GRAPHICS = tools.load_graphics('resources/graphics')
pygame.display.set_icon(tools.get_image(
    GRAPHICS['icon'], 7, 0, 27, 41, C.WHITE, C.CURSOR_MULTI))
SOUNDS = tools.load_sounds('resources/sounds')