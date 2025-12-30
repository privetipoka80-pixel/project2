import arcade
from arcade.camera import Camera2D
from arcade.types import Color


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "The Conqueror of Dungeons"
TILE_SCALING = 3
SPEED = 5
SCALE = 0.5
CAMERA_LERP = 0.1


START_PLAYER_X = 2
START_PLAYER_y = 5


class MyGame(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        color = Color.from_hex_string('181425')
        arcade.set_background_color((color[0], color[1], color[2]))

        self.cell_size = 32

        self.all_sprites = arcade.SpriteList()

    def setup(self):

        self.don = (':resources:images/enemies/slimePurple.png')
        self.player = arcade.Sprite(self.don, SCALE)
        x2 = START_PLAYER_X * self.cell_size + self.cell_size // 2
        y2 = START_PLAYER_y * self.cell_size + self.cell_size // 2

        self.player.position = (x2, y2)
        self.all_sprites.append(self.player)

        self.world_camera = Camera2D()

        map_name = "assets/map1.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.torches_list = self.tile_map.sprite_lists["torches"]

        self.torch_frames = []
        for i in range(1, 9):
            texture = arcade.load_texture(f"assets/sprites/f{i}.png")
            self.torch_frames.append(texture)

        self.torches = arcade.SpriteList()
        for sprite in self.torches_list:
            self.torches.append(sprite)

        self.animation_timer = 0
        self.current_frame = 0
        self.animation_speed = 0.1

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list
        )

    def on_draw(self):
        """Отрисовка кадра"""
        self.clear()
        self.scene.draw(pixelated=True)
        self.player.update()
        self.all_sprites.draw(pixelated=True)
        self.torches.draw(pixelated=True)

        self.physics_engine.update()
        self.world_camera.use()

    def on_update(self, delta_time):
        """Обновление логики игры"""
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player.position),
            CAMERA_LERP,
        )
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
        if key == arcade.key.S:
            self.player.change_y = -SPEED
        if key == arcade.key.D:
            self.player.change_x = SPEED
        if key == arcade.key.A:
            self.player.change_x = -SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 0
        if key == arcade.key.S:
            self.player.change_y = 0
        if key == arcade.key.D:
            self.player.change_x = 0
        if key == arcade.key.A:
            self.player.change_x = 0


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
