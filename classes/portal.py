from config import TILE_SCALING
import arcade

SCALE = 5


class Portal(arcade.Sprite):
    def __init__(self, grid_x=0, grid_y=0):
        super().__init__(scale=SCALE)

        self.portal_path = 'assets/sprites/portal.png'
        self.frame_w = 32
        self.frame_h = 32

        self.load_animations()
        self.texture = self.idle_frames[0]
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.15
        self.cell_size = 80 * 16 * TILE_SCALING // 5
        self.set_position(grid_x, grid_y)

    def load_animations(self):
        portal_texture = arcade.load_texture(self.portal_path)
        self.idle_frames = []

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

    def set_position(self, grid_x, grid_y):
        x = grid_x * self.cell_size + self.cell_size // 2
        y = grid_y * self.cell_size + self.cell_size // 2
        self.center_x = x
        self.center_y = y

    def is_in_portal(self, player):
        if arcade.check_for_collision(self, player):
            return True
        return False
