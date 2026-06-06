import math
import arcade
from constants import *
import random

def calculate_aiming_data(start_x, start_y, target_x, target_y, speed):
  """ Calculates the visual angle and X/Y velocities needed to travel from a start point to a target. """
  diff_x = target_x - start_x
  diff_y = target_y - start_y

  angle_in_radians = math.atan2(diff_y, diff_x)

  angle_in_degress = 90 - math.degrees(angle_in_radians)

  change_x = math.cos(angle_in_radians) * speed
  change_y = math.sin(angle_in_radians) * speed

  return angle_in_degress, change_x, change_y

def create_wall_hitboxed():
  """ Builds and returns a SpriteList containing all the map hitboxes """
  wall_list = arcade.SpriteList()

  car_hitbox1 = arcade.SpriteSolidColor(90, 270, arcade.color.BRIGHT_GREEN)
  car_hitbox1.center_x = 420
  car_hitbox1.center_y = 190
  car_hitbox1.angle = -15
  car_hitbox1.alpha = 100

  car_hitbox2 = arcade.SpriteSolidColor(140, 100, arcade.color.BLACK)
  car_hitbox2.center_x = 300
  car_hitbox2.center_y = 200
  car_hitbox2.angle = -25
  car_hitbox2.alpha = 100

  car_hitbox3 = arcade.SpriteSolidColor(200, 85, arcade.color.BLACK)
  car_hitbox3.center_x = 825
  car_hitbox3.center_y = 475
  car_hitbox3.angle = 45
  car_hitbox3.alpha = 100

  wall_list.append(car_hitbox1)
  wall_list.append(car_hitbox2)
  wall_list.append(car_hitbox3)

  return wall_list

def place_sprite_safely(sprite, wall_list):
  """ Randomly places a sprite until it doesn't hit any walls """
  is_safe = False

  while not is_safe:
    sprite.center_x = random.randint(100, SCREEN_WIDTH - 100)
    sprite.center_y = random.randint(100, SCREEN_HEIGHT - 100)

    hit_list = arcade.check_for_collision_with_list(sprite, wall_list)
    if len(hit_list) == 0:
      is_safe = True