from objects.terrain import Terrain
from objects.frame import Frame
from typing import List

def generate_background(frames: List[Frame]) -> List[List[List[int]]]:
    """Generate stitched background"""
    terrain = Terrain(frames, 0)
    background = terrain.get_terrain()
    return background
