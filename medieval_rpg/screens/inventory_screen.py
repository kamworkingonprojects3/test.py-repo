import pygame
from settings import *

def inventory_screen(player_class, skills, stats, player):
    """
    Display the inventory, skills, stats, and active quests for the player.
    
    Args:
        player_class (str): The player's class.
        skills (list): List of skill names.
        stats (dict): Player stats like HP, Attack, Defense.
        player (dict): Player dictionary containing quests.
    """
    running = True
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    small_font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont("Times New Roman", 60, bold=True)
    
    while running:
        screen.fill((80, 80, 80))
        mouse_pos = pygame.mouse.get_pos()

        # --- Draw Stats ---
        stats_x = 50
        stats_y = 50
        screen.blit(title_font.render("Stats", True, (255, 255, 255)), (stats_x, stats_y))
        offset = 80
        for stat_name, value in stats.items():
            screen.blit(small_font.render(f"{stat_name}: {value}", True, (255, 255, 255)),
                        (stats_x, stats_y + offset))
            offset += 30

        # --- Draw Skills/Hotbar ---
        hotbar_x = 300
        hotbar_y = 50
        screen.blit(title_font.render("Skills", True, (255, 255, 255)), (hotbar_x, hotbar_y))
        for i, skill in enumerate(skills):
            rect = pygame.Rect(hotbar_x, hotbar_y + 70 + i*60, 200, 50)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            text = small_font.render(skill if skill else "Empty", True, (0, 0, 0))
            screen.blit(text, (rect.x + 10, rect.y + 10))
            key_text = small_font.render(str(i+1), True, (0, 0, 0))
            screen.blit(key_text, (rect.x + 170, rect.y + 10))
            if rect.collidepoint(mouse_pos) and skill:
                desc_text = small_font.render(skill_descriptions.get(skill, "No description"), True, (255, 255, 0))
                screen.blit(desc_text, (rect.x + 220, rect.y + 10))

        # --- Draw Active Quests ---
        quest_x = 550
        quest_y = 50
        screen.blit(title_font.render("Quests", True, (255, 255, 255)), (quest_x, quest_y))
        offset = 80
        if "quests" in player and player["quests"]:
            for quest in player["quests"]:
                q_text = f"{quest['npc']}: {quest['requirement']} -> {quest['reward']}"
                screen.blit(small_font.render(q_text, True, (255, 255, 0)), (quest_x, quest_y + offset))
                offset += 30
        else:
            screen.blit(small_font.render("No active quests", True, (255, 255, 0)), (quest_x, quest_y + offset))

        # --- Close instruction ---
        screen.blit(small_font.render("Press I to close inventory", True, (255, 255, 255)), (WIDTH//2 - 100, HEIGHT - 50))

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    running = False

        pygame.display.flip()
        clock.tick(30)
