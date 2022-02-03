#!python3

class Settings:
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = 255, 0, 0
        self.lasers_allowed = 3

        # Tie settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        
        # How quickly the tie point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.laser_speed = 3.0
        self.tie_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.tie_points = 50

    def increase_speed(self):
        """Increase speed settings and tie point values."""
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.tie_speed *= self.speedup_scale

        self.tie_points = int(self.tie_points * self.score_scale)
