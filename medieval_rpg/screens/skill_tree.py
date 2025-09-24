class_skills_tree = {
    "Warrior": {
        "tier1": ["Slash", "Shield Bash"],
        "tier2": ["Power Strike", "Armor Up"],
        "tier3": ["Berserk", "Earthquake"]
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

def skill_tree_screen(player_class, player, screen, font, clock):
    tree = class_skills_tree[player_class]
    running = True

    # Node positions for visual layout
    positions = {
        "tier1": [(200, 150), (400, 150)],
        "tier2": [(200, 300), (400, 300)],
        "tier3": [(300, 450), (500, 450)]
    }

    tier_levels = {"tier1": 5, "tier2": 10, "tier3": 20}

    while running:
        screen.fill((50, 50, 50))

        # Draw skill nodes
        for tier, skills in tree.items():
            req_level = tier_levels[tier]
            for i, skill in enumerate(skills):
                x, y = positions[tier][i] if i < len(positions[tier]) else (100+i*100, 100)
                color = (100, 100, 100)  # locked by default
                if skill in player["skills"]:
                    color = (0, 255, 0)  # unlocked
                elif player["level"] >= req_level:
                    color = (255, 255, 0)  # unlockable
                pygame.draw.rect(screen, color, (x, y, 120, 40))
                text = font.render(skill, True, BLACK)
                lvl_text = font.render(f"Lvl {req_level}", True, BLACK)
                screen.blit(text, (x + 60 - text.get_width()//2, y + 10))
                screen.blit(lvl_text, (x + 60 - lvl_text.get_width()//2, y + 25))

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

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for tier, skills in tree.items():
                    req_level = tier_levels[tier]
                    for i, skill in enumerate(skills):
                        x, y = positions[tier][i] if i < len(positions[tier]) else (100+i*100, 100)
                        rect = pygame.Rect(x, y, 120, 40)
                        if rect.collidepoint(mx, my) and player["level"] >= req_level:
                            if skill not in player["skills"]:
                                for idx in range(len(player["skills"])):
                                    if player["skills"][idx] == "":
                                        player["skills"][idx] = skill
                                        break

        pygame.display.flip()
        clock.tick(30)
