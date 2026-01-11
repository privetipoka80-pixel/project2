import arcade


class StartMenu(arcade.View):
    def __init__(self, game_window_class):
        super().__init__()
        self.game_window_class = game_window_class
        self.background_color = arcade.color.BLACK
        self.start_hovered = False
        self.exit_hovered = False
        self.records_hovered = False

        self.background_texture = None
        self.background_sprite = None

    def on_show_view(self):
        arcade.set_background_color(self.background_color)

        try:
            self.background_texture = arcade.load_texture("assets/backgrounds/menu_background.jpg")
            self.background_sprite = arcade.Sprite(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                scale=1.0
            )
            self.background_sprite.texture = self.background_texture
            scale_x = self.window.width / self.background_texture.width
            scale_y = self.window.height / self.background_texture.height
            self.background_sprite.scale = max(scale_x, scale_y)
        except:
            self.background_texture = None

    def on_draw(self):
        self.clear()

        if self.background_sprite:
            self.background_sprite.draw()
        else:
            arcade.draw_lrbt_rectangle_filled(
                0, self.window.width, 0, self.window.height,
                arcade.color.GRAY
            )

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
        records_y = self.window.height / 2 - 70
        exit_y = self.window.height / 2 - 140

        start_color = arcade.color.GREEN if self.start_hovered else arcade.color.DARK_GREEN
        records_color = arcade.color.BLUE if self.records_hovered else arcade.color.DARK_BLUE
        exit_color = arcade.color.RED if self.exit_hovered else arcade.color.DARK_RED
        border_width = 4 if self.start_hovered or self.exit_hovered or self.records_hovered else 2

        arcade.draw_lrbt_rectangle_filled(start_x - 100, start_x + 100, start_y - 25, start_y + 25, start_color)
        arcade.draw_lrbt_rectangle_outline(start_x - 100, start_x + 100, start_y - 25, start_y + 25, arcade.color.WHITE,
                                           border_width)
        arcade.draw_text(
            "СТАРТ",
            start_x,
            start_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_lrbt_rectangle_filled(start_x - 100, start_x + 100, records_y - 25, records_y + 25, records_color)
        arcade.draw_lrbt_rectangle_outline(start_x - 100, start_x + 100, records_y - 25, records_y + 25, arcade.color.WHITE,
                                           border_width)
        arcade.draw_text(
            "РЕКОРДЫ",
            start_x,
            records_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_lrbt_rectangle_filled(start_x - 100, start_x + 100, exit_y - 25, exit_y + 25, exit_color)
        arcade.draw_lrbt_rectangle_outline(start_x - 100, start_x + 100, exit_y - 25, exit_y + 25, arcade.color.WHITE,
                                           border_width)
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
        records_y = self.window.height / 2 - 70
        exit_y = self.window.height / 2 - 140

        self.start_hovered = start_x - 100 < x < start_x + 100 and start_y - 25 < y < start_y + 25
        self.records_hovered = start_x - 100 < x < start_x + 100 and records_y - 25 < y < records_y + 25
        self.exit_hovered = start_x - 100 < x < start_x + 100 and exit_y - 25 < y < exit_y + 25

    def on_mouse_press(self, x, y, button, modifiers):
        start_x = self.window.width / 2
        start_y = self.window.height / 2
        records_y = self.window.height / 2 - 70
        exit_y = self.window.height / 2 - 140

        if button == arcade.MOUSE_BUTTON_LEFT:
            if start_x - 100 < x < start_x + 100 and start_y - 25 < y < start_y + 25:
                game = self.game_window_class()
                game.setup()
                self.window.close()
                arcade.run()

            if start_x - 100 < x < start_x + 100 and records_y - 25 < y < records_y + 25:
                pass

            if start_x - 100 < x < start_x + 100 and exit_y - 25 < y < exit_y + 25:
                arcade.exit()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
