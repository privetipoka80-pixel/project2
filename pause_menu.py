import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

class PauseMenu(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        arcade.draw_text(
            "ПАУЗА",
            self.window.width / 2,
            self.window.height / 2 + 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

        continue_x = self.window.width / 2
        continue_y = self.window.height / 2
        main_menu_y = self.window.height / 2 - 70

        arcade.draw_lrbt_rectangle_filled(continue_x - 150, continue_x + 150, continue_y - 25, continue_y + 25, arcade.color.DARK_GREEN)
        arcade.draw_lrbt_rectangle_outline(continue_x - 150, continue_x + 150, continue_y - 25, continue_y + 25, arcade.color.WHITE, 2)
        arcade.draw_text(
            "ПРОДОЛЖИТЬ",
            continue_x,
            continue_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_lrbt_rectangle_filled(continue_x - 150, continue_x + 150, main_menu_y - 25, main_menu_y + 25, arcade.color.DARK_BLUE)
        arcade.draw_lrbt_rectangle_outline(continue_x - 150, continue_x + 150, main_menu_y - 25, main_menu_y + 25, arcade.color.WHITE, 2)
        arcade.draw_text(
            "ГЛАВНОЕ МЕНЮ",
            continue_x,
            main_menu_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        continue_x = self.window.width / 2
        continue_y = self.window.height / 2
        main_menu_y = self.window.height / 2 - 70

        if continue_x - 150 < x < continue_x + 150 and continue_y - 25 < y < continue_y + 25:
            self.window.close()
            import game
            game_window = game.TheConquerorOfDungeons()
            game_window.setup()
            game_window.run()

        if continue_x - 150 < x < continue_x + 150 and main_menu_y - 25 < y < main_menu_y + 25:
            self.window.close()
            import start_menu
            window = arcade.Window(1000, 700, "The Conqueror of Dungeons", fullscreen=True)
            menu = start_menu.StartMenu(window)
            window.show_view(menu)
            arcade.run()