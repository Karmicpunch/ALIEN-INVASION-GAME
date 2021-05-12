class GameStats:
    """ Alien Invasion statistic """

    def __init__(self, ai_game):
        """ Statistic initialisation """
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """ Initialisation statistic that changing in game """
        self.ships_left = self.settings.ship_limit
