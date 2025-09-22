# entities/collision.py

def can_move(tilemap, tx, ty):
    """
    Returns True if the player can move onto the tile (tx, ty)
    Blocks movement on trees, boulders, and outside village collision if needed.
    """
    tile_type = tilemap.get_tile(tx, ty)
    if tile_type in ["tree", "boulder"]:
        return False
    return True
