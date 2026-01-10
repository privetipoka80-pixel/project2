import arcade
from menu import MenuView


def main():
    window = arcade.Window(vsync=True, fullscreen=True)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
