# pip install pytiled-parser[zstd]
from generate_enemy import Generate_enemy
import arcade
from arcade.camera import Camera2D
from arcade.types import Color
from player import Player
from config import *


class TheConquerorOfDungeons(arcade.View):
    def __init__(self):
        super().__init__()
        color = Color.from_hex_string('181425')
        arcade.set_background_color((color[0], color[1], color[2]))

        self.cell_size = 80 * 16 * TILE_SCALING // 5

        self.all_sprites = arcade.SpriteList()
        self.enemies = Generate_enemy()
        self.setup()

    def setup(self):
        self.background_music = arcade.load_sound('assets/sounds/MUSIC.mp3')

        # self.music_player = arcade.play_sound(
        #     self.background_music,
        #     volume=0.3,
        #     loop=True
        # )

        self.player = Player()
        self.spawn_player(4, 4)
        self.all_sprites.append(self.player)
        for i in range(10):
            self.enemies.spawn_in_grid(2, 0)
        for i in range(10):
            self.enemies.spawn_in_grid(2, 2)
        for i in range(10):
            self.enemies.spawn_in_grid(2, 4)

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
        self.all_sprites.draw(pixelated=True)
        self.torches.draw(pixelated=True)
        self.world_camera.use()
        self.enemies.draw(pixelated=True)

    def on_update(self, delta_time):
        """Обновление логики игры"""
        self.player.update()
        self.physics_engine.update()
        self.physics_engine2.update()

        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player.position),
            CAMERA_LERP)
        for enemy in self.enemies:
            enemy.update_ai(self.player, delta_time, self.wall_list)
            enemy.update_animation(delta_time)
            if enemy.damag_to_enemy(self.player):
                self.player.health -= enemy.damag
            if enemy.health <= 0:
                self.enemies.remove(enemy)

            if self.player.damag_to_player(enemy):
                enemy.health -= self.player.damag

        print(self.player.health)

        if self.player.health <= 0:
            self.all_sprites.remove(self.player)
            self.player = Player()
            self.spawn_player(4, 4)
            self.all_sprites.append(self.player)
            self.player.health = PLAYER_HEALTH

            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player, self.wall_list)
            self.physics_engine2 = arcade.PhysicsEngineSimple(
                self.player, self.details_list)

            self.world_camera.position = self.player.position

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
            self.player.w_pressed = True
            self.player.change_y = SPEED
        if key == arcade.key.S:
            self.player.s_pressed = True
            self.player.change_y = -SPEED
        if key == arcade.key.D:
            self.player.d_pressed = True
            self.player.side = 'right'
            self.player.change_x = SPEED
        if key == arcade.key.A:
            self.player.a_pressed = True
            self.player.side = 'left'
            self.player.change_x = -SPEED
        if key == arcade.key.K:
            self.player.attack()

        self.player.is_walking = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player.w_pressed = False
            self.player.change_y = -SPEED if self.player.s_pressed else 0
        if key == arcade.key.S:
            self.player.s_pressed = False
            self.player.change_y = SPEED if self.player.w_pressed else 0
        if key == arcade.key.D:
            self.player.d_pressed = False
            self.player.change_x = -SPEED if self.player.a_pressed else 0
            if self.player.change_x < 0:
                self.player.side = 'left'
        if key == arcade.key.A:
            self.player.a_pressed = False
            self.player.change_x = SPEED if self.player.d_pressed else 0
            if self.player.change_x > 0:
                self.player.side = 'right'

        if self.player.change_x == 0 and self.player.change_y == 0:
            self.player.is_walking = False
            self.player.curr_texture_index = 0
