#! python3

import pygame
from pygame.sprite import Sprite

class Tie(Sprite):
    """A class to represent a single tie fighter in the fleet."""

    def __init__(self, sw_game):
        """Initialize the tie fighter and set its starting position."""
        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings

        # Load the tie fighter image and set its rect attribute.
        self.image = pygame.image.load('images/tie_fighter.bmp')
        self.rect = self.image.get_rect()

        # Start each new tie fighter near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the tie fighter's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if tie is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the tie to the right."""
        self.x += (self.settings.tie_speed * self.settings.fleet_direction)
        self.rect.x = self.x
