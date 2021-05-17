import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ Class to control resources of the game. """

    def __init__(self):
        """ Game initialization, building game resources."""
        pygame.init()  # initialization of game settings

        self.settings = Settings()
        # For full screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # pygame.display.set_caption("Alien Invasion")
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # graphical elements of the game ("surface")
        pygame.display.set_caption("Alien Invasion")  # 1200-800 window parameters

        # Creating exemplar for game statistic
        # and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Button "PLAY"
        self.play_button = Button(self, "PLAY")

    def run_game(self):
        """ Main cycle run"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # Tracking keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_botton(mouse_pos)

    def _check_play_botton(self, mouse_pos):
        """ Starting new game when 'PLAY' pressed """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Reset aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Creating new fleet and a ship in the centre
            self._create_fleet()
            self.ship.center_ship()
            # Mouse pointer not shows during the game
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """ Keystroke response (push)"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Keystroke response (release)"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """ Making new bullet and including it in bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # remove bullets, after reaching upper screen edge
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision"""
        # if hit - remove bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # destroying existed bullets and creating new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # level increase
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ Renewing positions of aliens """
        self._check_fleet_edges()
        self.aliens.update()
        # check alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Checking that aliens get to the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """ Checking that aliens get to the bottom edge of the screen """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """respond to the ship hit the alien"""
        if self.stats.ships_left > 0:
            # ships_left become less; renewing points
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # cleaning lists of aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Creating new fleet and displaying new ship in the center
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """ Fleet of invasion """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # alien fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # alien creation, counting aliens in a row
        # interval between two aliens = alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """ Alien reach the edge of the screen """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Moving all fleet down and change direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # code that rewriting the screen in cycle
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Information about score
        self.sb.show_score()

        # "PLAY" button shows only in inactive game
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Showing last game screen. This module will be renewing screen
        # while cycle working.
        pygame.display.flip()


if __name__ == '__main__':
    # Building exemplar and run game.
    ai = AlienInvasion()
    ai.run_game()
