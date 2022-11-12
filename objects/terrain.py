from objects.frame import Frame
from objects.block import Block

class Terrain:
    def __init__(self) -> None:
        """Used for background and foreground
        frames - a list of frames from the video
        mode - 0 for background, 1 for foreground
        """
        self.frames: list(Frame)
        self.mode: int
    
    def stitch_frames() -> list(int, int):
        """Stitch frames together and convert to a 2d array of integers"""
        pass
