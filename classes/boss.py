from .enemy import Enemy
from config import BOSS_DAMAG, BOSS_HEALTH, SPEED_CHASE
SCALE = 10


class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.scale = SCALE
        self.health = BOSS_HEALTH
        self.damag = BOSS_DAMAG
        self.chase_speed = SPEED_CHASE
        self.detection_range = 1000
