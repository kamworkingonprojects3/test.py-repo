import pygame
import sys
import random

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW= (255, 255, 0)

def battle_screen(screen, clock, player):
    font = pygame.font.SysFont(None, 28)

    # Create enemy
    enemy = {
        "name": random.choice(["Goblin", "Bat", "Slime"]),
        "hp": 50,
        "attack": 5,
        "effects": {}  # status effects like poison, stun, etc.
    }

    # --- Skills and hotbar ---
    active_slot = 0
    skills = player["skills"]
    cooldowns = [0] * 5
    turn = "player"

    running = True
    while running:
        screen.fill((200, 200, 200))

        # --- Enemy UI ---
        screen.blit(font.render(f"{enemy['name']} HP: {enemy['hp']}", True, BLACK), (20, 20))
        pygame.draw.rect(screen, RED, (20, 50, enemy["hp"]*2, 20))

        # --- Player UI ---
        screen.blit(font.render(f"Player HP: {player['stats']['hp']}", True, BLACK), (20, 100))

        # --- Hotbar UI ---
        hotbar_x = 50
        hotbar_y = 400
        for i, skill in enumerate(skills):
            rect = pygame.Rect(hotbar_x + i*90, hotbar_y, 80, 40)
            pygame.draw.rect(screen, WHITE, rect)
            if i == active_slot: pygame.draw.rect(screen, YELLOW, rect, 3)
            if skill:
                cd_text = f" ({cooldowns[i]})" if cooldowns[i] > 0 else ""
                text = font.render(skill + cd_text, True, BLACK)
                screen.blit(text, (rect.x + 5, rect.y + 10))

        # --- Turn Info ---
        if turn == "player":
            screen.blit(font.render("Your Turn: SPACE to use skill", True, BLACK), (20, 200))
        else:
            screen.blit(font.render("Enemy Turn...", True, BLACK), (20, 200))

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Swap skill
                if pygame.K_1 <= event.key <= pygame.K_5:
                    idx = event.key - pygame.K_1
                    if skills[idx]: active_slot = idx

                # Use skill
                if event.key == pygame.K_SPACE and turn == "player":
                    skill_name = skills[active_slot]
                    if not skill_name or cooldowns[active_slot] > 0:
                        continue
                    dmg, cd, effect = use_skill(skill_name, player, enemy)
                    enemy["hp"] -= dmg
                    if effect:
                        enemy["effects"].update(effect)
                    cooldowns[active_slot] = cd
                    turn = "enemy"

        # --- Enemy Turn ---
        if turn == "enemy":
            pygame.time.delay(500)
            dmg = enemy["attack"]
            if "stun" in enemy["effects"]:
                dmg = 0  # skip turn
                del enemy["effects"]["stun"]
            player["stats"]["hp"] -= dmg
            turn = "player"

            # Apply ongoing effects on enemy
            if "poison" in enemy["effects"]:
                poison_dmg, turns_left = enemy["effects"]["poison"]
                enemy["hp"] -= poison_dmg
                turns_left -= 1
                if turns_left <= 0:
                    del enemy["effects"]["poison"]
                else:
                    enemy["effects"]["poison"] = (poison_dmg, turns_left)

            # Reduce cooldowns
            for i in range(len(cooldowns)):
                if cooldowns[i] > 0: cooldowns[i] -= 1

              # --- Win/Loss Check ---
            if enemy["hp"] <= 0:
                #heal player after battle
                player["stats"]["hp"] = player["stats"]["max_hp"]
                return
        if player["stats"]["hp"] <= 0:
            print("You died!")
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(30)


def use_skill(skill_name, player, enemy):
    """
    Returns: (damagprint(f"{enemy['name']} defeated!")
    # Heale, cooldown, effect_dict)
    effect_dict = {"poison": (dmg_per_turn, turns), "stun": 1, etc.}
    """
    dmg = player["stats"]["attack"]
    cd = 0
    effect = {}

    # --- Tier 1: low damage ---
    if skill_name in ["Slash", "Backstab", "Arrow Shot", "Fireball", "Bone Throw"]:
        dmg += 5
        cd = 0
    elif skill_name in ["Shield Bash", "Rattle", "Ice Bolt"]:
        dmg += 3
        effect = {"stun": 1}  # stuns 1 turn
        cd = 1

    # --- Tier 2: moderate damage / effect ---
    elif skill_name in ["Power Strike", "Lightning", "Necrotic Touch", "Hemorrhage Strike", "Fire Arrows", "Poison Arrows"]:
        dmg += 12
        cd = 2
        if skill_name in ["Poison Arrows", "Necrotic Touch"]:
            effect = {"poison": (3, 3)}  # 3 dmg per turn for 3 turns

    elif skill_name in ["Armor Up", "Smoke Bomb", "Bone Shield", "Mana Shield", "Cloak"]:
        dmg = 0
        cd = 3
        if skill_name == "Armor Up":
            player["stats"]["defense"] += 5
        elif skill_name == "Mana Shield":
            player["stats"]["hp"] += 10  # absorbs damage
        elif skill_name == "Cloak":
            player["stats"]["speed"] += 2

    # --- Tier 3: insane damage, long cooldown ---
    elif skill_name in ["Berserk", "Assassination", "Holy Shot", "Death Grasp"]:
        dmg += 25
        cd = 5
    elif skill_name in ["Earthquake", "Arrow Rain", "Meteor", "Bone Storm", "Execution"]:
        dmg += 20
        cd = 6

    return dmg, cd, effect
