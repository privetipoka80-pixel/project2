import arcade
from config import TILE_SCALING


class ResourceManager():
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def load_all_resources(self):

        self.TEXTURE_NORMAL = arcade.load_texture(
            "assets/sprites/normal_button.png")
        self.TEXTURE_HOVERED = arcade.load_texture(
            "assets/sprites/hover_button.png")
        self.TEXTURE_PRESSED = arcade.load_texture(
            "assets/sprites/click_button.png")

        self.maps = ["assets/map1.tmx", "assets/map2.tmx", "assets/map3.tmx"]
        self.boss_map_path = "assets/boss_map.tmx"
        self.tile_map1 = arcade.load_tilemap(
            self.maps[0], scaling=TILE_SCALING)
        self.tile_map2 = arcade.load_tilemap(
            self.maps[1], scaling=TILE_SCALING)
        self.tile_map3 = arcade.load_tilemap(
            self.maps[2], scaling=TILE_SCALING)
        self.boss_map = arcade.load_tilemap(
            self.boss_map_path, scaling=TILE_SCALING)

        self.background_music = arcade.load_sound('assets/sounds/MUSIC.mp3')

        self.torch_frames = []
        for i in range(1, 9):
            texture = arcade.load_texture(f"assets/sprites/f{i}.png")
            self.torch_frames.append(texture)

        self.sound1 = arcade.load_sound('assets/sounds/ATTACK1.mp3')
        self.sound2 = arcade.load_sound('assets/sounds/ATTACK2.mp3')

        self.boss_idle_path = 'assets/enemy/enemy4.png'
        self.boss_walk_path = 'assets/enemy/enemy3.png'
        self.boss_attack1_path = 'assets/enemy/enemy1.png'
        self.boss_dead_path = 'assets/enemy/enemy2.png'
        self.boss_attack3_path = 'assets/enemy/enemy5.png'

        self.boss_frame_w = 64
        self.boss_frame_h = 64

        idle_texture = arcade.load_texture(self.boss_idle_path)
        self.boss_idle_frames = []
        for i in range(4):
            frame = idle_texture.crop(
                i * self.boss_frame_w, 0, self.boss_frame_w, self.boss_frame_h)
            self.boss_idle_frames.append(frame)

        walk_texture = arcade.load_texture(self.boss_walk_path)
        self.boss_walk_frames = []
        for i in range(6):
            frame = walk_texture.crop(
                i * self.boss_frame_w, 0, self.boss_frame_w, self.boss_frame_h)
            self.boss_walk_frames.append(frame)

        attack1_texture = arcade.load_texture(self.boss_attack1_path)
        self.boss_attack_frames = []
        for i in range(6):
            frame = attack1_texture.crop(
                i * self.boss_frame_w, 0, self.boss_frame_w, self.boss_frame_h)
            self.boss_attack_frames.append(frame)

        dead_texture = arcade.load_texture(self.boss_dead_path)
        self.boss_dead_frames = []
        for i in range(6):
            frame = dead_texture.crop(
                i * self.boss_frame_w, 0, self.boss_frame_w, self.boss_frame_h)
            self.boss_dead_frames.append(frame)

        self.player_idle_path = 'assets/player/IDLE.png'
        self.player_walk_path = 'assets/player/WALK.png'
        self.player_attack1_path = 'assets/player/ATTACK1.png'
        self.player_attack2_path = 'assets/player/ATTACK2.png'
        self.player_attack3_path = 'assets/player/ATTACK3.png'

        self.player_frame_w = 96
        self.player_frame_h = 84

        idle_texture = arcade.load_texture(self.player_idle_path)
        self.player_idle_frames = []
        for i in range(7):
            frame = idle_texture.crop(
                i * self.player_frame_w, 0, self.player_frame_w, self.player_frame_h)
            self.player_idle_frames.append(frame)

        walk_texture = arcade.load_texture(self.player_walk_path)
        self.player_walk_frames = []
        for i in range(6):
            frame = walk_texture.crop(
                i * self.player_frame_w, 0, self.player_frame_w, self.player_frame_h)
            self.player_walk_frames.append(frame)

        attack1_texture = arcade.load_texture(self.player_attack1_path)
        self.player_attack1_frames = []
        for i in range(6):
            frame = attack1_texture.crop(
                i * self.player_frame_w, 0, self.player_frame_w, self.player_frame_h)
            self.player_attack1_frames.append(frame)

        attack2_texture = arcade.load_texture(self.player_attack2_path)
        self.player_attack2_frames = []
        for i in range(5):
            frame = attack2_texture.crop(
                i * self.player_frame_w, 0, self.player_frame_w, self.player_frame_h)
            self.player_attack2_frames.append(frame)

        attack3_texture = arcade.load_texture(self.player_attack3_path)
        self.player_attack3_frames = []
        for i in range(6):
            frame = attack3_texture.crop(
                i * self.player_frame_w, 0, self.player_frame_w, self.player_frame_h)
            self.player_attack3_frames.append(frame)

        self.walk1 = arcade.load_sound('assets/sounds/WALK4.mp3')
        self.walk2 = arcade.load_sound('assets/sounds/WALK5.mp3')
        self.coin_sound = arcade.load_sound('assets/sounds/coin.mp3')
        self.background_texture = arcade.load_texture("assets/sprites/background.png")