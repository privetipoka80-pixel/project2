from enemy import Enemy
import arcade


class Generate_enemy(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.spawn_points = []
    
    def spawn_enemy(self, x, y):
        enemy = Enemy()
        enemy.center_x = x
        enemy.center_y = y
        self.append(enemy)
        return enemy
    
    def spawn_in_grid(self, grid_x, grid_y, cell_size=512):
        x = grid_x * cell_size + cell_size // 2 + 80
        y = grid_y * cell_size + cell_size // 2

        return self.spawn_enemy(x, y)
    
    def update_all_animations(self, delta_time):
        for enemy in self:
            enemy.update_animation(delta_time)