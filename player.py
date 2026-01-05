import arcade

SCALE = 2

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=SCALE)
        self.idle_path = 'assets/player/IDLE.png'
        self.walk_path = 'assets/player/WALK.png'

        self.side = 'right'
        self.load_animations()

        self.texture = self.idle_frames[0]

        self.curr_texture_index = 0
        self.change_time = 0.0
        self.time = 0.1
        self.is_walking = False
    
    def load_animations(self):
        """Загружает анимации"""
        frame_w = 96
        frame_h = 84

        # анимация покоя
        idle_texture = arcade.load_texture(self.idle_path)
        self.idle_frames = []
        for i in range(7):
            frame = idle_texture.crop(i * frame_w, 0, frame_w, frame_h)
            self.idle_frames.append(frame)

        # анимация ходьбы
        walk_texture = arcade.load_texture(self.walk_path)
        self.walk_frames = []
        for i in range(8):
            frame = walk_texture.crop(i * frame_w, 0, frame_w, frame_h)
            self.walk_frames.append(frame)
    
    def get_current_frames(self):
        """Возвращает текущие кадры анимации"""
        return self.walk_frames if self.is_walking else self.idle_frames
    
    """Обновление анимации игрока"""
    def update_animation(self, delta_time):
        self.change_time += delta_time
        
        if self.change_time > self.time:
            frames = self.get_current_frames()

            self.curr_texture_index += 1
            if self.curr_texture_index >= len(frames):
                self.curr_texture_index = 0

            if self.side == 'right':
                self.texture = frames[self.curr_texture_index]
            else:
                self.texture = frames[self.curr_texture_index].flip_horizontally()
            self.change_time = 0.0