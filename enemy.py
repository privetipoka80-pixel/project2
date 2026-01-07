import arcade
from random import uniform, random
import time
import math
SCALE = 2


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=SCALE)
        self.idle_path = 'assets/enemy/enemy4.png'
        self.walk_path = 'assets/enemy/enemy3.png'
        self.attack1_path = 'assets/enemy/enemy1.png'
        self.attack2_path = 'assets/enemy/enemy2.png'
        self.attack3_path = 'assets/enemy/enemy5.png'

        self.sound1 = arcade.load_sound('assets/sounds/ATTACK1.mp3')
        self.sound2 = arcade.load_sound('assets/sounds/ATTACK2.mp3')
        self.next_sound_is_sound1 = True

        self.next_sound_is_walk4 = True

        self.walk_sound_timer = 0
        self.walk_sound_interval = 0.3

        self.frame_w = 64
        self.frame_h = 64
        self.side = 'right'
        self.load_animations()
        self.texture = self.idle_frames[0]

        self.is_walking = False
        self.is_attacking = False

        self.current_frame = 0
        self.animation_time = 0

        self.animation_speeds = {
            'idle': 0.15,
            'walk': 0.05,
            'attack': 0.05
        }

        self.sound_played = False
        self.sound_played2 = False

        self.speed = 1.5
        self.change_x = 0  # скорость x
        self.change_y = 0  # скорость y
        self.move_timer = 0
        self.move_direction_timer = 0
        self.direction_change_interval = 2.0  # менять направление каждые 2 с
        self.current_direction = uniform(0, 6.28)
        self.last_collision_time = 0
        self.collision_cooldown = 0.3
        self.detection_range = 200

    def load_animations(self):
        """Загружает все анимации персонажа"""
        # анимация покоя
        idle_texture = arcade.load_texture(self.idle_path)
        self.idle_frames = []
        for i in range(4):
            frame = idle_texture.crop(
                i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.idle_frames.append(frame)

        # анимация ходьбы
        walk_texture = arcade.load_texture(self.walk_path)
        self.walk_frames = []
        for i in range(6):
            frame = walk_texture.crop(
                i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.walk_frames.append(frame)

        # анимация атаки
        attack1_texture = arcade.load_texture(self.attack1_path)
        self.attack_frames = []
        for i in range(6):
            frame = attack1_texture.crop(
                i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.attack_frames.append(frame)

    def get_current_frames(self):
        """Возвращает текущие кадры анимации"""
        if self.is_attacking:
            return self.attack_frames
        if self.is_walking:
            return self.walk_frames
        return self.idle_frames

    def update_movement(self, delta_time):
        """Обновляет движение врага"""
        self.move_direction_timer += delta_time

        if random() < 0.05:
            self.is_walking = not self.is_walking

            if self.is_walking:
                self.current_direction = uniform(0, 6.28)
                self.direction_change_interval = uniform(1, 3)
            else:
                self.change_x = 0
                self.change_y = 0
                return
        if not self.is_walking:
            return
        if self.move_direction_timer >= self.direction_change_interval:
            self.move_direction_timer = 0
            self.current_direction = uniform(0, 6.28)
            self.direction_change_interval = uniform(1, 3)

        self.change_x = math.cos(self.current_direction) * self.speed
        self.change_y = math.sin(self.current_direction) * self.speed
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.side = 'right'
        elif self.change_x < 0:
            self.side = 'left'

    def bounce_from_wall(self):
        """Отходит от стены при столкновении"""
        self.current_direction += math.pi
        self.current_direction += uniform(-0.5, 0.5)

        self.move_direction_timer = 0

    def update_ai(self, player, delta_time, wall_list=None):
        """Основной метод ии врага"""
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance_to_player = math.sqrt(dx * dx + dy * dy)
        if distance_to_player < self.detection_range:
            angle_to_player = math.atan2(dy, dx)
            self.current_direction = angle_to_player
            self.speed = 2.0
            if distance_to_player > 50:
                self.is_walking = True
            else:
                self.is_walking = False
                self.change_x = 0
                self.change_y = 0
                self.attack()
        else:
            self.update_movement(delta_time)
            self.speed = 1.5
        if wall_list and self.is_walking:
            if arcade.check_for_collision_with_list(self, wall_list):
                current_time = time.time()
                if current_time - self.last_collision_time > self.collision_cooldown:
                    self.bounce_from_wall()
                    self.last_collision_time = current_time
                    self.is_walking = False
                    self.change_x = 0
                    self.change_y = 0

    def get_current_speed(self):
        """Возвращает текущую скорость анимации"""
        if self.is_attacking:
            return self.animation_speeds.get('attack', 0.05)
        elif self.is_walking:
            return self.animation_speeds['walk']
        else:
            return self.animation_speeds['idle']

    def generate_interval(self):
        self.walk_sound_interval = uniform(0.05, 0.4)

    def update_animation(self, delta_time):
        """Обновление анимации"""
        self.animation_time += delta_time
        current_speed = self.get_current_speed()

        if self.is_walking:
            self.walk_sound_timer += delta_time
            self.generate_interval()
            if self.walk_sound_timer >= self.walk_sound_interval:
                self.walk_sound_timer = 0

        if self.animation_time >= current_speed:
            self.animation_time = 0
            frames = self.get_current_frames()
            if not frames:
                return
            self.current_frame = (self.current_frame + 1) % len(frames)
            if self.is_attacking and self.current_frame == 0:
                self.is_attacking = False
                self.current_frame = 0
                self.texture = self.idle_frames[0]
            else:
                self.texture = frames[self.current_frame]
                if self.side == 'left':
                    self.texture = self.texture.flip_horizontally()

    def play_attack_sound(self):
        if not self.sound_played:
            if self.next_sound_is_sound1:
                arcade.play_sound(self.sound1, volume=1)
            else:
                arcade.play_sound(self.sound2, volume=1)
            self.next_sound_is_sound1 = not self.next_sound_is_sound1
            self.sound_played = True

    def attack(self):
        """Начать атаку"""
        if not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.animation_time = 0
            self.sound_played = False
            self.change_x = 0
            self.change_y = 0
            self.is_walking = False
            self.play_attack_sound()

    def start_walking(self):
        """Начать анимацию ходьбы"""
        self.is_walking = True
        self.current_frame = 0
        self.animation_time = 0

    def stop_walking(self):
        """Остановить анимацию ходьбы"""
        self.is_walking = False
        self.current_frame = 0
        self.animation_time = 0
        self.texture = self.idle_frames[0]
