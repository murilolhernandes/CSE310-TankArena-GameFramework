import arcade
import random
from constants import * 
from utils import calculate_aiming_data, create_wall_hitboxed, place_sprite_safely
from sprites import Bullet, Player, Enemy

class TankArena(arcade.Window):
  def __init__(self):
    """ Initializes the main game window, sets up sounds, and calls the setup method. """
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    self.center_window()

    self.fire_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Hit2.wav")
    self.hit_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Hit1.wav")
    self.explode_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Boom1.wav")
    self.miss_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Jump3.wav") 

    self.background = None

    self.high_score = 0

    self.setup()

  def setup(self):
    """ Sets up game variables, sprite lists, map hitboxes, and spawns the initial player and enemies. """
    self.player_list = arcade.SpriteList()
    self.player_bullet_list = arcade.SpriteList()
    self.enemy_bullet_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()
    self.wall_list = create_wall_hitboxed()
    self.explosion_list = arcade.SpriteList()

    self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (18)-ups-FAV.webp")

    self.game_over = False

    self.score = 0

    self.level = 1
    self.max_enemies = 1
    self.enemy_fire_rate = 1.5

    self.spawn_player()
    self.respawn_timer = 3.0
    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, [self.enemy_list, self.wall_list])
    self.enemies_spawned_this_wave = 0

  def spawn_player(self):
    """ Spawns the player at a random safe location """
    self.player_sprite = Player("assets/TankAsset/Tank_Swamp_67x108.png", 1)
    self.player_sprite.health = 5

    place_sprite_safely(self.player_sprite, self.wall_list)

    self.player_list.append(self.player_sprite)


  def spawn_enemy(self):
    """ Creates a new enemy at a random safe location """
    enemy = Enemy("assets/TankAsset/Tank_Brown_67x108.png", 1)

    enemy.fire_timer = self.enemy_fire_rate
    
    place_sprite_safely(enemy, self.wall_list)

    enemy.physics_engine = arcade.PhysicsEngineSimple(enemy, self.wall_list)

    self.enemy_list.append(enemy)

  def on_draw(self):
    """ Renders the background, all sprites, health bars, and text to the screen. """
    self.clear()

    arcade.draw_texture_rect(
      self.background,
      rect=arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    self.player_list.draw()
    self.enemy_list.draw()
    self.player_bullet_list.draw()
    self.enemy_bullet_list.draw()
    self.explosion_list.draw()

    if not self.game_over:
      arcade.draw_text(f"HP: {self.player_sprite.health} / 5", 20, SCREEN_HEIGHT - 30,
                  arcade.color.WHITE, 18, bold=True)

      arcade.draw_lbwh_rectangle_filled(20, SCREEN_HEIGHT - 60, 200, 20, arcade.color.DARK_RED)

      health_width = (self.player_sprite.health / 5) * 200

      if health_width > 0:
        arcade.draw_lbwh_rectangle_filled(20, SCREEN_HEIGHT - 60, health_width, 20, arcade.color.GREEN)

      arcade.draw_text(f"SCORE: {self.score}", SCREEN_WIDTH - 20, SCREEN_HEIGHT - 40,
                       arcade.color.GOLD, 24, bold=True, anchor_x="right")

      arcade.draw_text(f"LEVEL: {self.level}", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40,
                       arcade.color.WHITE, 24, bold=True, anchor_x="center")

    if self.game_over:
      arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                       arcade.color.RED, 64, bold=True, anchor_x="center")

      arcade.draw_text("Press SPACEBAR to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
                       arcade.color.WHITE, 24, anchor_x="center")

      stats_text = f"Level Reached: {self.level}  |  Score: {self.score}  |  Personal Best: {self.high_score}"
      arcade.draw_text(stats_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70,
                        arcade.color.GOLD, 18, bold=True, anchor_x="center")

  def on_update(self, delta_time):
    """ Updates game logic, physics, entity movement, collisions, and AI states. """
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

    expected_level = (self.score // 50) + 1
    if expected_level > self.level:
      self.level = expected_level
      self.max_enemies += 1

      self.enemy_fire_rate = max(0.5, 1.5 - ((self.level -1) * 0.2))

    if self.enemies_spawned_this_wave < self.max_enemies:
      self.respawn_timer -= delta_time

      if self.respawn_timer <= 0:
        self.spawn_enemy()
        self.enemies_spawned_this_wave += 1
        self.respawn_timer = 2.0

    elif len(self.enemy_list) == 0:
      self.enemies_spawned_this_wave = 0
      self.respawn_timer - 3.0
      
      if self.respawn_timer <= 0:
        
        for _ in range(self.max_enemies):
          self.spawn_enemy()
          
        self.respawn_timer = 3.0

    for enemy in self.enemy_list:
      enemy.follow_player(self.player_sprite, self.wall_list)

      enemy.physics_engine.update()

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

        enemy.fire_timer = self.enemy_fire_rate

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

          if self.score > self.high_score:
            self.high_score = self.score

          self.game_over = True

          return
        else:
          arcade.play_sound(self.hit_sound)

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
            self.score += 10
            explosion = arcade.Sprite("assets/explosion.png", 0.2)
            explosion.center_x = enemy.center_x
            explosion.center_y = enemy.center_y

            explosion.lifetime = 0.2

            self.explosion_list.append(explosion)

            enemy.remove_from_sprite_lists()
            arcade.play_sound(self.explode_sound)

            # self.respawn_timer = 3.0
          else:
            arcade.play_sound(self.hit_sound)
      
        continue

      wall_hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)

      if len(wall_hit_list) > 0:
        bullet.remove_from_sprite_lists()
        arcade.play_sound(self.miss_sound)

        continue

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
    """ Handles keyboard input for movement, restarting the game, or exiting. """
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
    """ Handles keyboard input when a movement key is released to stop the player. """
    if key == arcade.key.W or key == arcade.key.UP:
      self.player_sprite.change_y = 0
    elif key == arcade.key.S or key == arcade.key.DOWN:
      self.player_sprite.change_y = 0
    elif key == arcade.key.A or key == arcade.key.LEFT:
      self.player_sprite.change_x = 0
    elif key == arcade.key.D or key == arcade.key.RIGHT:
      self.player_sprite.change_x = 0

def main():
  """ Main entry point to initialize the game window and start the arcade event loop. """
  game = TankArena()
  arcade.run()

if __name__ == "__main__":
  main()