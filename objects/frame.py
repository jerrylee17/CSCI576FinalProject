from block import Block
from random import randint
import numpy as np

MACRO_SIZE = 16

# Holds a single frame
class Frame:
    def __init__(self, index, width, height) -> None:
        """
        index - chronological index of frame
        position - relative to frame 0, position of frame
        vector - motion vector of frame (from previous frame)
        """
        self.index: int = index
        self.position: tuple[int, int]
        self.vector: tuple[int, int]
        self.width: int = width
        self.height: int = height
        # Store values in the blocks within the frame
        self.blocks: list[Block, Block] = []

    def read_into_blocks(self, pixels: list[list[list[int, int, int]]]) -> None:
        """Read 2D array of pixels into self.blocks"""
        split_x = [x for x in range(0, self.width, MACRO_SIZE)]
        split_y = [y for y in range(0, self.height, MACRO_SIZE)]
        for x in split_x:
            for y in split_y:
                data = pixels[x:x + MACRO_SIZE, y:y + MACRO_SIZE]
                block = Block(data, self.index, (x, y))
                self.blocks.append(block)

    def calculate_average_motion_vector(self) -> None:
        """Determine camera movement by average motion vector"""
        pass

    def calculate_mode_motion_vector(self) -> None:
        """Determine camera movement by most occuring motion vector"""
        pass

    def set_block_visibility(self) -> None:
        """Set blocks to foreground or background"""
        pass


def test_read_into_blocks():
    test = np.array([[[randint(0, 100) for i in range(3)] for j in range(480)] for k in range(640)])
    # test = np.array([[0 for j in range(480)] for k in range(640)])
    frame = Frame(0, 640, 480)
    frame.read_into_blocks(test)
    # Check first and last frame
    first_frame_expected = test[0:16, 0:16]
    last_frame_expected = test[624:640, 464:480]
    print(first_frame_expected == frame.blocks[0].data)
    print(last_frame_expected == frame.blocks[-1].data)

