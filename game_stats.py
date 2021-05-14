class GameStats:
    """ Alien Invasion statistic """

    def __init__(self, ai_game):
        """ Statistic initialisation """
        self.settings = ai_game.settings
        self.reset_stats()

        # Game can runs in inactive state
        self.game_active = False
        # Record stays
        self.high_score = 0

    def reset_stats(self):
        """ Initialisation statistic that changing in game """
        self.ships_left = self.settings.ship_limit
        self.score = 0
