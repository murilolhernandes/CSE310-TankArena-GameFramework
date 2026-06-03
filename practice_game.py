import arcade

# 1. Define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Basics Practice"
MOVEMENT_SPEED = 5

# 2. Create the main Game Class by inheriting from arcade.Window
class PracticeGame(arcade.Window):
  def __init__(self):
    # Initialize the parent window with our constants
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    self.tank_texture = arcade.load_texture("")
    
    # Center the window on the screen
    self.center_window()

    # Set the background color (arcade.color has tons of built-in choices)
    arcade.set_background_color(arcade.color.DARK_GREEN)

    # Setup the starting position and speed of our circle
    self.circle_x = 400
    self.circle_y = 300
    self.change_x = 0
    self.change_y = 0

  def on_draw(self):
    """ This method runs automatically every single frame to draw things to the screen """
    # Clear the screen and prepare to draw new things
    self.clear()

    # Draw a simple circle in the middle of the screen
    # Arguments: (center_x, center_y, radius, color)
    arcade.draw_circle_filled(self.circle_x, self.circle_y, 50, arcade.color.YELLOW)

  def on_update(self, delta_time):
    """ This method runs 60 times a second to update game logic """
    # Apply the movement speed to the position
    self.circle_x += self.change_x
    self.circle_y += self.change_y

    # --- BOUNDARY CHECKING ---
    # The circle's radius is 50, so we use 50 to stop exactly on the edge

    # Left edge
    if self.circle_x < 50:
      self.circle_x = 50
    
    # Right edge
    elif self.circle_x > SCREEN_WIDTH - 50:
      self.circle_x = SCREEN_WIDTH - 50

    # Bottom edge
    if self.circle_y < 50:
      self.circle_y = 50

    # Top edge
    elif self.circle_y > SCREEN_HEIGHT - 50:
      self.circle_y = SCREEN_HEIGHT - 50

  def on_key_press(self, key, modifiers):
    """ Called whenever a key is pressed """
    # Set the speed when WASD is pressed
    if key == arcade.key.W:
      self.change_y = MOVEMENT_SPEED
    elif key == arcade.key.S:
      self.change_y = -MOVEMENT_SPEED
    elif key == arcade.key.A:
      self.change_x = -MOVEMENT_SPEED
    elif key == arcade.key.D:
      self.change_x = MOVEMENT_SPEED

  def on_key_release(self, key, modifiers):
    """ Called whenever a user releases a key """
    # Stop movement when WASD is released
    if key == arcade.key.W or key == arcade.key.S:
      self.change_y = 0
    elif key == arcade.key.A or key == arcade.key.D:
      self.change_x = 0

# 3. The Main entry point to run the program
def main():
  game = PracticeGame()
  arcade.run()

# This tells Python to execute the main function when we click run
if __name__ == "__main__":
  main()
import arcade

# 1. Define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Basics Practice"

# 2. Create the main Game Class by inheriting from arcade.Window
class PracticeGame(arcade.Window):
  def __init__(self):
    # Initialize the parent window with our constants
    super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    
    # Center the window on the screen
    self.center_window()

    # Set the background color (arcade.color has tons of built-in choices)
    arcade.set_background_color(arcade.color.DARK_GREEN)

  def on_draw(self):
    """ This method runs automatically every single frame to draw things to the screen """
    # Clear the screen and prepare to draw new things
    self.clear()

    # Draw a simple circle in the middle of the screen
    # Arguments: (center_x, center_y, radius, color)
    arcade.draw_circle_filled(400, 300, 50, arcade.color.YELLOW)

# 3. The Main entry point to run the program
def main():
  game = PracticeGame()
  arcade.run()

# This tells Python to execute the main function when we click run
if __name__ == "__main__":
  main()
