import arcade
import random
from constants import * 
from utils import calculate_aiming_data, create_wall_hitboxed, place_sprite_safely
from sprites import Bullet, Player

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
    self.player_bullet_list = arcade.SpriteList()
    self.enemy_bullet_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()
    self.wall_list = create_wall_hitboxed()
    self.explosion_list = arcade.SpriteList()

    self.spawn_player()
    self.respawn_timer = 0
    self.spawn_enemy()

    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, [self.enemy_list, self.wall_list])

    self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (18)-ups-FAV.webp")

    self.game_over = False

  def spawn_player(self):
    """ Spawns the player at a random safe location """
    self.player_sprite = Player("assets/TankAsset/Tank_Swamp_67x108.png", 1)
    self.player_sprite.health = 5

    place_sprite_safely(self.player_sprite, self.wall_list)

    self.player_list.append(self.player_sprite)


  def spawn_enemy(self):
    """ Creates a new enemy at a random safe location """
    enemy = arcade.Sprite("assets/TankAsset/Tank_Brown_67x108.png", 1)
    enemy.health = 5

    enemy.fire_timer = 1.5

    place_sprite_safely(enemy, self.wall_list)

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
    self.player_bullet_list.draw()
    self.enemy_bullet_list.draw()
    self.explosion_list.draw()

    if self.game_over:
      arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30,
                       arcade.color.RED, 64, anchor_x="center")

      arcade.draw_text("Press SPACEBAR to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                       arcade.color.WHITE, 24, anchor_x="center")

  def on_update(self, delta_time):
    if self.game_over:
      for explosion in self.explosion_list:
        explosion.lifetime -= delta_time
        if explosion.lifetime <= 0:
          explosion.remove_from_sprite_lists()

      return
    
    self.physics_engine.update()
    self.player_list.update()
    self.player_bullet_list.update()
    self.enemy_bullet_list.update()

    for enemy in self.enemy_list:
      enemy.fire_timer -= delta_time

      if enemy.fire_timer <= 0:
        arcade.play_sound(self.fire_sound)
        enemy_bullet = Bullet("assets/TankAsset/GenericProjectile.png", 1, self.miss_sound)
        enemy_bullet.color = arcade.color.RED

        enemy_bullet.center_x = enemy.center_x
        enemy_bullet.center_y = enemy.center_y

        enemy_bullet.angle, enemy_bullet.change_x, enemy_bullet.change_y = calculate_aiming_data(
          enemy.center_x,
          enemy.center_y,
          self.player_sprite.center_x,
          self.player_sprite.center_y,
          BULLET_SPEED
        )

        self.enemy_bullet_list.append(enemy_bullet)

        enemy.fire_timer = 1.5

    for bullet in self.enemy_bullet_list:
      wall_hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
      if len(wall_hit_list) > 0:
        bullet.remove_from_sprite_lists()

        arcade.play_sound(self.miss_sound)

        continue

      if arcade.check_for_collision(bullet, self.player_sprite):
        bullet.remove_from_sprite_lists()
        self.player_sprite.health -= 1

        if self.player_sprite.health <= 0:
          explosion = arcade.Sprite("assets/explosion.png", 0.2)
          explosion.center_x = self.player_sprite.center_x
          explosion.center_y = self.player_sprite.center_y

          explosion.lifetime = 0.2

          self.explosion_list.append(explosion)

          self.player_sprite.remove_from_sprite_lists()
          arcade.play_sound(self.explode_sound)

          self.game_over = True

          return
        else:
          arcade.play_sound(self.hit_sound)

    if self.respawn_timer > 0:
      self.respawn_timer -= delta_time

      if self.respawn_timer <= 0:
        self.spawn_enemy()
        self.respawn_timer = 0

    for explosion in self.explosion_list:
      explosion.lifetime -= delta_time

      if explosion.lifetime <= 0:
        explosion.remove_from_sprite_lists()

    for bullet in self.player_bullet_list:
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

      # if (bullet.bottom > SCREEN_HEIGHT or bullet.top < 0 or 
      #     bullet.right < 0 or bullet.left > SCREEN_WIDTH):
      #   bullet.remove_from_sprite_lists()
      #   arcade.play_sound(self.miss_sound)

  def on_mouse_motion(self, x, y, dx, dy):
    """ Called whenever the mouse moves over the window """
    if self.game_over:
      return
    
    angle, _, _ = calculate_aiming_data(
      self.player_sprite.center_x,
      self.player_sprite.center_y,
      x, y, 0
    )

    self.player_sprite.angle = angle

  def on_mouse_press(self, x, y, button, modifiers):
    """ Called whenever the mouse button is clicked """
    if self.game_over:
      return
    
    arcade.play_sound(self.fire_sound)
    bullet = Bullet("assets/TankAsset/GenericProjectile.png", 1, self.miss_sound)

    bullet.center_x = self.player_sprite.center_x
    bullet.center_y = self.player_sprite.center_y

    bullet.angle, bullet.change_x, bullet.change_y = calculate_aiming_data(
      self.player_sprite.center_x,
      self.player_sprite.center_y,
      x,
      y,
      BULLET_SPEED
    )

    self.player_bullet_list.append(bullet)

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