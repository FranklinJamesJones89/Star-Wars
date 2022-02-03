#!python3

import pygame
from pygame.sprite import Sprite

class Laser(Sprite):
    """A class to manage lasers fired from the ship."""

    def __init__(self, sw_game):
        """"Create a laser object at the ship's current position."""
        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.color = self.settings.laser_color

        # Create a laser rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
        self.rect.midtop = sw_game.ship.rect.midtop

        # Store the laser's position as a decimal value.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the laser up the screen."""
        # Update the decimal position of the laser.
        self.y -= self.settings.laser_speed
        # Update the rect positiion.
        self.rect.y = self.y

    def draw_laser(self):
        """Draw the laser to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
