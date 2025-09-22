import pygame
import random
import sys
from settings import *
from screens.map_screen import map_screen
from entities.tiles import TileMap

def class_spinner(screen, clock, font, small_font, title_font):
    selected_class = ""
    no_spin_message_timer = 0
    remaining_spins_local = total_spins
    tilemap = TileMap()  # Initialize tilemap

    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
    finish_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 60)

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, button_rect)
        screen.blit(font.render("SPIN!", True, WHITE), (button_rect.x + 40, button_rect.y + 10))
        pygame.draw.rect(screen, DARK_GREEN, finish_rect)
        screen.blit(font.render("FINISH", True, WHITE), (finish_rect.x + 20, finish_rect.y + 10))

        if selected_class:
            screen.blit(font.render(f"Class: {selected_class}", True, class_colors[selected_class]),
                        (WIDTH//2 - 150, HEIGHT//2 - 150))
        screen.blit(small_font.render(f"Remaining Spins: {remaining_spins_local}", True, BLACK),
                    (WIDTH//2 - 90, HEIGHT - 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    if remaining_spins_local > 0:
                        selected_class = random.choices(classes, weights=chances, k=1)[0]
                        remaining_spins_local -= 1
                    else:
                        no_spin_message_timer = 60
                if finish_rect.collidepoint(event.pos) and selected_class:
                    # Pass only the class string, not the player dict
                    map_screen(screen, clock, selected_class, tilemap, small_font)
                    return

        if no_spin_message_timer > 0:
            screen.blit(small_font.render("No Spins Left!", True, RED), (WIDTH//2 - 80, HEIGHT//2 + 50))
            no_spin_message_timer -= 1

        pygame.display.flip()
        clock.tick(60)
