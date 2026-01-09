# pip install pytiled-parser[zstd]
from generate_enemy import Generate_enemy
import arcade
from arcade.camera import Camera2D
from arcade.types import Color
from player import Player
from start_menu import StartMenu

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "The Conqueror of Dungeons"
TILE_SCALING = 3
SPEED = 2
SCALE = 0.5
CAMERA_LERP = 0.1


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,
                         SCREEN_TITLE, vsync=True, fullscreen=True)
        color = Color.from_hex_string('181425')
        arcade.set_background_color((color[0], color[1], color[2]))

        self.cell_size = 512
        self.all_sprites = arcade.SpriteList()
        self.enemies = Generate_enemy()
        self.set_update_rate(1/144)

    def setup(self):
        self.background_music = arcade.load_sound('assets/sounds/MUSIC.mp3')

        # self.music_player = arcade.play_sound(
        #     self.background_music,
        #     volume=0.3,
        #     loop=True
        # )

        self.player = Player()
        self.spawn_player(3, 3)
        self.all_sprites.append(self.player)
        for i in range(10):
            self.enemies.spawn_in_grid(3, 2)
        for i in range(10):
            self.enemies.spawn_in_grid(3, 3)
        for i in range(10):
            self.enemies.spawn_in_grid(3, 5)

        self.world_camera = Camera2D()

        map_name = "assets/map2.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.torches_list = self.tile_map.sprite_lists["torches"]
        self.details_list = self.tile_map.sprite_lists["details"]

        self.torch_frames = []
        self.torches = arcade.SpriteList()

        for i in range(1, 9):
            texture = arcade.load_texture(f"assets/sprites/f{i}.png")
            self.torch_frames.append(texture)

        for sprite in self.torches_list:
            self.torches.append(sprite)

        self.animation_timer = 0
        self.current_frame = 0
        self.animation_speed = 0.1

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(
            self.player, self.details_list)

    def spawn_player(self, grid_x, grid_y):
        """Спавн игрока в сетке комнат/коридоров"""
        x = grid_x * self.cell_size + self.cell_size // 2
        y = grid_y * self.cell_size + self.cell_size // 2
        self.player.center_x = x
        self.player.center_y = y

    def on_draw(self):
        """Отрисовка кадра"""
        self.clear()
        self.scene.draw(pixelated=True)
        self.player.update()
        self.all_sprites.draw(pixelated=True)
        self.torches.draw(pixelated=True)
        self.physics_engine.update()
        self.physics_engine2.update()
        self.world_camera.use()
        self.enemies.draw(pixelated=True)

    def on_update(self, delta_time):
        """Обновление логики игры"""
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player.position),
            CAMERA_LERP)
        for enemy in self.enemies:
            enemy.update_ai(self.player, delta_time, self.wall_list)
            enemy.update_animation(delta_time)

        self.player.update_animation(delta_time)
        self.animation_timer += delta_time

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.torch_frames)

            for torch in self.torches:
                torch.texture = self.torch_frames[self.current_frame]

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = SPEED
            self.player.is_walking = True
        if key == arcade.key.S:
            self.player.change_y = -SPEED
            self.player.is_walking = True
        if key == arcade.key.D:
            self.player.side = 'right'
            self.player.change_x = SPEED
            self.player.is_walking = True
        if key == arcade.key.A:
            self.player.side = 'left'
            self.player.change_x = -SPEED
            self.player.is_walking = True

        if key == arcade.key.K:
            self.player.attack()

    def on_key_release(self, key, modifiers):
        # print(self.player.position)
        if key == arcade.key.W:
            self.player.change_y = 0
        if key == arcade.key.S:
            self.player.change_y = 0
        if key == arcade.key.D:
            self.player.side = 'right'
            self.player.change_x = 0
        if key == arcade.key.A:
            self.player.side = 'left'
            self.player.change_x = 0

        if self.player.change_x == 0 and self.player.change_y == 0:
            self.player.is_walking = False
            self.player.curr_texture_index = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, vsync=True, fullscreen=True)
    start_menu = StartMenu(MyGame)
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()
