import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ Ship control class """

    def __init__(self, ai_game):
        """ Ship initialization and start position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # loading ship image and getting square back
        self.image = pygame.image.load('images/DurrrSpaceShip.bmp')
        self.rect = self.image.get_rect()
        # every new ship shows at the bottom ege of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # saving ship centre coordinates
        self.x = float(self.rect.x)

        # moving flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Renewing position of the ship """
        # renewing x attribute, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # renewing attribute rect (self.x)
        self.rect.x = self.x

    def blitme(self):
        """ Draws the ship in the current position """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Attaching ship in the bottom center """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
