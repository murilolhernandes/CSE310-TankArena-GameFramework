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
