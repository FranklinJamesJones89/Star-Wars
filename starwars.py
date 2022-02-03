#!python3

import pygame, sys
from time import sleep
from settings import Settings
from ship import Ship
from laser import Laser
from tie import Tie
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class StarWars:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height 
        pygame.display.set_caption('Star Wars')

        # Add music to the game.
        music = pygame.mixer.music.load('Duel Of Fates Nes.mp3')
        pygame.mixer.music.play(-1)
        
        # Create an instance to store game statistics.
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.lasers = pygame.sprite.Group()
        self.ties = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")


    def  _ship_hit(self):
        """Respond to the ship being hit by a tie."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Get rid of any remaining ties and lasers.
            self.ties.empty()
            self.lasers.empty()

            # Create a new fleet and center the ship.
            self._create_fleet() 
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_ties_bottom(self):
        """check if any ties have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for tie in self.ties.sprites():
            if tie.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def run_game(self):
        """Start the main game loop."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_lasers()
                self._update_ties()
                
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks 'Play'."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

        # Get rid of any remaining ties and lasers.
            self.ties.empty()
            self.lasers.empty()

        # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_laser()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_laser(self):
        """Create a new laser and add it to the lasers group."""
        if len(self.lasers) < self.settings.lasers_allowed:
            new_laser = Laser(self)
            self.lasers.add(new_laser)
    
    def _update_lasers(self):
        """Update position of lasers and get rid of old bullets."""
        # Update laser positions.
        self.lasers.update()
        # Get rid of lasers that have disappeared.
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        
        self._check_laser_tie_collisions()

    def _check_laser_tie_collisions(self):
        """Respond to laser-tie collisions."""
        collisions = pygame.sprite.groupcollide(self.lasers, self.ties, True, True)

        if collisions:
            for ties in collisions.values():
                self.stats.score += self.settings.tie_points * len(ties)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.ties:
            # Destroy existing lasers and create new fleet.
            self.lasers.empty()
            self._create_fleet()
            self.settings.increase_speed() 
        
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()


    def _update_ties(self):
        """Update the positions of all ties in the fleet."""
        self._check_fleet_edges()
        self.ties.update()
    
        # Look for tie-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.ties):
            self._ship_hit()
            
        # Look for ties hitting the bottom of the screen.
        self._check_ties_bottom()

    def _create_fleet(self):
        """Create the fleet of tie fighters."""
        # Create a tie and find the number of ties in a row.
        # Spacing between each tie is equal to one tie width.
        tie = Tie(self)
        tie_width, tie_height = tie.rect.size
        available_space_x = self.settings.screen_width - (2 * tie_width)
        number_ties_x = available_space_x // (2 * tie_width)
        
        # Determine the number of rows of ties that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * tie_height) - ship_height)
        number_rows = available_space_y // (2 * tie_height)

        # Create the full fleet of ties.
        for row_number in range(number_rows):
            for tie_number in range(number_ties_x):
                self._create_tie(tie_number, row_number)

    def _create_tie(self, tie_number, row_number):
        """Create a tie and place it in a row."""
        tie = Tie(self)
        tie_width, tie_height = tie.rect.size
        tie.x = tie_width + 2 * tie_width * tie_number
        tie.rect.x = tie.x
        tie.rect.y = tie.rect.height + 2 * tie.rect.height * row_number
        self.ties.add(tie)

    def _check_fleet_edges(self):
        """Respond appropriately if any ties have reached an edge."""
        for tie in self.ties.sprites():
            if tie.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for tie in self.ties.sprites():
            tie.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.ties.draw(self.screen)
        
        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    sw = StarWars()
    sw.run_game()


