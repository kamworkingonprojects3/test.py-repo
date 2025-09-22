import pygame
import random
from settings import *

class TileMap:
    def __init__(self):
        self.tiles = {}  # dictionary of (x,y) -> tile_type

    def set_tile(self, x, y, tile_type):
        self.tiles[(x,y)] = tile_type

    def get_tile(self, x, y):
        return self.tiles.get((x,y), 'grass')

    def is_area_clear(self, x, y, w, h):
        for dx in range(w):
            for dy in range(h):
                if self.get_tile(x+dx, y+dy) != 'grass':
                    return False
        return True

    def generate_village(self, x, y, w, h):
        # houses 3x3 in columns with 1-tile grass roads
        for i in range(0, w, 4):
            for j in range(0, h, 4):
                for dx in range(3):
                    for dy in range(3):
                        self.set_tile(x+i+dx, y+j+dy, 'village')
                # leave column of grass between house blocks
                for r in range(3):
                    self.set_tile(x+i+3, y+j+r, 'grass')

    def draw(self, screen, player_tx, player_ty, TILE_SIZE):
        for i in range(-10,11):
            for j in range(-8,9):
                tx = player_tx + i
                ty = player_ty + j
                t_type = self.get_tile(tx, ty)
                if t_type == 'grass':
                    color = LIGHT_GREEN
                elif t_type == 'tree':
                    color = BROWN
                elif t_type == 'boulder':
                    color = DARK_GRAY
                elif t_type == 'village':
                    color = GOLD
                else:
                    color = GRAY
                screen_x = (i+10) * TILE_SIZE
                screen_y = (j+8) * TILE_SIZE
                pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

    def generate_tile(self, x, y):
        # Only generate if tile doesn't exist
        if (x, y) in self.tiles:
            return
        rand = random.randint(1,10)
        if rand == 1: self.set_tile(x,y,'tree')
        elif rand == 2: self.set_tile(x,y,'boulder')
        else: self.set_tile(x,y,'grass')
