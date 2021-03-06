class GameStats():

    """ Track statistics for Alien Invasion. """

    def __init__(self, ai_settings):
        """ Initialize the statistics """
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

        # High score should never be reset (because always comparing it to 0 in game_functions.check_high_score()
        self.high_score = 0

    def reset_stats(self):
        """ Initialize statistics that we can change during the game. """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1