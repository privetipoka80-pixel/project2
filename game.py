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

        self.maps = ["assets/map1.tmx", "assets/map2.tmx", "assets/map3.tmx"]
        self.map_name = "assets/map1.tmx"
        self.coords_enemy = MAP1_SPAWN_ENEMY_COORD
        self.coords_player = MAP1_SPAWN_PLAYER_COORD
        self.lvl = 1
        self.player = Player()
        self.all_sprites.append(self.player)

        for x, y in self.coords_enemy:
            for _ in range(10):
                self.enemies.spawn_in_grid(x, y)

        self.tile_map1 = arcade.load_tilemap(
            self.maps[0], scaling=TILE_SCALING)
        self.tile_map2 = arcade.load_tilemap(
            self.maps[1], scaling=TILE_SCALING)
        self.tile_map3 = arcade.load_tilemap(
            self.maps[2], scaling=TILE_SCALING)

        self.scene1 = arcade.Scene.from_tilemap(self.tile_map1)
        self.scene2 = arcade.Scene.from_tilemap(self.tile_map2)
        self.scene3 = arcade.Scene.from_tilemap(self.tile_map3)

        self.tile_map = self.tile_map1
        self.scene = self.scene1

        self.enemies.spawn_boss_in_grid(x, y)
        self.setup()

    def setup(self):
        self.background_music = arcade.load_sound('assets/sounds/MUSIC.mp3')

        # self.music_player = arcade.play_sound(
        #     self.background_music,
        #     volume=0.3,
        #     loop=True
        # )

        self.spawn_player(self.coords_player[0], self.coords_player[1])
        self.world_camera = Camera2D()
        self.ui_camera = Camera2D()

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
        self.world_camera.use()
        self.scene.draw(pixelated=True)
        self.all_sprites.draw(pixelated=True)
        self.torches.draw(pixelated=True)
        self.enemies.draw(pixelated=True)

        self.ui_camera.use()
        self.draw_hp_bar()

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
            if enemy.health <= 0 and enemy.is_dead:
                self.enemies.remove(enemy)

            if self.player.damag_to_player(enemy):
                enemy.health -= self.player.damag

        print(self.player.health)
        if not self.enemies:
            self.tile_map = self.tile_map2
            self.scene = self.scene2
            self.lvl += 1
            if self.lvl == 2:
                self.map_name = self.maps[1]
                self.coords_enemy = MAP2_SPAWN_ENEMY_COORD
                self.coords_player = MAP2_SPAWN_PLAYER_COORD
                self.next_level()

        if self.player.health <= 0:
            self.spawn_player(
                MAP1_SPAWN_PLAYER_COORD[0], MAP1_SPAWN_PLAYER_COORD[1])
            self.player.health = PLAYER_HEALTH
            self.tile_map = self.tile_map1
            self.scene = self.scene1

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

    def draw_hp_bar(self):
        hp_ratio = max(0, self.player.health / self.player.max_health)

        bar_w = 300
        bar_h = 20
        x = 20
        y = self.window.height - 40
        arcade.draw_lbwh_rectangle_filled(
            x, y, bar_w, bar_h, arcade.color.DARK_RED)
        arcade.draw_lbwh_rectangle_filled(
            x, y, bar_w * hp_ratio, bar_h, arcade.color.RED)
        arcade.draw_lrbt_rectangle_outline(
            x, x + bar_w, y, y + bar_h, arcade.color.BLACK, 2)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.A or key == arcade.key.D:
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
        if key == arcade.key.ESCAPE:
            from menu import PauseView
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

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

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def next_level(self):
        self.spawn_player(self.coords_player[0], self.coords_player[1])

        for x, y in self.coords_enemy:
            for _ in range(10):
                self.enemies.spawn_in_grid(x, y)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(
            self.player, self.details_list)

        self.world_camera.position = self.player.position

        self.setup()
