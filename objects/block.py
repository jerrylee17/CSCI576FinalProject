from objects.frame import Frame
from objects.pixel import Pixel
from objects.vector import Vector
# Holds an 8x8 block in a frame
class Block:
    def __init__(self) -> None:
        """
        index - chronological index of frame that holds block
        position - relative to (0,0) within the frame, position of block
        type - foreground(1) or background(0)
        vector - motion vector of block
        """
        self.data: list[list[Pixel]]
        self.index: int
        self.position: tuple[int, int]
        self.type: int
        self.vector: Vector

    def calculate_motion_vector(previous_frame: Frame) -> None:
        """Calculates motion vector based on MAD"""
        pass