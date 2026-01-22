from classes.generate_enemy import Generate_enemy
import arcade
from arcade.camera import Camera2D
from arcade.types import Color
from classes.player import Player
from config import *
from classes.portal import Portal
from classes.resources_manager import ResourceManager
import os


class TheConquerorOfDungeons(arcade.View):
    def __init__(self):
        super().__init__()
        color = Color.from_hex_string('181425')
        arcade.set_background_color((color[0], color[1], color[2]))
        self.resources_manager = ResourceManager()

        self.cell_size = 80 * 16 * TILE_SCALING // 5

        self.all_sprites = arcade.SpriteList()
        self.portal_sprite = arcade.SpriteList()
        self.enemies = Generate_enemy()

        self.coords_enemy = MAP1_SPAWN_ENEMY_COORD
        self.coords_player = MAP1_SPAWN_PLAYER_COORD
        self.lvl = 0
        self.player = Player()
        self.all_sprites.append(self.player)

        for x, y in self.coords_enemy:
            for _ in range(10):
                self.enemies.spawn_in_grid(x, y)

        self.tile_map1 = self.resources_manager.tile_map1
        self.tile_map2 = self.resources_manager.tile_map2
        self.tile_map3 = self.resources_manager.tile_map3
        self.boss_map = self.resources_manager.boss_map

        self.scene1 = arcade.Scene.from_tilemap(self.tile_map1)
        self.scene2 = arcade.Scene.from_tilemap(self.tile_map2)
        self.scene3 = arcade.Scene.from_tilemap(self.tile_map3)
        self.scene4 = arcade.Scene.from_tilemap(self.boss_map)

        self.tile_map = self.tile_map1
        self.scene = self.scene1

        self.portal = None
        self.portal_spawned = False
        self.setup()
        self.background_music = self.resources_manager.background_music

        self.music_player = arcade.play_sound(
            self.background_music,
            volume=0.1,
            loop=True
        )
        self.balance = 0
        self.balance_file = 'balance.txt'
        try:
            with open(self.balance_file, 'r', encoding='utf-8') as f:
                self.balance = int(f.read())
        except:
            self.balance = 0
            with open(self.balance_file, 'w', encoding='utf-8') as f:
                f.write('0')

    def setup(self):
        self.spawn_player(self.coords_player[0], self.coords_player[1])
        self.world_camera = Camera2D()
        self.ui_camera = Camera2D()

        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.torches_list = self.tile_map.sprite_lists["torches"]
        self.details_list = self.tile_map.sprite_lists["details"]

        self.torch_frames = self.resources_manager.torch_frames
        self.torches = arcade.SpriteList()

        for torch_sprite in self.torches_list:
            self.torches.append(torch_sprite)

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

    def spawn_portal(self, grid_x, grid_y):
        x = grid_x * self.cell_size + self.cell_size // 2
        y = grid_y * self.cell_size + self.cell_size // 2
        self.portal = Portal()
        self.portal.center_x = x
        self.portal.center_y = y
        self.portal_sprite.append(self.portal)
        self.portal_spawned = True

    def on_draw(self):
        """Отрисовка кадра"""
        self.clear()
        self.world_camera.use()
        self.scene.draw(pixelated=True)
        self.portal_sprite.draw(pixelated=True)
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

        enemies_to_remove = []
        for enemy in self.enemies:
            if enemy.health > 0:
                enemy.update_ai(self.player, delta_time, self.wall_list)
                if enemy.damag_to_enemy(self.player):
                    self.player.health -= enemy.damag
            enemy.update_animation(delta_time)
            if self.player.damag_to_player(enemy):
                enemy.health -= self.player.damag
            if enemy.health <= 0 and enemy.is_dead:
                enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

        if not self.enemies and not self.portal_spawned:
            if self.lvl == 0:
                self.spawn_portal(0, 4)
            elif self.lvl == 1:
                self.spawn_portal(4, 4)
            elif self.lvl == 2:
                self.spawn_portal(0, 0)

        if self.portal and self.portal_spawned:
            if self.portal.is_in_portal(self.player):
                self.handle_level_transition()
        if self.portal:
            self.portal.update_animation(delta_time)

        self.player.update_animation(delta_time)

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.torch_frames)
            for torch in self.torches:
                torch.texture = self.torch_frames[self.current_frame]

        if self.player.health <= 0:
            self.lvl = 0
            self.enemies.clear()
            self.portal = None
            self.portal_sprite.clear()
            self.portal_spawned = False
            self.tile_map = self.tile_map1
            self.scene = self.scene1
            self.coords_player = MAP1_SPAWN_PLAYER_COORD
            self.coords_enemy = MAP1_SPAWN_ENEMY_COORD
            self.wall_list = self.tile_map.sprite_lists["walls"]
            self.details_list = self.tile_map.sprite_lists["details"]
            self.torches.clear()
            if "torches" in self.tile_map.sprite_lists:
                for sprite in self.tile_map.sprite_lists["torches"]:
                    self.torches.append(sprite)
            for x, y in self.coords_enemy:
                for _ in range(10):
                    self.enemies.spawn_in_grid(x, y)
            self.spawn_player(self.coords_player[0], self.coords_player[1])
            self.player.health = PLAYER_HEALTH
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player, self.wall_list)
            self.physics_engine2 = arcade.PhysicsEngineSimple(
                self.player, self.details_list)
            self.world_camera.position = self.player.position

    def handle_level_transition(self):
        self.portal = None
        self.portal_sprite.clear()
        self.portal_spawned = False

        self.lvl += 1

        if self.lvl == 1:
            self.tile_map = self.tile_map2
            self.scene = self.scene2
            self.coords_enemy = MAP2_SPAWN_ENEMY_COORD
            self.coords_player = MAP2_SPAWN_PLAYER_COORD
            self.next_level()

        elif self.lvl == 2:
            self.tile_map = self.tile_map3
            self.scene = self.scene3
            self.coords_enemy = MAP3_SPAWN_ENEMY_COORD
            self.coords_player = MAP3_SPAWN_PLAYER_COORD
            self.next_level()

        elif self.lvl == 3:
            self.tile_map = self.boss_map
            self.scene = self.scene4
            self.coords_player = (1, 1)
            self.enemies.spawn_boss_in_grid(2, 2)
            self.player.health = self.player.max_health
            self.next_level()

        elif self.lvl == 4:
            pass

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
            self.player.is_walking = True
        if key == arcade.key.K:
            self.player.attack()
        if key == arcade.key.ESCAPE:
            from classes.menu import PauseView
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
            self.music_player.pause()

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
        super().on_mouse_press(x, y, button, modifiers)
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.attack()

    def next_level(self):
        if self.lvl != 3:
            for x, y in self.coords_enemy:
                for _ in range(10):
                    self.enemies.spawn_in_grid(x, y)

        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.details_list = self.tile_map.sprite_lists["details"]

        self.torches.clear()
        if "torches" in self.tile_map.sprite_lists:
            for sprite in self.tile_map.sprite_lists["torches"]:
                self.torches.append(sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(
            self.player, self.details_list)

        self.world_camera.position = self.player.position
        self.setup()
