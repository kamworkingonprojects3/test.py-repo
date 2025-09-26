import pygame

# --- Screen ---
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 50

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (65, 105, 225)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 70, 0)
GRAY = (150, 150, 150)
BROWN = (101, 67, 33)
DARK_GRAY = (80, 80, 80)
GOLD = (218, 165, 32)
YELLOW = (255, 255, 0)

# --- Classes and chances ---
classes = ["Warrior", "Mage", "Skeleton", "Archer", "Rogue"]
chances = [30, 25, 15, 20, 10]
total_spins = 5

# Map class to player color
class_colors = {
    "Warrior": RED,
    "Mage": BLUE,
    "Skeleton": DARK_GRAY,
    "Archer": DARK_GREEN,
    "Rogue": GOLD
}

# Class-specific starting skills
class_starting_skills = {
    "Warrior": "Slash",
    "Mage": "Fireball",
    "Skeleton": "Bone Throw",
    "Archer": "Arrow Shot",
    "Rogue": "Backstab"
}

# Skill descriptions
skill_descriptions = {
    "Slash": "Cuts a tree in front of you.",
    "Fireball": "Launch a fireball forward.",
    "Bone Throw": "Throw a bone at enemies.",
    "Arrow Shot": "Shoot an arrow forward.",
    "Backstab": "Deal extra damage from behind."
}

# Player starting stats (normalized to lowercase keys to avoid KeyError)
class_starting_stats = {
    "Warrior": {"max_hp":100,"hp": 100, "attack": 15, "defense": 10, "speed": 5, "level": 5},
    "Mage": {"max_hp":80,"hp": 80, "attack": 20, "defense": 5, "speed": 6, "level": 5},
    "Skeleton": {"max_hp":70,"hp": 70, "attack": 10, "defense": 5, "speed": 7, "level": 5},
    "Archer": {"max_hp":90,"hp": 90, "attack": 12, "defense": 8, "speed": 6, "level": 5},
    "Rogue": {"max_hp":85,"hp": 85, "attack": 14, "defense": 6, "speed": 8, "level": 5}
}


# Skill colors
skill_colors = {
    "Slash": RED,
    "Fireball": BLUE,
    "Arrow Shot": GOLD,
    "Backstab": YELLOW,
    "Bone Throw": DARK_GRAY
}

ENCOUNTER_CHANCE = 0.02  # 10% chance per step on grass tile

# Zones for map generation
ZONES = [
    {
        "name": "Meadow",
        "x_range": (-50, 50),
        "y_range": (-50, 50),
        "tiles": ["grass", "tree", "boulder"],
        "encounter_chance": 0.05
    },
    {
        "name": "Dark Forest",
        "x_range": (51, 100),
        "y_range": (-50, 50),
        "tiles": ["tree", "boulder"],
        "encounter_chance": 0.15
    },
    {
        "name": "Desert",
        "x_range": (-100, -51),
        "y_range": (-50, 50),
        "tiles": ["sand", "rock"],
        "encounter_chance": 0.08
    }
]
