import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ Respond to key presses. """


    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet if limit not reached yet. """

    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """ Respond to key releases """

    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ Respond to key presses and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # mouse.get_pos() returns tuple containing x,y cords of mouse cursor when clicked

            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ Start a new game when the player clicks Play. """

    # We use collidepoint to check if the point of the mouse click overlaps region defined by Play Button's rect/
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """ Update images on the screen and flip to the new screen. """

    # Redraw the screen during each pass through the loop
    # If this was below "Redraw all bullets ... ", then it would cover up the bullets since it's
    # running after we draw the bullets, therefore, making the background cover them up.

    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    # Using draw() on a group will automatically draw each element in that group
    # at the position defined by rect attribute
    aliens.draw(screen)

    # Draw score information
    sb.show_score()

    # Draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.update()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Update position of bullets and get rid of old bullets. """

    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    # Make a copy because you don't want to remove items from a list within a for loop
    # So, we have to loop over a copy of the group.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Respond to bullet - alien collisions """

    # Check for unit collision (overlapping)
    # Whenever the two groups overlap, groupcollide() returns a key-pair dictionary and True's delete the bullets/aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    # Each bullet that collides w/ an alien becomes a key in collisions, value associated is list of aliens that it collided with
    if collisions:

        # When we multiply by len(aliens), this makes sure we correctly add up the alien points bc each value is a list
        for aliens in collisions.values():

            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

        check_high_score(stats, sb)

    # Do here because that's where individual aliens are destroyed
    if len(aliens) == 0:

        # Destroy existing bullets, speed up game, and crease new fleet
        bullets.empty()
        ai_settings.increase_speed()

        # If entire fleet destroyed, start a new level
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """ Determine the number of aliens that fit in a row"""

    # Since we have two margins, the available space for aliens is screen width - 2 alien widths
    available_space_x = ai_settings.screen_width - 2 * alien_width

    # Space needed to display one alien is twice its width (bc space between aliens is 1 alien width)
    # By dividing the total available space by the width space required, we'll be able to fit
    # how many aliens are allowed in the screen.
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Create an alien and place it in the row """

    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    # Add up the alien width, with the (2 * width) to account for space each alien takes up
    # And multiply it by the alien's position.
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x

    # Each row starts 2 alien heights below the last row, so (2 * ... * row_number)
    # If row number is not 1st row, we have one alien's height to create empty space at top of row
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create a fleet full of aliens. """

    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens
    # Outer loop counts number of rows we want
    # Inner loop creates aliens in one row
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings, ship_height, alien_height):
    """ Determine the number of rows of aliens that fit on the screen. """

    # Available vertical space is found by subtracting alien height from the top,
    # ship height from bottom, and 2 alien heights from bottom of the screen.
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def change_fleet_direction(ai_settings, aliens):
    """ Drop the entire fleet and change fleet's direction """

    # Loop through all aliens and multiply by -1 if alien is at the edge.
    for alien in aliens.sprites():
        alien.rect.y += float(ai_settings.fleet_drop_speed)
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    """ Respond appropriately if any aliens have reached an edge """

    # Loops through the fleet and calls check_edges() on each alien
    # If True, then the alien is at the edge and whole fleet needs to change direction
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Respond to ship being hit by alien. """

    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

        # Update scoreboard
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Check if any aliens have reached the bottom of the screen. """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            """ Treat this the same as if the ship got hit. """
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Update position of all aliens in the fleet. """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien - ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """ Check to see if there's a new high score. """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()