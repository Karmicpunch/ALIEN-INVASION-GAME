class Settings:
    """ Class for storage all game settings """

    def __init__(self):
        """ Settings initialisation """
        # screen parameters
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 30)

        # ship speed settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 4

        # alien settings
        self.alien_speed = 0.3
        self.fleet_drop_speed = 10
        # fleet_direction = 1 means moving right, -1 moving left
        self.fleet_direction = 1
