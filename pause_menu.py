import arcade



class PauseMenu(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.continue_hovered = False
        self.main_menu_hovered = False

        self.background_texture = None
        self.background_sprite = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

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
            "ПАУЗА",
            self.window.width / 2,
            self.window.height / 2 + 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )

        continue_x = self.window.width / 2
        continue_y = self.window.height / 2
        main_menu_y = self.window.height / 2 - 70

        continue_color = arcade.color.GREEN if self.continue_hovered else arcade.color.DARK_GREEN
        main_menu_color = arcade.color.BLUE if self.main_menu_hovered else arcade.color.DARK_BLUE
        border_width = 4 if self.continue_hovered or self.main_menu_hovered else 2

        arcade.draw_lrbt_rectangle_filled(continue_x - 150, continue_x + 150, continue_y - 25, continue_y + 25,
                                          continue_color)
        arcade.draw_lrbt_rectangle_outline(continue_x - 150, continue_x + 150, continue_y - 25, continue_y + 25,
                                           arcade.color.WHITE, border_width)
        arcade.draw_text(
            "ПРОДОЛЖИТЬ",
            continue_x,
            continue_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_lrbt_rectangle_filled(continue_x - 150, continue_x + 150, main_menu_y - 25, main_menu_y + 25,
                                          main_menu_color)
        arcade.draw_lrbt_rectangle_outline(continue_x - 150, continue_x + 150, main_menu_y - 25, main_menu_y + 25,
                                           arcade.color.WHITE, border_width)
        arcade.draw_text(
            "ГЛАВНОЕ МЕНЮ",
            continue_x,
            main_menu_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_motion(self, x, y, dx, dy):
        continue_x = self.window.width / 2
        continue_y = self.window.height / 2
        main_menu_y = self.window.height / 2 - 70

        self.continue_hovered = continue_x - 150 < x < continue_x + 150 and continue_y - 25 < y < continue_y + 25
        self.main_menu_hovered = continue_x - 150 < x < continue_x + 150 and main_menu_y - 25 < y < main_menu_y + 25

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
