import pygame
from settings import class_colors, class_starting_skills, class_starting_stats

class Player:
    def __init__(self, class_name):
        self.class_name = class_name
        self.color = class_colors.get(class_name, (255,0,0))
        self.skills = [class_starting_skills[class_name], "", "", "", ""]
        self.stats = class_starting_stats[class_name]
        self.tx, self.ty = 0, 0  # tile coordinates
        self.last_move = (0, -1)
        self.selected_skill = 0

    def move(self, dx, dy, tiles):
        target_tile = (self.tx + dx, self.ty + dy)
        if tiles.get(target_tile, "grass") not in ["tree", "boulder", "village"]:
            self.tx += dx
            self.ty += dy
            self.last_move = (dx, dy)

    def draw(self, screen, TILE_SIZE):
        pygame.draw.rect(screen, self.color, (10*TILE_SIZE, 8*TILE_SIZE, TILE_SIZE, TILE_SIZE))
