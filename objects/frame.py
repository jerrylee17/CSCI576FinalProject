from objects.block import Block
from objects.vector import Vector
# Holds a single frame
class Frame:
    def __init__(self) -> None:
        """
        index - chronological index of frame
        position - relative to frame 0, position of frame
        vector - motion vector of frame (from previous frame)
        """
        self.index: int
        self.position: tuple[int, int]
        self.vector: Vector
        # Could optionally store the blocks within the frame
        self.blocks: list[Block, Block]


