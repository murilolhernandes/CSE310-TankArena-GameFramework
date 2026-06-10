import arcade
from constants import *
import math
from utils import calculate_aiming_data

class Bullet(arcade.Sprite):
  def __init__(self, filename, scale, miss_sound):
    """ Initializes the Bullet sprite with a specified texture, scale, and miss sound. """
    super().__init__(filename, scale)

    self.miss_sound = miss_sound

  def update(self, *args, **kwargs):
    """ Updates the bullet's position and removes it if it flies off-screen. """
    super().update(*args, **kwargs)

    if (self.bottom > SCREEN_HEIGHT or self.top < 0 or
        self.right < 0 or self.left > SCREEN_WIDTH):
      self.remove_from_sprite_lists()
      arcade.play_sound(self.miss_sound)

class Player(arcade.Sprite):
  def update(self, *args, **kwargs):
    """ Updates the player's position and prevents them from leaving the screen bounds. """
    super().update(*args, **kwargs)
    
    if self.left < 0:
      self.left = 0
    elif self.right > SCREEN_WIDTH:
      self.right = SCREEN_WIDTH

    if self.bottom < 0:
      self.bottom = 0
    elif self.top > SCREEN_HEIGHT:
      self.top = SCREEN_HEIGHT

class Enemy(arcade.Sprite):
  def __init__(self, filename, scale):
    """ Initializes the Enemy tank sprite with standard attributes like health and fire rate. """
    super().__init__(filename, scale)

    self.health = 5
    self.fire_timer = 1.5
    self.speed = 1

  def follow_player(self, player_sprite, wall_list):
    """ Smart AI: Calculate the angle to the player and drive towards them, while dodging walls """
    target_angle, dx, dy = calculate_aiming_data(
      self.center_x, self.center_y,
      player_sprite.center_x, player_sprite.center_y,
      self.speed
    )

    look_ahead_x = self.center_x + (dx * 10)
    look_ahead_y = self.center_y + (dy * 10)

    for wall in wall_list:
      distance = math.dist((look_ahead_x, look_ahead_y), (wall.center_x, wall.center_y))

      if distance < 50:
        dx -= (wall.center_x - self.center_x) * 0.1
        dy -= (wall.center_y - self.center_y) * 0.1

    self.change_x = dx
    self.change_y = dy
    self.angle = 90 - math.degrees(math.atan2(self.change_y, self.change_x))