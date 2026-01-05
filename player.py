import arcade

SCALE = 2

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=SCALE)
        texture = arcade.load_texture('assets/player/IDLE.png')
        self.side = 'right'
        frame_w = 96
        frame_h = 84
        
        self.idle_frames = []
        for i in range(7):
            frame = texture.crop(i * frame_w, 0, frame_w, frame_h)
            self.idle_frames.append(frame)
        
        self.texture = self.idle_frames[0]

        self.curr_texture_index = 0
        self.change_time = 0.0
        self.time = 0.1
    
    """Обновление анимации игрока"""
    def update_animation(self, delta_time):
        self.change_time += delta_time
        
        if self.change_time > self.time:
            self.curr_texture_index += 1
            if self.curr_texture_index >= len(self.idle_frames):
                self.curr_texture_index = 0

            if self.side == 'right':
                self.texture = self.idle_frames[self.curr_texture_index]
            else:
                self.texture = self.idle_frames[self.curr_texture_index].flip_horizontally()
            self.change_time = 0.0