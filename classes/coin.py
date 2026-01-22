from config import TILE_SCALING
import arcade
from .resources_manager import ResourceManager
SCALE = 1.5


class Coin(arcade.Sprite):
    def __init__(self, grid_x=0, grid_y=0):
        super().__init__(scale=SCALE)
        self.resuts_manager = ResourceManager()
        self.portal_path = 'assets/sprites/coin.png'
        self.frame_w = 14
        self.frame_h = 12

        self.load_animations()
        self.texture = self.idle_frames[0]
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.15

    def load_animations(self):
        portal_texture = arcade.load_texture(self.portal_path)
        self.idle_frames = []
        self.coin_sound = self.resuts_manager.coin_sound

        for i in range(6):
            frame = portal_texture.crop(
                i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.idle_frames.append(frame)

    def update_animation(self, delta_time):
        self.animation_time += delta_time
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.idle_frames)
            self.texture = self.idle_frames[self.current_frame]

    def is_get_coin(self, player):
        if arcade.check_for_collision(self, player):
            self.coin_sound.play()
            return True
        return False
