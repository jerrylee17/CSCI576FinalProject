from objects.frame import Frame
from objects.block import Block
from typing import List

class Terrain:
    def __init__(self) -> None:
        """Used for background and foreground
        frames - a list of frames from the video
        mode - 0 for background, 1 for foreground
        """
        self.pixels: List[List[List[int]]]
        self.frames: List[Frame]
        self.mode: int
    
    def stitch_frames(self) -> None:
        """Stitch frames together and convert to a 2d array of pixels"""
        pass

    def get_terrain(self) -> List[List[List[int]]]:
        """Return entire terrain"""
        self.stitch_frames()
        return self.frames

    def synchronize(self, background):
        """Synchronize foreground pixel indecies with background terrain size"""
        if self.mode == 0:
            return
        pass
