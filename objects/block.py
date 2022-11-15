from pixel import Pixel

# Holds an 8x8 block in a frame
class Block:
    def __init__(self, data, index, position) -> None:
        """
        index - chronological index of frame that holds block
        position - relative to (0,0) within the frame, position of block
        type - foreground(1) or background(0)
        vector - motion vector of block
        """
        self.data: list[list[list[int, int, int]]] = data
        self.index: int = index
        self.position: tuple[int, int] = position
        self.type: int
        self.vector: tuple[int, int]

    def calculate_motion_vector(previous_frame) -> None:
        """Calculates motion vector based on MAD"""
        pass
    