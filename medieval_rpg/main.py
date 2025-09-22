import pygame
import sys
from settings import *
from screens.title_screen import title_screen
from screens.spinner_screen import class_spinner

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medieval RPG")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont("Times New Roman", 80, bold=True)
subtitle_font = pygame.font.SysFont("Times New Roman", 40)

def main():
    # Show title screen
    title_screen(screen, clock, title_font, subtitle_font)
    
    # Show class spinner and get player
    player = class_spinner(screen, clock, font, small_font, title_font)

if __name__ == "__main__":
    main()
