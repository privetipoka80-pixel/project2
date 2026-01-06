import arcade

SCALE = 2

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=SCALE)
        
        self.idle_path = 'assets/player/IDLE.png'
        self.walk_path = 'assets/player/WALK.png'
        self.attack1_path = 'assets/player/ATTACK1.png'
        self.attack2_path = 'assets/player/ATTACK2.png'
        self.attack3_path = 'assets/player/ATTACK3.png'
        
        self.frame_w = 96
        self.frame_h = 84
        self.side = 'right'
        self.load_animations()

        self.texture = self.idle_frames[0]

        self.is_walking = False
        self.is_attacking = False
        self.current_attack = None
        
        self.attack_sequence = ['attack1', 'attack2', 'attack3']
        self.current_attack_index = 0
        
        self.current_frame = 0
        self.animation_time = 0

        self.animation_speeds = {
            'idle': 0.15,
            'walk': 0.05,
            'attack1': 0.05,
            'attack2': 0.05,
            'attack3': 0.05,
        }
        
    def load_animations(self):
        """Загружает все анимации персонажа"""
        # анимация покоя
        idle_texture = arcade.load_texture(self.idle_path)
        self.idle_frames = []
        for i in range(7):
            frame = idle_texture.crop(i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.idle_frames.append(frame)
        
        # анимация ходьбы
        walk_texture = arcade.load_texture(self.walk_path)
        self.walk_frames = []
        for i in range(6):
            frame = walk_texture.crop(i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.walk_frames.append(frame)
        
        # анимация атаки 1
        attack1_texture = arcade.load_texture(self.attack1_path)
        self.attack1_frames = []
        for i in range(6):
            frame = attack1_texture.crop(i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.attack1_frames.append(frame)
        
        # анимация атаки 2
        attack2_texture = arcade.load_texture(self.attack2_path)
        self.attack2_frames = []
        for i in range(5):
            frame = attack2_texture.crop(i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.attack2_frames.append(frame)
        
        # анимация атаки 3
        attack3_texture = arcade.load_texture(self.attack3_path)
        self.attack3_frames = []
        for i in range(6):
            frame = attack3_texture.crop(i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.attack3_frames.append(frame)

        self.texture = self.idle_frames[0]
    
    def get_current_frames(self):
        """Возвращает текущие кадры анимации"""
        if self.is_attacking and self.current_attack:
            if self.current_attack == 'attack1':
                return self.attack1_frames
            elif self.current_attack == 'attack2':
                return self.attack2_frames
            elif self.current_attack == 'attack3':
                return self.attack3_frames
        
        if self.is_walking:
            return self.walk_frames
        
        return self.idle_frames
    
    def get_current_speed(self):
        """Возвращает текущую скорость анимации"""
        if self.is_attacking and self.current_attack:
            return self.animation_speeds.get(self.current_attack, 0.05)
        elif self.is_walking:
            return self.animation_speeds['walk']
        else:
            return self.animation_speeds['idle']
    
    def update_animation(self, delta_time: float):
        """Обновление анимации"""
        self.animation_time += delta_time
        current_speed = self.get_current_speed()

        if self.animation_time >= current_speed:
            self.animation_time = 0
            
            frames = self.get_current_frames()
            if not frames:
                return
            
            self.current_frame = (self.current_frame + 1) % len(frames)

            if self.is_attacking and self.current_frame == 0:
                self.is_attacking = False
                self.current_attack = None
                self.current_frame = 0
                self.texture = self.idle_frames[0]
            else:
                self.texture = frames[self.current_frame]
                if self.side == 'left':
                    self.texture = self.texture.flip_horizontally()
    
    def attack(self):
        if not self.is_attacking:
            self.current_attack = self.attack_sequence[self.current_attack_index]

            self.current_attack_index = (self.current_attack_index + 1) % len(self.attack_sequence)

            self.is_attacking = True
            self.current_frame = 0
            self.animation_time = 0
            
            # print(f"атака {self.current_attack}")
    
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