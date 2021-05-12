import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Class for alien """

    def __init__(self, ai_game):
        """ Alien initialization and start position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Loading pic of alien and connecting it to <rect>
        self.image = pygame.image.load('images/alien1.bmp')
        self.rect = self.image.get_rect()

        # Every new alien shows in the left upper corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saving exact horizontal position of the alien ship
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Return True if alien on the edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """ Alien move right or left """
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
