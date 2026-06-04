import arcade
import math
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Tank Arena"
MOVEMENT_SPEED = 5
BULLET_SPEED = 10

class TankArena(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    self.center_window()


    self.fire_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Hit2.wav")
    self.hit_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Hit1.wav")
    self.explode_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Boom1.wav")
    # self.miss_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Coin2.wav")
    self.miss_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Jump3.wav") 

    self.background = None

    self.setup()

  def setup(self):
    self.player_list = arcade.SpriteList()
    self.bullet_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()
    self.wall_list = arcade.SpriteList()
    self.explosion_list = arcade.SpriteList()

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

    self.wall_list.append(car_hitbox1)
    self.wall_list.append(car_hitbox2)
    self.wall_list.append(car_hitbox3)

    self.spawn_player()
    self.respawn_timer = 0
    self.spawn_enemy()

    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, [self.enemy_list, self.wall_list])

    self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (18)-ups-FAV.webp")

  def spawn_player(self):
    """ Spawns the player at a random safe location """
    self.player_sprite = arcade.Sprite("assets/TankAsset/Tank_Swamp_67x108.png", 1)
    self.player_sprite.health = 5

    is_safe = False

    while not is_safe:
      self.player_sprite.center_x = random.randint(100, SCREEN_WIDTH - 100)
      self.player_sprite.center_y = random.randint(100, SCREEN_HEIGHT - 100)

      hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)

      if len(hit_list) == 0:
        is_safe = True

      self.player_list.append(self.player_sprite)


  def spawn_enemy(self):
    """ Creates a new enemy at a random safe location """
    enemy = arcade.Sprite("assets/TankAsset/Tank_Brown_67x108.png", 1)
    enemy.health = 3

    is_safe = False

    while not is_safe:
      enemy.center_x = random.randint(100, SCREEN_WIDTH - 100)
      enemy.center_y = random.randint(100, SCREEN_HEIGHT - 100)

      hit_list = arcade.check_for_collision_with_list(enemy, self.wall_list)

      if len(hit_list) == 0:
        is_safe = True

    self.enemy_list.append(enemy)

  def on_draw(self):
    self.clear()

    arcade.draw_texture_rect(
      self.background,
      rect=arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    # For debugging. Remove later
    # self.wall_list.draw()

    self.player_list.draw()
    self.enemy_list.draw()
    self.bullet_list.draw()
    self.explosion_list.draw()

  def on_update(self, delta_time):
    self.physics_engine.update()
    self.bullet_list.update()

    if self.respawn_timer > 0:
      self.respawn_timer -= delta_time

      if self.respawn_timer <= 0:
        self.spawn_enemy()
        self.respawn_timer = 0

    for explosion in self.explosion_list:
      explosion.lifetime -= delta_time

      if explosion.lifetime <= 0:
        explosion.remove_from_sprite_lists()

    if self.player_sprite.left < 0:
      self.player_sprite.left = 0
    elif self.player_sprite.right > SCREEN_WIDTH:
      self.player_sprite.right = SCREEN_WIDTH

    if self.player_sprite.bottom < 0:
      self.player_sprite.bottom = 0
    elif self.player_sprite.top > SCREEN_HEIGHT:
      self.player_sprite.top = SCREEN_HEIGHT

    for bullet in self.bullet_list:
      enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

      if len(enemy_hit_list) > 0:
        bullet.remove_from_sprite_lists()

        for enemy in enemy_hit_list:
          enemy.health -= 1

          if enemy.health <= 0:
            explosion = arcade.Sprite("assets/explosion.png", 0.2)
            explosion.center_x = enemy.center_x
            explosion.center_y = enemy.center_y

            explosion.lifetime = 0.2

            self.explosion_list.append(explosion)

            enemy.remove_from_sprite_lists()
            arcade.play_sound(self.explode_sound)

            self.respawn_timer = 3.0
          else:
            arcade.play_sound(self.hit_sound)
      
        continue

      wall_hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)

      if len(wall_hit_list) > 0:
        bullet.remove_from_sprite_lists()
        arcade.play_sound(self.miss_sound)

        continue

      if (bullet.bottom > SCREEN_HEIGHT or bullet.top < 0 or 
          bullet.right < 0 or bullet.left > SCREEN_WIDTH):
        bullet.remove_from_sprite_lists()
        arcade.play_sound(self.miss_sound)

  def on_mouse_motion(self, x, y, dx, dy):
    """ Called whenever the mouse moves over the window """
    diff_x = x - self.player_sprite.center_x
    diff_y = y - self.player_sprite.center_y

    angle_in_radians = math.atan2(diff_y, diff_x)

    angle_in_degress = math.degrees(angle_in_radians)

    self.player_sprite.angle = 90 - angle_in_degress

  def on_mouse_press(self, x, y, button, modifiers):
    """ Called whenever the mouse button is clicked """
    arcade.play_sound(self.fire_sound)
    bullet = arcade.Sprite("assets/TankAsset/GenericProjectile.png", 1)

    bullet.center_x = self.player_sprite.center_x
    bullet.center_y = self.player_sprite.center_y

    diff_x = x - self.player_sprite.center_x
    diff_y = y - self.player_sprite.center_y
    angle_in_radians = math.atan2(diff_y, diff_x)

    bullet.angle = 90 - math.degrees(angle_in_radians)

    bullet.change_x = math.cos(angle_in_radians) * BULLET_SPEED
    bullet.change_y = math.sin(angle_in_radians) * BULLET_SPEED

    self.bullet_list.append(bullet)

  def on_key_press(self, key, modifiers):
    if key == arcade.key.W or key == arcade.key.UP:
      self.player_sprite.change_y = MOVEMENT_SPEED
    elif key == arcade.key.S or key == arcade.key.DOWN:
      self.player_sprite.change_y = -MOVEMENT_SPEED
    elif key == arcade.key.A or key == arcade.key.LEFT:
      self.player_sprite.change_x = -MOVEMENT_SPEED
    elif key == arcade.key.D or key == arcade.key.RIGHT:
      self.player_sprite.change_x = MOVEMENT_SPEED
    elif key == arcade.key.SPACE:
      self.setup()
    elif key == arcade.key.ESCAPE:
      arcade.exit()

  def on_key_release(self, key, modifiers):
    if key == arcade.key.W or key == arcade.key.UP:
      self.player_sprite.change_y = 0
    elif key == arcade.key.S or key == arcade.key.DOWN:
      self.player_sprite.change_y = 0
    elif key == arcade.key.A or key == arcade.key.LEFT:
      self.player_sprite.change_x = 0
    elif key == arcade.key.D or key == arcade.key.RIGHT:
      self.player_sprite.change_x = 0

def main():
  game = TankArena()
  arcade.run()

if __name__ == "__main__":
  main()