import random

# --- Zone Classes ---
class Zone:
    def __init__(self, name, tileset, encounter_rate, feature=None):
        self.name = name
        self.tileset = tileset  # dict mapping tile types to colors
        self.encounter_rate = encounter_rate  # float probability
        self.feature = feature  # function to randomly place features

# --- Feature Functions ---
def forest_feature(tilemap, x, y, w, h):
    # Place random trees, avoid overlapping existing obstacles
    for _ in range(random.randint(1, 3)):
        tx = x + random.randint(0, w-1)
        ty = y + random.randint(0, h-1)
        if tilemap.get_tile(tx, ty) == 'grass':
            tilemap.set_tile(tx, ty, 'tree')

def plains_feature(tilemap, x, y, w, h):
    # Place sparse boulders every ~10 tiles
    if random.randint(0, 10) < 2:  # ~2 boulders per 10 tiles
        bx = x + random.randint(0, w-1)
        by = y + random.randint(0, h-1)
        if tilemap.get_tile(bx, by) == 'grass':
            tilemap.set_tile(bx, by, 'boulder')

# --- Tileset Colors ---
forest_tileset = {
    'grass': (34, 139, 34),
    'tree': (0, 100, 0),
    'boulder': (105, 105, 105),
    'village': (210, 180, 140)
}

plains_tileset = {
    'grass': (144, 238, 144),
    'tree': (34, 139, 34),
    'boulder': (139, 69, 19),
    'village': (210, 180, 140)
}

# --- Zones ---
forest_zone = Zone("Forest", forest_tileset, encounter_rate=0.05, feature=forest_feature)
plains_zone = Zone("Plains", plains_tileset, encounter_rate=0.02, feature=plains_feature)

# --- Zone Map (simple) ---
def get_zone_at(x, y):
    # Example logic: left side forest, right side plains
    if x < 0:
        return forest_zone
    else:
        return plains_zone
