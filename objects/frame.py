from objects.block import Block
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
        self.vector: tuple[int, int]
        # Store values in the blocks within the frame
        self.blocks: list[Block, Block]

    def read_into_blocks(pixels: list[list[list[int, int, int]]]) -> None:
        """Read 2D array of pixels into self.blocks"""
        pass

    def calculate_average_motion_vector(self) -> None:
        """Determine camera movement by average motion vector"""
        pass

    def calculate_mode_motion_vector(self) -> None:
        """Determine camera movement by most occuring motion vector"""
        pass

    def set_block_visibility(self) -> None:
        """Set blocks to foreground or background"""
        pass
