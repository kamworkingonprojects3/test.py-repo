import pygame, random

class NPC:
    def __init__(self, x, y, name, direction, color=(0,0,255)):
        self.x = x
        self.y = y
        self.name = name
        self.dir = direction
        self.color = color

    def update(self, tiles):
        if random.random() < 0.2:
            self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        next_pos = (self.x + self.dir[0], self.y + self.dir[1])
        if tiles.get(next_pos) == "village":
            self.x, self.y = next_pos

    def draw(self, screen, TILE_SIZE, small_font, player_tx, player_ty):
        screen_x = (self.x - player_tx + 10) * TILE_SIZE
        screen_y = (self.y - player_ty + 8) * TILE_SIZE
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        screen.blit(small_font.render(self.name, True, (0,0,0)), (screen_x, screen_y-15))
