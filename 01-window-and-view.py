import arcade

window = arcade.Window(title="Tank Arena")
# window.set_location(700, 400)
window.center_window()

class GameView(arcade.View):
  def __init__(self) -> None:
    super().__init__()

game = GameView()
window.show_view(game)
arcade.run()