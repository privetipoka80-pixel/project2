import arcade
from random import uniform, random
import time
import random
import math
SCALE = 1.7


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

        self.walk_sound_interval = 0.3

        self.frame_w = 64
        self.frame_h = 64
        self.side = 'right'
        self.load_animations()
        self.texture = self.idle_frames[0]

        self.current_frame = 0
        self.animation_time = 0

        self.animation_speeds = {
            'idle': 0.15,
            'walk': 0.05,
            'attack': 0.05
        }

        self.speed = 1.5
        self.change_x = 0  # скорость x
        self.change_y = 0  # скорость y
        self.move_timer = 0
        self.detection_range = 200

        self.state = 'idle'

        self.random_move_cooldown = 0
        self.attack_cooldown = 0
        self.random_move_chance = 0.03
        self.attack_cooldown_time = 1
        self.random_move_duration = 2
        self.chase_speed = 1.5
        self.attack_range = 50

    def load_animations(self):
        """Загружает все анимации врага"""
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
        if self.state == 'attack':
            return self.attack_frames
        elif self.state in ['walk', 'chase']:
            return self.walk_frames
        return self.idle_frames

    def update_ai(self, player, delta_time, wall_list=None):
        """Основной метод ии врага"""
        if self.random_move_cooldown > 0:
            self.random_move_cooldown -= delta_time

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance_sq = dx * dx + dy * dy

        if distance_sq < self.attack_range * self.attack_range:
            self.state = 'attack'
            self.change_x = 0
            self.change_y = 0

            if self.attack_cooldown <= 0:
                self.play_attack_sound()
                self.attack_cooldown = self.attack_cooldown_time
        elif distance_sq < self.detection_range * self.detection_range:
            distance = math.sqrt(distance_sq)
            self.state = 'chase'
            self.change_x = (dx / distance) * self.chase_speed
            self.change_y = (dy / distance) * self.chase_speed

            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.change_x > 0:
                self.side = 'right'
            elif self.change_x < 0:
                self.side = 'left'
        else:
            self.random_walk(delta_time)

        if wall_list and self.change_x != 0 and self.change_y != 0:
            self.handle_wall_collisions(wall_list)

    def handle_wall_collisions(self, wall_list):
        """Обработка столкновений врага со стенами"""
        if arcade.check_for_collision_with_list(self, wall_list):
            self.change_x *= -1
            self.change_y *= -1
            self.center_x += self.change_x * 2
            self.center_y += self.change_y * 2

            if self.change_x > 0:
                self.side = 'right'
            elif self.change_x < 0:
                self.side = 'left'

    def random_walk(self, delta_time):
        """Случайное блуждание"""
        self.move_timer += delta_time

        if random.random() < self.random_move_chance and self.random_move_cooldown <= 0:
            if self.state == 'idle':
                # движение в случайном направлении
                self.state = 'walk'
                angle = random.uniform(0, 6.28)
                self.change_x = math.cos(angle) * self.speed
                self.change_y = math.sin(angle) * self.speed
                self.random_move_cooldown = random.uniform(1, 3)
            else:
                self.state = 'idle'
                self.change_x = 0
                self.change_y = 0
                self.random_move_cooldown = random.uniform(0.5, 2)

        # по таймеру движение заканчивается
        if self.state == 'walk' and self.move_timer >= self.random_move_duration:
            self.state = 'idle'
            self.change_x = 0
            self.change_y = 0
            self.move_timer = 0
            self.random_move_cooldown = random.uniform(0.5, 2)

        # обнов позиции
        if self.state == 'walk':
            self.center_x += self.change_x
            self.center_y += self.change_y

            # направление взгляда
            if self.change_x > 0:
                self.side = 'right'
            elif self.change_x < 0:
                self.side = 'left'

    def get_current_speed(self):
        """Возвращает текущую скорость анимации"""
        if self.state == 'attack':
            return self.animation_speeds.get('attack', 0.05)
        elif self.state in ['walk', 'chase']:
            return self.animation_speeds['walk']
        else:
            return self.animation_speeds['idle']

    def generate_interval(self):
        self.walk_sound_interval = uniform(0.05, 0.4)

    def update_animation(self, delta_time):
        """Обновление анимации"""
        self.animation_time += delta_time
        current_speed = self.get_current_speed()

        if self.animation_time >= current_speed:
            self.animation_time = 0
            frames = self.get_current_frames()
            if not frames:
                return

            self.current_frame = (self.current_frame + 1) % len(frames)

            if self.state == 'attack' and self.current_frame == 0:
                # атака закончилась
                self.state = 'idle'
                self.current_frame = 0
                self.texture = self.idle_frames[0]
            else:
                self.texture = frames[self.current_frame]
                if self.side == 'left':
                    self.texture = self.texture.flip_horizontally()

    def play_attack_sound(self):
        if self.attack_cooldown <= 0:  # звук только если нет кд
            if self.next_sound_is_sound1:
                arcade.play_sound(self.sound1, volume=1)
            else:
                arcade.play_sound(self.sound2, volume=1)
            self.next_sound_is_sound1 = not self.next_sound_is_sound1
