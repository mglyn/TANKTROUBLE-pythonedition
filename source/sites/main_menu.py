import pygame
from .. import setup, tools, constants as C


class MainMenu:
    def __init__(self):
        self.setup_player()
        self.setup_cursor()
        self.setup_start_animation()
        self.finished = False
        self.next = 'load_screen'

    def setup(self, *args):
        self.setup_player()
        self.setup_cursor()
        self.setup_start_animation()
        self.finished = False
        self.next = 'load_screen'

    def setup_start_animation(self):
        self.frame_size = 0
        self.start_label = tools.create_label('press space to start', 32)
        self.display_start_label = (self.start_label, (500, 500))

    def update_start_animation(self, surface):
        if self.cursor_p1.state+self.cursor_p2.state+self.cursor_p3.state < 2:
            return
        if self.frame_size < 0.1:
            self.frame_size += 0.4/C.FRAME_RATE
        else:
            self.frame_size = -0.1
        rect = self.start_label.get_rect()
        self.display_start_label = (pygame.transform.scale(self.start_label,
                                                           (int(rect.width*(1+self.frame_size)),
                                                            int(rect.height*(1+self.frame_size)))),
                                    (0.4*C.SCREEN_W-0.1*C.SCREEN_W*self.frame_size, 0.8*C.SCREEN_H))
        surface.blit(self.display_start_label[0], self.display_start_label[1])

    def setup_player(self):
        self.player_labels = []
        self.player_labels.append(
            (tools.create_label('PLAYER 1', 35), (C.PLAYER1_X, C.PLAYER1_Y)))
        self.player_labels.append(
            (tools.create_label('WASD Q', 35), (0.15*C.SCREEN_W+C.PLAYER1_X, C.PLAYER1_Y)))
        self.player_labels.append(
            (tools.create_label('press Q', 35), (0.36*C.SCREEN_W+C.PLAYER1_X, C.PLAYER1_Y)))
        self.player_labels.append(
            (tools.create_label('PLAYER 2', 35), (C.PLAYER1_X, 0.1*C.SCREEN_H+C.PLAYER1_Y)))
        self.player_labels.append((tools.create_label(
            'IJKL U', 35), (0.15*C.SCREEN_W+C.PLAYER1_X, 0.1*C.SCREEN_H+C.PLAYER1_Y)))
        self.player_labels.append((tools.create_label(
            'press U', 35), (0.36*C.SCREEN_W+C.PLAYER1_X, 0.1*C.SCREEN_H+C.PLAYER1_Y)))
        self.player_labels.append(
            (tools.create_label('PLAYER 3', 35), (C.PLAYER1_X, 0.2*C.SCREEN_H+C.PLAYER1_Y)))
        self.player_labels.append(
            (tools.create_label('DIRECT DEL', 35), (0.15*C.SCREEN_W+C.PLAYER1_X, 0.2*C.SCREEN_H+C.PLAYER1_Y)))
        self.player_labels.append(
            (tools.create_label('press DELETE', 35), (0.36*C.SCREEN_W+C.PLAYER1_X, 0.2*C.SCREEN_H+C.PLAYER1_Y)))

    def setup_cursor(self):
        self.cursor_p1 = pygame.sprite.Sprite()
        self.cursor_p1.image = tools.get_image(
            setup.GRAPHICS['red'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.CURSOR_MULTI)
        rect = self.cursor_p1.image.get_rect()
        rect.x, rect.y = (0.57*C.SCREEN_W+C.PLAYER1_X -
                          rect.w/2, C.PLAYER1_Y-rect.h/2)
        self.cursor_p1.rect = rect
        self.cursor_p1.state = False

        self.cursor_p2 = pygame.sprite.Sprite()
        self.cursor_p2.image = tools.get_image(
            setup.GRAPHICS['green'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.CURSOR_MULTI)
        rect = self.cursor_p2.image.get_rect()
        rect.x, rect.y = (0.57*C.SCREEN_W+C.PLAYER1_X-rect.w/2,
                          0.1*C.SCREEN_H+C.PLAYER1_Y-rect.h/2)
        self.cursor_p2.rect = rect
        self.cursor_p2.state = False

        self.cursor_p3 = pygame.sprite.Sprite()
        self.cursor_p3.image = tools.get_image(
            setup.GRAPHICS['blue'], 0, 0, C.PLAYER_PY, C.PLAYER_PX, C.WHITE, C.CURSOR_MULTI)
        rect = self.cursor_p3.image.get_rect()
        rect.x, rect.y = (0.57*C.SCREEN_W+C.PLAYER1_X-rect.w/2,
                          0.2*C.SCREEN_H+C.PLAYER1_Y-rect.h/2)
        self.cursor_p3.rect = rect
        self.cursor_p3.state = False

        self.can_change = True

    def update_cursor(self, surface, keys):
        if keys[pygame.K_SPACE]:
            self.player_num = self.cursor_p1.state+self.cursor_p2.state+self.cursor_p3.state
            if self.player_num >= 2:
                self.score = (self.cursor_p1.state-1,
                              self.cursor_p2.state-1,
                              self.cursor_p3.state-1)
                self.finished = True

        if keys[pygame.K_q] and self.can_change:
            self.cursor_p1.state = not self.cursor_p1.state
        if self.cursor_p1.state:
            surface.blit(self.cursor_p1.image, self.cursor_p1.rect)

        if keys[pygame.K_u] and self.can_change:
            self.cursor_p2.state = not self.cursor_p2.state
        if self.cursor_p2.state:
            surface.blit(self.cursor_p2.image, self.cursor_p2.rect)

        if keys[pygame.K_DELETE] and self.can_change:
            self.cursor_p3.state = not self.cursor_p3.state
        if self.cursor_p3.state:
            surface.blit(self.cursor_p3.image, self.cursor_p3.rect)

        if keys[pygame.K_q] or keys[pygame.K_u] or keys[pygame.K_DELETE]:
            self.can_change = False
        else:
            self.can_change = True

    def update(self, surface, keys):
        surface.fill(C.SCREEN_COLOR)
        caption = tools.get_image(
            setup.GRAPHICS['caption'], 0, 0, 152, 14, C.WHITE, 6)
        rect = caption.get_rect()
        rect.x, rect.y = 175, 110
        surface.blit(caption, rect)
        self.update_start_animation(surface)
        self.update_cursor(surface, keys)
        for label in self.player_labels:
            surface.blit(label[0], label[1])