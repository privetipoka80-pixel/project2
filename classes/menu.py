import arcade
from arcade.gui import (UITextureButton, UIManager,
                        UIAnchorLayout, UIBoxLayout, UILabel)
from game import TheConquerorOfDungeons
from .resources_manager import ResourceManager


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.resources_manager = ResourceManager()
        self.background_texture = self.resources_manager.background_texture
        arcade.load_font("assets/tiles/4 GUI/TinyFontCraftpixPixel.otf")
        self.custom_font = "TinyFontCraftpixPixel"
        self.style = {"normal": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20),
                      "hover": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20),
                      "pressed": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20),
                      "press": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20), }
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
                        align="center",
                        font_name=self.custom_font)
        self.box_layout.add(label)
        start_game_button = UITextureButton(text='Start game',
                                            texture=texture_normal,
                                            texture_hovered=texture_hovered,
                                            texture_pressed=texture_pressed,
                                            scale=2.0,
                                            style=self.style
                                            )
        start_game_button.on_click = self.start_game
        self.box_layout.add(start_game_button)

        records_button = UITextureButton(text='Records',
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=2.0,
                                         font_name=self.custom_font,
                                         style=self.style
                                         )
        records_button.on_click = self.records_click
        self.box_layout.add(records_button)

        # если нажать заработает метод exit_click
        exit = UITextureButton(text='Exit',
                               texture=texture_normal,
                               texture_hovered=texture_hovered,
                               texture_pressed=texture_pressed,
                               scale=2.0,
                               style=self.style
                               )
        exit.on_click = self.exit
        self.box_layout.add(exit)

    def on_show(self):
        self.manager.enable()

    def on_hide(self):
        self.manager.disable()

    def start_game(self, event):
        self.manager.disable()
        self.game_view = TheConquerorOfDungeons()
        self.window.show_view(self.game_view)

    def exit(self, event):
        self.manager.disable()
        arcade.exit()

    def records_click(self, event):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_draw(self):
        self.clear()
        width = self.window.width
        height = self.window.height
        arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(
            width // 2, height // 2, width, height))
        self.manager.draw(pixelated=True)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.resources_manager = ResourceManager()
        self.game_view = game_view

        arcade.load_font("assets/tiles/4 GUI/TinyFontCraftpixPixel.otf")
        self.custom_font = "TinyFontCraftpixPixel"
        self.style = {"normal": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20),
                      "hover": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20),
                      "pressed": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20),
                      "press": UITextureButton.UIStyle(font_name=self.custom_font, font_size=20), }

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

        label = UILabel(text="Pause",
                        font_size=60,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center",
                        font_name=self.custom_font)
        self.box_layout.add(label)

        continue_button = UITextureButton(text='Continue',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=2.0,
                                          style=self.style
                                          )
        continue_button.on_click = self.continue_game
        self.box_layout.add(continue_button)

        main_menu_button = UITextureButton(text='Main menu',
                                           texture=texture_normal,
                                           texture_hovered=texture_hovered,
                                           texture_pressed=texture_pressed,
                                           scale=2.0,
                                           style=self.style
                                           )
        main_menu_button.on_click = self.main_menu
        self.box_layout.add(main_menu_button)

    def on_show(self):
        self.manager.enable()

    def on_hide(self):
        self.manager.disable()

    def continue_game(self, event):
        self.manager.disable()
        self.game_view.music_player.play()
        self.window.show_view(self.game_view)

    def main_menu(self, event):
        self.manager.disable()
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=self.window.width,
            top=self.window.height,
            bottom=0,
            color=(0, 0, 0, 180)
        )
        self.manager.draw()
