import pygame
from pygame.sprite import Sprite


# Sprite used to group related elements in the game and act on all grouped elements at once.
# Call super() to inherit properly from Sprite
class Bullet(Sprite):
    """ A class to manage bullets fired from the ship """

    def __init__(self, ai_settings, screen, ship):

        """ Create a bullet object at the shi['s current position. """


        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0,0) and set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)

        # Set bullet's centerx equal to ship's centerx ( Should emerge from top of ship )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ Move the bullet up the screen. """

        # Update the decimal position of the bullet
        # When the bullet fired, it's moving up the screen, therefore, a decreasing y-coordinate value
        self.y -= self.speed_factor

        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen. """
        pygame.draw.rect(self.screen, self.color, self.rect)


