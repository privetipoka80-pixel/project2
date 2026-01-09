from game import TheConquerorOfDungeons
from start_menu import StartMenu
import arcade


def main():
    window = arcade.Window(1000, 700, "The Conqueror of Dungeons")
    start_menu = StartMenu(TheConquerorOfDungeons)
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()
