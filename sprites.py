import arcade
from constants import *

class Bullet(arcade.Sprite):
  def __init__(self, filename, scale, miss_sound):
    super().__init__(filename, scale)

    self.miss_sound = miss_sound

  def update(self, *args, **kwargs):
    super().update(*args, **kwargs)

    if (self.bottom > SCREEN_HEIGHT or self.top < 0 or
        self.right < 0 or self.left > SCREEN_WIDTH):
      self.remove_from_sprite_lists()
      arcade.play_sound(self.miss_sound)

class Player(arcade.Sprite):
  def update(self, *args, **kwargs):
    super().update(*args, **kwargs)
    
    if self.left < 0:
      self.left = 0
    elif self.right > SCREEN_WIDTH:
      self.right = SCREEN_WIDTH

    if self.bottom < 0:
      self.bottom = 0
    elif self.top > SCREEN_HEIGHT:
      self.top = SCREEN_HEIGHT