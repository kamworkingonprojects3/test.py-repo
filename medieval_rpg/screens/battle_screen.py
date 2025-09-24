import pygame
import random
from settings import *

def battle_screen(screen, clock, player):
    font = pygame.font.SysFont(None, 40)
    enemy = {
        "name": random.choice(["Slime", "Goblin", "Bat"]),
        "hp": random.randint(20, 40),
        "max_hp": 40,
        "color": (200, 0, 0)
    }

    # Use lowercase keys to match settings.py
    player_hp = class_starting_stats[player["class"]]["hp"]
    skills = [class_starting_skills[player["class"]], "", "", "", ""]
    selected_skill = 0

    running = True
    while running:
        screen.fill((50, 50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Player attacks with skill 1
                if event.key == pygame.K_1 and skills[0]:
                    damage = class_starting_stats[player["class"]]["attack"]
                    enemy["hp"] -= damage
                    print(f"{skills[0]} dealt {damage} damage!")

                    # Enemy counterattack
                    if enemy["hp"] > 0:
                        player_hp -= random.randint(5, 12)

        # Draw battle UI
        pygame.draw.rect(screen, (0, 200, 0), (50, HEIGHT-150, max(player_hp, 0) * 2, 30))
        pygame.draw.rect(screen, enemy["color"], (WIDTH-250, 50, max(enemy["hp"], 0) * 2, 30))
        screen.blit(font.render(f"Enemy: {enemy['name']}", True, (255, 255, 255)), (WIDTH-250, 20))
        screen.blit(font.render(f"Player HP: {player_hp}", True, (255, 255, 255)), (50, HEIGHT-180))
        screen.blit(font.render("Press 1 to attack!", True, (255, 255, 0)), (50, HEIGHT-100))

        pygame.display.flip()
        clock.tick(30)

        # End battle if someone dies
        if enemy["hp"] <= 0 or player_hp <= 0:
            running = False
