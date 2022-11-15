from objects.block import Block
from objects.constants import MACRO_SIZE
from random import randint
import numpy as np
from typing import List, Tuple

# Holds a single frame
class Frame:
    def __init__(self, index, width, height) -> None:
        """
        index - chronological index of frame
        position - relative to frame 0, position of frame
        vector - motion vector of frame (from previous frame)
        """
        self.index: int = index
        self.position: Tuple[int, int]
        self.vector: Tuple[int, int]
        self.width: int = width
        self.height: int = height
        # Store values in the blocks within the frame
        self.blocks: List[Block, Block] = []

    def read_into_blocks(self, pixels: List[List[List[int]]]) -> None:
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

    def get_frame_data(self) -> List[List[List[int]]]:
        """Retrieve all values in frame"""
        x_blocks = self.width // MACRO_SIZE
        y_blocks = self.height // MACRO_SIZE
        blocks = np.array(self.blocks).reshape(x_blocks, y_blocks)
        frame_data = []
        for block_row in blocks:
            block_row = [x.data for x in block_row]
            block_row = np.concatenate(block_row, axis = 1)
            frame_data.extend(block_row)
        return frame_data

def test_read_into_blocks():
    test = np.array([[[randint(0, 255) for i in range(3)] for j in range(480)] for k in range(640)])
    # test = np.array([[0 for j in range(480)] for k in range(640)])
    frame = Frame(0, 640, 480)
    frame.read_into_blocks(test)
    # Check first and last frame
    first_frame_expected = test[0:16, 0:16]
    last_frame_expected = test[624:640, 464:480]
    # print(first_frame_expected == frame.blocks[0].data)
    # print(last_frame_expected == frame.blocks[-1].data)
    frame_data = frame.get_frame_data()
    print("===========")
    print(frame_data == test)
