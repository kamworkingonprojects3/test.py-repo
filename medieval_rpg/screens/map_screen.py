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

def map_screen(screen, clock, player_class, tilemap, font):
    # --- Player Setup ---
    player_tx, player_ty = 0, 0
    skills = [class_starting_skills[player_class], "", "", "", ""]
    stats = class_starting_stats[player_class]
    player = {
        "class": player_class,
        "skills": skills,
        "stats": stats,
        "quests": []
    }
    player_color = class_colors.get(player_class, RED)
    last_move = (0, -1)

    # --- Generate Clearing for Spawn ---
    clearing_radius = 3
    for dx in range(-clearing_radius, clearing_radius+1):
        for dy in range(-clearing_radius, clearing_radius+1):
            tilemap.set_tile(player_tx+dx, player_ty+dy, 'grass')

    # --- Generate Villages ---
    village_coords = []
    for _ in range(2):
        while True:
            vx = random.randint(-20, 20)
            vy = random.randint(-15, 15)
            w, h = 12, 12
            if tilemap.is_area_clear(vx, vy, w, h):
                tilemap.generate_village(vx, vy, w, h)
                village_coords.append((vx, vy, w, h))
                break

    # --- Spawn NPCs and Assign Quests ---
    npc_names = ["Eldon","Marla","Finn","Rina","Garrick","Lina","Doran"]
    quest_templates = [
        {"name":"Collect Herbs","requirement":"5 Herbs","reward":"50 Gold"},
        {"name":"Defeat Wolves","requirement":"3 Wolves","reward":"XP +10"},
        {"name":"Find Lost Item","requirement":"1 Lost Item","reward":"Potion"}
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
                        "x":npc_x,
                        "y":npc_y,
                        "dir":random.choice([(1,0),(-1,0),(0,1),(0,-1)]),
                        "name": random.choice(npc_names),
                        "color": npc_color,
                        "quest": quest
                    })
                    break

    running = True
    quest_ui = None  # To store quest accept/decline display
    last_player_tx, last_player_ty = player_tx, player_ty

    while running:
        screen.fill(GRAY)
        
        # --- Get current zone based on player position ---
        zone = get_zone_at(player_tx, player_ty)

        # --- Player Input ---
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: move_y=-1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: move_y=1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move_x=-1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: move_x=1
        if move_x!=0 or move_y!=0: last_move=(move_x,move_y)
        target_tile = (player_tx + move_x, player_ty + move_y)

        # --- Player Movement ---
        if tilemap.get_tile(*target_tile) not in ['tree','boulder']:
            player_tx += move_x
            player_ty += move_y

            # --- Procedural tree/boulder generation on move ---
            if player_tx != last_player_tx or player_ty != last_player_ty:
                for _ in range(10):
                    x = random.randint(-10, 10)
                    y = random.randint(-8, 8)
                    tile_x = player_tx + x
                    tile_y = player_ty + y
                    if -3 <= x <= 3 and -3 <= y <= 3:
                        continue
                    current_tile = tilemap.get_tile(tile_x, tile_y)
                    current_zone = get_zone_at(tile_x, tile_y)
                    if current_tile == 'grass':
                        if current_zone.name == "Forest" and random.random() < 0.3:
                            tilemap.set_tile(tile_x, tile_y, 'tree')
                        elif current_zone.name == "Plains" and random.random() < 0.2:
                            tilemap.set_tile(tile_x, tile_y, 'boulder')
                last_player_tx, last_player_ty = player_tx, player_ty

            # --- Random encounter ---
            current_tile = tilemap.get_tile(player_tx, player_ty)
            if current_tile != 'village':
                if random.random() < zone.encounter_rate:
                    battle_screen(screen, clock, player)

        # --- NPC Movement ---
        for npc in npcs:
            if random.random() < 0.1:
                npc["dir"] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            next_pos = (npc["x"]+npc["dir"][0], npc["y"]+npc["dir"][1])
            if tilemap.get_tile(*next_pos) == 'village':
                npc["x"], npc["y"] = next_pos

        # --- Draw Tiles ---
        for y in range(-8, 9):
            for x in range(-10, 11):
                tile_x = player_tx + x
                tile_y = player_ty + y
                tile = tilemap.get_tile(tile_x, tile_y)
                color = zone.tileset.get(tile, (180, 180, 180))
                screen_x = (x + 10) * TILE_SIZE
                screen_y = (y + 8) * TILE_SIZE
                pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

        # --- Zone Display ---
        zone_text = font.render(f"Zone: {zone.name}", True, BLACK)
        screen.blit(zone_text, (WIDTH - zone_text.get_width() - 10, 10))

        # --- Draw NPCs ---
        for npc in npcs:
            screen_x = (npc["x"]-player_tx+10)*TILE_SIZE
            screen_y = (npc["y"]-player_ty+8)*TILE_SIZE
            pygame.draw.rect(screen, npc["color"], (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            screen.blit(font.render(npc["name"], True, BLACK), (screen_x, screen_y-15))

        # --- Check for Quest Interaction ---
        quest_ui = None
        for npc in npcs:
            if abs(player_tx - npc["x"])<=1 and abs(player_ty - npc["y"])<=1 and npc["quest"]:
                quest_ui = npc
                break

        # --- Draw Quest UI ---
        if quest_ui:
            rect = pygame.Rect(WIDTH//2-150, HEIGHT//2-100, 300, 150)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            quest_text = font.render(f"Quest: {quest_ui['quest']['name']}", True, BLACK)
            req_text = font.render(f"Req: {quest_ui['quest']['requirement']}", True, BLACK)
            reward_text = font.render(f"Reward: {quest_ui['quest']['reward']}", True, BLACK)
            screen.blit(quest_text, (rect.x+10, rect.y+10))
            screen.blit(req_text, (rect.x+10, rect.y+50))
            screen.blit(reward_text, (rect.x+10, rect.y+90))
            accept_rect = pygame.Rect(rect.x+20, rect.y+120, 100, 25)
            decline_rect = pygame.Rect(rect.x+180, rect.y+120, 100, 25)
            pygame.draw.rect(screen, GREEN, accept_rect)
            pygame.draw.rect(screen, RED, decline_rect)
            screen.blit(font.render("ACCEPT", True, BLACK), (accept_rect.x+5, accept_rect.y))
            screen.blit(font.render("DECLINE", True, BLACK), (decline_rect.x+5, decline_rect.y))

        # --- Draw Player ---
        pygame.draw.rect(screen, player_color, (10*TILE_SIZE,8*TILE_SIZE,TILE_SIZE,TILE_SIZE))

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

        # --- Display Stats/Skills ---
        screen.blit(font.render(f"Class: {player_class}", True, BLACK), (10,10))
        screen.blit(font.render(f"Skill: {skills[0]}", True, BLACK), (WIDTH//2-50, HEIGHT-100))

        # --- Inventory / Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory_screen(player_class, skills, stats, player)
            if event.type == pygame.MOUSEBUTTONDOWN and quest_ui:
                mx,my = event.pos
                if accept_rect.collidepoint(mx,my):
                    quest_copy = quest_ui["quest"].copy()
                    quest_copy["npc"] = quest_ui["name"]
                    player["quests"].append(quest_copy)
                    quest_ui["quest"]=None
                if decline_rect.collidepoint(mx,my):
                    quest_ui["quest"]=None

        pygame.display.flip()
        clock.tick(10)
