import arcade
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Tank Arena"
MOVEMENT_SPEED = 5
BULLET_SPEED = 10

class TankArena(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    self.center_window()

    arcade.set_background_color(arcade.color.ANTIQUE_BRASS)

    self.fire_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Hit2.wav")
    self.hit_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Hit1.wav")
    self.explode_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Boom1.wav")
    # self.miss_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Coin2.wav")
    self.miss_sound = arcade.load_sound("assets/JaviiWind 8 Bits Samples SFX/Jump3.wav") 

    # self.background = None

    self.setup()

  def setup(self):
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (12)-ups-FAV.webp")
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (13)-ups-FAV.webp")
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (17)-ups-FAV.webp")
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (18)-ups-FAV.webp")
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (21)-ups-FAV.webp")
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (35)-ups-FAV.webp")
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (67)-ups-FAV.webp") # Hard to see the projectile
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (71)-ups-FAV.webp") # Hard to see the projectile
    # self.background = arcade.load_texture("assets/S0L-Fallout-VTTPack/Fallout-Maps/FOMAP (94)-ups-FAV.webp") # Really hard to see the tank and projectile

    self.player_list = arcade.SpriteList()
    self.bullet_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()

    # self.player_sprite = arcade.Sprite("assets/TankAsset/Tank_Dark_67x108.png", 1)
    self.player_sprite = arcade.Sprite("assets/TankAsset/Tank_Swamp_67x108.png", 1)
    # self.player_sprite = arcade.Sprite("assets/TankAsset/Tank_B_Big_Gray_3_128x194.png", 0.5)
    self.player_sprite.center_x = 400
    self.player_sprite.center_y = 300
    self.player_list.append(self.player_sprite)

    self.enemy = arcade.Sprite("assets/TankAsset/Tank_Brown_67x108.png", 1)
    self.enemy.center_x = 200
    self.enemy.center_y = 450
    self.enemy.health = 3
    self.enemy_list.append(self.enemy)

    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.enemy_list)

  def on_draw(self):
    self.clear()

    # arcade.draw_texture_rect(
    #   self.background,
    #   rect=arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    # )

    self.player_list.draw()

    self.enemy_list.draw()

    self.bullet_list.draw()

  def on_update(self, delta_time):
    self.physics_engine.update()
    self.bullet_list.update()

    if self.player_sprite.left < 0:
      self.player_sprite.left = 0
    elif self.player_sprite.right > SCREEN_WIDTH:
      self.player_sprite.right = SCREEN_WIDTH

    if self.player_sprite.bottom < 0:
      self.player_sprite.bottom = 0
    elif self.player_sprite.top > SCREEN_HEIGHT:
      self.player_sprite.top = SCREEN_HEIGHT

    for bullet in self.bullet_list:
      hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

      if len(hit_list) > 0:
        bullet.remove_from_sprite_lists()

        for enemy in hit_list:
          enemy.health -= 1

          if enemy.health <= 0:
            enemy.remove_from_sprite_lists()
            arcade.play_sound(self.explode_sound)
          else:
            arcade.play_sound(self.hit_sound)
      
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
  game.setup()
  arcade.run()

if __name__ == "__main__":
  main()