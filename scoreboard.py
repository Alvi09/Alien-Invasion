import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():

    """ A class to report scoring information. """
    def __init__(self, ai_settings, screen, stats):

        """ Initialize scorekeeping attributes. """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)
        self.font_level = pygame.font.SysFont(None, 24)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_high_score_label()
        self.prep_level_image()
        self.prep_stage()
        self.prep_ships()

    def prep_score(self):
        """ Turn the score into a rendered image. """

        # Negative integer will round value to nearest 10, 100, 1000, ...
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Turn the high score into a rendered image. """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font_level.render(high_score_str, True,
                                                       self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_high_score_label(self):
        ''' Write "high score" in front of the high score number '''

        self.high_score_text = self.font_level.render(str("High Score:"),
                                                      True, self.text_color, self.ai_settings.bg_color)

        # "High Score:" font positioned before the score
        self.high_score_text_rect = self.high_score_image.get_rect()
        self.high_score_text_rect.centerx = self.screen_rect.centerx
        self.high_score_text_rect.top = self.high_score_rect.top
        self.high_score_text_rect.left = self.high_score_rect.left - 125

    def prep_level_image(self):

        """ Turn the level into a render image. """
        self.level_image = self.font_level.render(str(self.stats.level),
                                                  True, self.text_color, self.ai_settings.bg_color)
        # Position the level below the score.
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def prep_stage(self):
        ''' Write "Stage" in front of the stage number '''
        self.level_text = self.font_level.render(str("Stage:"), True, self.text_color, self.ai_settings.bg_color)

        # "Stage:" font positioned before the score
        self.level_text_rect = self.level_text.get_rect()
        self.level_text_rect.right = self.score_rect.left - 10
        self.level_text_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ Show many ships are left """

        # Basically applies the ship icon spaced next to each other depending on how many lives you have
        self.ships = Group()

        for ship_number in range(self.stats.ships_left + 1):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        """ Draw score to the screen. """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.high_score_text, self.high_score_text_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.screen.blit(self.level_text, self.level_text_rect)

        self.ships.draw(self.screen)