import arcade


class StartMenu(arcade.View):
    def __init__(self, game_window_class):
        super().__init__()
        self.game_window_class = game_window_class
        self.background_color = arcade.color.BLACK
        self.start_hovered = False
        self.exit_hovered = False

    def on_show_view(self):
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "The Conqueror of Dungeons",
            self.window.width / 2,
            self.window.height / 2 + 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )

        start_x = self.window.width / 2
        start_y = self.window.height / 2
        exit_y = self.window.height / 2 - 70

        start_color = arcade.color.GREEN if self.start_hovered else arcade.color.DARK_GREEN
        exit_color = arcade.color.RED if self.exit_hovered else arcade.color.DARK_RED
        border_width = 4 if self.start_hovered or self.exit_hovered else 2

        arcade.draw_lrbt_rectangle_filled(start_x - 100, start_x + 100, start_y - 25, start_y + 25, start_color)
        arcade.draw_lrbt_rectangle_outline(start_x - 100, start_x + 100, start_y - 25, start_y + 25, arcade.color.WHITE, border_width)
        arcade.draw_text(
            "СТАРТ",
            start_x,
            start_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_lrbt_rectangle_filled(start_x - 100, start_x + 100, exit_y - 25, exit_y + 25, exit_color)
        arcade.draw_lrbt_rectangle_outline(start_x - 100, start_x + 100, exit_y - 25, exit_y + 25, arcade.color.WHITE, border_width)
        arcade.draw_text(
            "ВЫХОД",
            start_x,
            exit_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_motion(self, x, y, dx, dy):
        start_x = self.window.width / 2
        start_y = self.window.height / 2
        exit_y = self.window.height / 2 - 70

        self.start_hovered = start_x - 100 < x < start_x + 100 and start_y - 25 < y < start_y + 25
        self.exit_hovered = start_x - 100 < x < start_x + 100 and exit_y - 25 < y < exit_y + 25

    def on_mouse_press(self, x, y, button, modifiers):
        start_x = self.window.width / 2
        start_y = self.window.height / 2
        exit_y = self.window.height / 2 - 70

        if button == arcade.MOUSE_BUTTON_LEFT:
            if start_x - 100 < x < start_x + 100 and start_y - 25 < y < start_y + 25:
                game = self.game_window_class()
                game.setup()
                self.window.close()
                arcade.run()

            if start_x - 100 < x < start_x + 100 and exit_y - 25 < y < exit_y + 25:
                arcade.exit()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
