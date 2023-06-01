"""Runner for text version of Twenty One Bust."""
from controller.twenty_one_bust import console_controller as controller

if __name__ == "__main__":
    game = controller.ConsoleController()
    game.run()
