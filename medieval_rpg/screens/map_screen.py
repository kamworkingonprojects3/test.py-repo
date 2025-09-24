import pygame
import random
import sys
from settings import *
from entities.tiles import TileMap
from screens.inventory_screen import inventory_screen
from screens.battle_screen import battle_screen
from zones import get_zone_at

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW= (255, 255, 0)
GRAY  = (180, 180, 180)
DARK_GREEN = (0, 155, 0)

# --- Example Skill Tree ---
class_skills_tree = {
    "Warrior": {
        "tier1": ["Slash", "Shield Bash"],
        "tier2": ["Power Strike", "Armor Up"],
        "tier3": ["Berserk", "Earthquake"]
    },
    "Rogue": {
        "tier1": ["Backstab", "Cloak"],
        "tier2": ["Hemorrhage Strike", "Smoke Bomb"],
        "tier3": ["Assasination", "Execution"]
    },
     "Archer": {
        "tier1": ["Arrow Shot", "Triple Shot"],
        "tier2": ["Poison Arrows", "Fire Arrows"],
        "tier3": ["Arrow Rain", "Holy Shot"]
    },
    "Mage": {
        "tier1": ["Fireball", "Ice Bolt"],
        "tier2": ["Lightning", "Mana Shield"],
        "tier3": ["Meteor", "Time Warp"]
    },
    "Skeleton": {
        "tier1": ["Bone Throw", "Rattle"],
        "tier2": ["Bone Shield", "Necrotic Touch"],
        "tier3": ["Death Grasp", "Bone Storm"]
    }
}

# --- Player Initialization ---
def initialize_player(player_class):
    stats = class_starting_stats[player_class].copy()
    if "speed" not in stats:
        stats["speed"] = 5
    player = {
        "class": player_class,
        "skills": [class_starting_skills[player_class], "", "", "", ""],
        "stats": stats,
        "quests": [],
        "xp": 0,
        "level": 5,
        "gold": 0,
        "items": []
    }
    # Simulate level-ups from 1 → 5
    for _ in range(4):
        player["stats"]["hp"] += 10
        player["stats"]["attack"] += 2
        player["stats"]["defense"] += 2
        player["stats"]["speed"] += 1
    return player

