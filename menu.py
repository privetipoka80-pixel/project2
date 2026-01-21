import arcade
from arcade.gui import (UITextureButton, UIManager,
                        UIAnchorLayout, UIBoxLayout, UILabel)
from game import TheConquerorOfDungeons
from resources_manager import ResourceManager


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ARSENIC
        self.resources_manager = ResourceManager()

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(
            self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):

        texture_normal = self.resources_manager.TEXTURE_NORMAL
        texture_hovered = self.resources_manager.TEXTURE_HOVERED
        texture_pressed = self.resources_manager.TEXTURE_PRESSED

        label = UILabel(text="The Conqueror of Dungeons",
                        font_size=60,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        start_game_button = UITextureButton(text='Старт',
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=2.0,
                                            font_name='arial'
                                            )
        start_game_button.on_click = self.start_game
        self.box_layout.add(start_game_button)

        records_button = UITextureButton(text='Рекорды',
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=2.0,
                                         )
        records_button.on_click = self.records_click
        self.box_layout.add(records_button)

        # если нажать заработает метод exit_click
        exit = UITextureButton(text='Выход',
                               texture=texture_normal,
                               texture_hovered=texture_hovered,
                               texture_pressed=texture_pressed,
                               scale=2.0,
                               )
        exit.on_click = self.exit
        self.box_layout.add(exit)

    def start_game(self, event):
        self.game_view = TheConquerorOfDungeons()
        self.window.show_view(self.game_view)

    def exit(self, event):
        arcade.exit()

    def records_click(self, event):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.background_color = arcade.color.ARSENIC
        self.resources_manager = ResourceManager()
        self.game_view = game_view

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(
            self.box_layout, anchor_x="center", anchor_y="center")
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        texture_normal = self.resources_manager.TEXTURE_NORMAL
        texture_hovered = self.resources_manager.TEXTURE_HOVERED
        texture_pressed = self.resources_manager.TEXTURE_PRESSED

        label = UILabel(text="Пауза",
                        font_size=60,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        continue_button = UITextureButton(text='Продолжить',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=2.0)
        continue_button.on_click = self.continue_game
        self.box_layout.add(continue_button)

        main_menu_button = UITextureButton(text='Главное меню',
                                           texture=texture_normal,
                                           texture_hovered=texture_hovered,
                                           texture_pressed=texture_pressed,
                                           scale=2.0)
        main_menu_button.on_click = self.main_menu
        self.box_layout.add(main_menu_button)

    def continue_game(self, event):
        self.game_view.music_player.play()
        self.window.show_view(self.game_view)

    def main_menu(self, event):
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()
