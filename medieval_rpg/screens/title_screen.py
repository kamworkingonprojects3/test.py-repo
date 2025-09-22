import pygame, sys
from settings import *

def title_screen(screen, clock, title_font, subtitle_font):
    running = True
    fade_out = False
    alpha = 255
    title_surface = pygame.Surface((WIDTH, HEIGHT))
    title_surface.fill(BLACK)

    while running:
        screen.fill(BLACK)
        screen.blit(title_font.render("Medieval RPG", True, GOLD), (WIDTH//2 - 200, HEIGHT//3))
        screen.blit(subtitle_font.render("Press Enter to Start", True, WHITE), (WIDTH//2 - 150, HEIGHT//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: fade_out = True

        if fade_out:
            alpha -= 10
            if alpha <= 0:
                return
            title_surface.set_alpha(alpha)
            screen.blit(title_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)
