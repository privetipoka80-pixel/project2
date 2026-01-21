from enemy import Enemy
import arcade
from random import randint
from config import TILE_SCALING
from boss import Boss


class Generate_enemy(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.cell_size = 80 * 16 * TILE_SCALING // 5

    def spawn_enemy(self, x, y):
        enemy = Enemy()
        enemy.center_x = x
        enemy.center_y = y
        self.append(enemy)
        return enemy

    def spawn_in_grid(self, grid_x, grid_y):
        x = grid_x * self.cell_size + self.cell_size // 2 + randint(-80, 80)
        y = grid_y * self.cell_size + self.cell_size // 2 + randint(-80, 80)

        return self.spawn_enemy(x, y)

    def spawn_boss(self, x, y):
        enemy = Boss()
        enemy.center_x = x
        enemy.center_y = y
        self.append(enemy)
        return enemy

    def spawn_boss_in_grid(self, grid_x, grid_y):
        x = grid_x * self.cell_size + self.cell_size // 2 + randint(-80, 80)
        y = grid_y * self.cell_size + self.cell_size // 2 + randint(-80, 80)

        return self.spawn_boss(x, y)