# --- Skill Tree Screen ---
def skill_tree_screen(player_class, player, screen, font, clock):
    tree = class_skills_tree[player_class]
    running = True
    positions = {
        "tier1": [(200, 150), (400, 150)],
        "tier2": [(200, 300), (400, 300)],
        "tier3": [(300, 450), (500, 450)]
    }

    while running:
        screen.fill((50, 50, 50))
        # Draw skill nodes
        for tier, skills in tree.items():
            for i, skill in enumerate(skills):
                x, y = positions[tier][i] if i < len(positions[tier]) else (100+i*100, 100)
                color = (100, 100, 100)  # locked
                if skill in player["skills"]:
                    color = (0, 255, 0)
                elif (tier=="tier1" or 
                      (tier=="tier2" and player["level"]>=5) or 
                      (tier=="tier3" and player["level"]>=10)):
                    color = (255, 255, 0)  # unlockable
                pygame.draw.rect(screen, color, (x, y, 120, 40))
                text = font.render(skill, True, BLACK)
                screen.blit(text, (x + 60 - text.get_width()//2, y + 20 - text.get_height()//2))
        # Draw lines between tiers
        for i, skill1 in enumerate(tree.get("tier1", [])):
            for j, skill2 in enumerate(tree.get("tier2", [])):
                pygame.draw.line(screen, WHITE, 
                                 (positions["tier1"][i][0]+60, positions["tier1"][i][1]+40),
                                 (positions["tier2"][j][0]+60, positions["tier2"][j][1]), 3)
        for i, skill1 in enumerate(tree.get("tier2", [])):
            for j, skill2 in enumerate(tree.get("tier3", [])):
                pygame.draw.line(screen, WHITE, 
                                 (positions["tier2"][i][0]+60, positions["tier2"][i][1]+40),
                                 (positions["tier3"][j][0]+60, positions["tier3"][j][1]), 3)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for tier, skills in tree.items():
                    for i, skill in enumerate(skills):
                        x, y = positions[tier][i] if i < len(positions[tier]) else (100+i*100, 100)
                        rect = pygame.Rect(x, y, 120, 40)
                        if rect.collidepoint(mx, my):
                            if (tier=="tier1" or 
                               (tier=="tier2" and player["level"]>=5) or 
                               (tier=="tier3" and player["level"]>=10)):
                                if skill not in player["skills"]:
                                    for idx in range(len(player["skills"])):
                                        if player["skills"][idx]=="":
                                            player["skills"][idx] = skill
                                            break
        pygame.display.flip()
        clock.tick(30)

# --- Map Screen ---
def map_screen(screen, clock, player_class, tilemap, font):
    player_tx, player_ty = 0, 0
    player = initialize_player(player_class)
    skills = player["skills"]
    stats = player["stats"]
    player_color = class_colors.get(player_class, RED)
    last_move = (0, -1)

    # Clearing spawn
    clearing_radius = 3
    for dx in range(-clearing_radius, clearing_radius+1):
        for dy in range(-clearing_radius, clearing_radius+1):
            tilemap.set_tile(player_tx+dx, player_ty+dy, 'grass')

    # Villages anywhere
    village_coords = []
    for _ in range(2):
        while True:
            vx = random.randint(-50, 50)
            vy = random.randint(-40, 40)
            w, h = 12, 12
            if tilemap.is_area_clear(vx, vy, w, h):
                tilemap.generate_village(vx, vy, w, h)
                village_coords.append((vx, vy, w, h))
                break

    # NPCs
    npc_names = ["Eldon","Marla","Finn","Rina","Garrick","Lina","Doran"]
    quest_templates = [
        {"name":"Defeat Goblins","requirement":"10 Goblins","reward":"XP +500"},
        {"name":"Defeat Bats","requirement":"3 Bats","reward":"XP +50"},
        {"name":"Defeat Slimes","requirement":"5 Slimes","reward":"XP +100"}
    ]
    npcs = []
    for vx, vy, w, h in village_coords:
        occupied_tiles = []
        for _ in range(random.randint(3,5)):
            while True:
                npc_x = vx + random.randint(0,w-1)
                npc_y = vy + random.randint(0,h-1)
                if tilemap.get_tile(npc_x, npc_y) == 'village' and (npc_x,npc_y) not in occupied_tiles:
                    occupied_tiles.append((npc_x,npc_y))
                    npc_color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
                    quest = random.choice(quest_templates).copy()
                    npcs.append({
                        "x":npc_x,"y":npc_y,
                        "dir":random.choice([(1,0),(-1,0),(0,1),(0,-1)]),
                        "name": random.choice(npc_names),
                        "color": npc_color,
                        "quest": quest
                    })
                    break

    running = True
    quest_ui = None
    last_player_tx, last_player_ty = player_tx, player_ty

    while running:
        screen.fill(GRAY)
        zone = get_zone_at(player_tx, player_ty)

        # --- Input ---
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: move_y=-1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: move_y=1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move_x=-1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: move_x=1
        if move_x!=0 or move_y!=0: last_move=(move_x,move_y)
        target_tile = (player_tx + move_x, player_ty + move_y)

        # --- Movement ---
        if tilemap.get_tile(*target_tile) not in ['tree','boulder']:
            player_tx += move_x
            player_ty += move_y
            if player_tx != last_player_tx or player_ty != last_player_ty:
                for _ in range(10):
                    x = random.randint(-10, 10)
                    y = random.randint(-8, 8)
                    tile_x = player_tx + x
                    tile_y = player_ty + y
                    if -3 <= x <= 3 and -3 <= y <= 3: continue
                    current_tile = tilemap.get_tile(tile_x, tile_y)
                    current_zone = get_zone_at(tile_x, tile_y)
                    if current_tile == 'grass':
                        if current_zone.name=="Forest" and random.random()<0.3:
                            tilemap.set_tile(tile_x, tile_y, 'tree')
                        elif current_zone.name=="Plains" and random.random()<0.2:
                            tilemap.set_tile(tile_x, tile_y, 'boulder')
                last_player_tx, last_player_ty = player_tx, player_ty

            # Random encounters
            current_tile = tilemap.get_tile(player_tx, player_ty)
            if current_tile != 'village' and random.random() < zone.encounter_rate:
                battle_screen(screen, clock, player)
                xp_gain = random.randint(5, 10) + player["level"]
                player["xp"] += xp_gain
                xp_needed = 50 + player["level"] * 50
                while player["xp"] >= xp_needed:
                    player["xp"] -= xp_needed
                    player["level"] += 1
                    player["stats"]["hp"] += 10
                    player["stats"]["attack"] += 2
                    player["stats"]["defense"] += 2
                    player["stats"]["speed"] += 1
                    xp_needed = 50 + player["level"] * 50
                    print(f"Level up! You are now level {player['level']}.")

        # --- NPC Movement ---
        for npc in npcs:
            if random.random()<0.1: npc["dir"]=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            next_pos = (npc["x"]+npc["dir"][0], npc["y"]+npc["dir"][1])
            if tilemap.get_tile(*next_pos)=='village': npc["x"], npc["y"] = next_pos

        # --- Draw Tiles ---
        for y in range(-8, 9):
            for x in range(-10, 11):
                tile_x = player_tx + x
                tile_y = player_ty + y
                tile = tilemap.get_tile(tile_x, tile_y)
                color = zone.tileset.get(tile, (180,180,180))
                screen_x = (x+10)*TILE_SIZE
                screen_y = (y+8)*TILE_SIZE
                pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

        # --- Zone Text ---
        zone_text = font.render(f"Zone: {zone.name}", True, BLACK)
        screen.blit(zone_text, (WIDTH - zone_text.get_width() - 10, 10))

        # --- NPCs ---
        for npc in npcs:
            screen_x = (npc["x"]-player_tx+10)*TILE_SIZE
            screen_y = (npc["y"]-player_ty+8)*TILE_SIZE
            pygame.draw.rect(screen, npc["color"], (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            screen.blit(font.render(npc["name"], True, BLACK), (screen_x, screen_y-15))

        # --- Quest UI ---
        quest_ui = None
        for npc in npcs:
            if abs(player_tx-npc["x"])<=1 and abs(player_ty-npc["y"])<=1 and npc["quest"]:
                quest_ui = npc
                break
        if quest_ui:
            rect = pygame.Rect(WIDTH//2-150, HEIGHT//2-100, 300, 150)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            screen.blit(font.render(f"Quest: {quest_ui['quest']['name']}", True, BLACK), (rect.x+10, rect.y+10))
            screen.blit(font.render(f"Req: {quest_ui['quest']['requirement']}", True, BLACK), (rect.x+10, rect.y+50))
            screen.blit(font.render(f"Reward: {quest_ui['quest']['reward']}", True, BLACK), (rect.x+10, rect.y+90))
            accept_rect = pygame.Rect(rect.x+20, rect.y+120, 100, 25)
            decline_rect = pygame.Rect(rect.x+180, rect.y+120, 100, 25)
            pygame.draw.rect(screen, GREEN, accept_rect)
            pygame.draw.rect(screen, RED, decline_rect)
            screen.blit(font.render("ACCEPT", True, BLACK), (accept_rect.x+5, accept_rect.y))
            screen.blit(font.render("DECLINE", True, BLACK), (decline_rect.x+5, decline_rect.y))

        # --- Player ---
        pygame.draw.rect(screen, player_color, (10*TILE_SIZE,8*TILE_SIZE,TILE_SIZE,TILE_SIZE))

        # --- EXP BAR ---
        bar_x = WIDTH//2 - 100
        bar_y = HEIGHT - 110
        bar_width = 200
        bar_height = 15
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        xp_needed = 50 + player["level"] * 50
        fill_width = int((player["xp"] / xp_needed) * bar_width)
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, fill_width, bar_height))
        xp_text = font.render(f"XP: {player['xp']} / {xp_needed}", True, BLACK)
        screen.blit(xp_text, (bar_x + bar_width//2 - xp_text.get_width()//2, bar_y-20))

        # --- Hotbar ---
        hotbar_width = TILE_SIZE*5 + 20
        hotbar_x = WIDTH//2 - hotbar_width//2
        hotbar_y = HEIGHT-70
        for i, skill in enumerate(skills):
            rect = pygame.Rect(hotbar_x+i*(TILE_SIZE+5), hotbar_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            if i==0: pygame.draw.rect(screen, YELLOW, rect, 3)
            if skill:
                text = font.render(skill[0], True, BLACK)
                screen.blit(text, (rect.x + TILE_SIZE//2 - text.get_width()//2,
                                   rect.y + TILE_SIZE//2 - text.get_height()//2))

        # --- HUD ---
        screen.blit(font.render(f"Class: {player_class}", True, BLACK), (10,10))
        screen.blit(font.render(f"Level: {player['level']}", True, BLACK), (10, 40))
        screen.blit(font.render(f"Skill: {skills[0]}", True, BLACK), (WIDTH//2-50, HEIGHT-100))

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: inventory_screen(player_class, skills, stats, player)
                if event.key == pygame.K_k: skill_tree_screen(player_class, player, screen, font, clock)
            if event.type == pygame.MOUSEBUTTONDOWN and quest_ui:
                mx,my = event.pos
                if accept_rect.collidepoint(mx,my):
                    reward = quest_ui["quest"]["reward"]
                    if reward.startswith("XP +"):
                        xp_amount = int(reward.split("+")[1])
                        player["xp"] += xp_amount
                        while player["xp"] >= 50 + player["level"]*50:
                            player["xp"] -= 50 + player["level"]*50
                            player["level"] += 1
                            player["stats"]["hp"] += 10
                            player["stats"]["attack"] += 2
                            player["stats"]["defense"] += 2
                            player["stats"]["speed"] += 1
                    elif reward.lower()=="potion": player["items"].append("Potion")
                    elif reward.lower().endswith("gold"): player["gold"] += int(reward.split()[0])
                    quest_copy = quest_ui["quest"].copy()
                    quest_copy["npc"] = quest_ui["name"]
                    player["quests"].append(quest_copy)
                    quest_ui["quest"] = None
                if decline_rect.collidepoint(mx,my):
                    quest_ui["quest"] = None

        pygame.display.flip()
        clock.tick(10)
