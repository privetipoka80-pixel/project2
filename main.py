import arcade
from resources_manager import ResourceManager


def main():
    resources = ResourceManager()
    resources.load_all_resources()
    window = arcade.Window(vsync=True, fullscreen=True)
    window.resources = resources
    from menu import MenuView
    menu_view = MenuView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()
