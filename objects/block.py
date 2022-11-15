from colorsys import rgb_to_hsv, hsv_to_rgb
from constants import MACRO_SIZE
from typing import List, Tuple

# Holds an 8x8 block in a frame
class Block:
    def __init__(self, data, index, position) -> None:
        """
        data - pixel values
        data_type = hsv or rgb
        index - chronological index of frame that holds block
        position - relative to (0,0) within the frame, position of block
        type - foreground(1) or background(0)
        vector - motion vector of block
        """
        self.data: List[List[List[int, int, int]]] = data
        self.data_type = "rgb"
        self.index: int = index
        self.position: Tuple[int, int] = position
        self.type: int
        self.vector: Tuple[int, int]

    def calculate_motion_vector(self, previous_frame_data: List[List[List[int, int, int]]]) -> None:
        """Calculates motion vector based on MAD"""
        # Convert to hsv
        self.convert_to_hsv()
        pass
    
    def convert_to_hsv(self) -> None:
        """Convert pixels to HSV"""
        if self.data_type == "hsv":
            return
        for x in range(MACRO_SIZE):
            for y in range(MACRO_SIZE):
                r, g, b = self.data[x][y]
                self.data[x][y] = rgb_to_hsv(r, g, b)
        self.data_type = "hsv"

    def convert_to_rgb(self) -> None:
        """Convert pixels to RGB"""
        if self.data_type == "rgb":
            return
        for x in range(MACRO_SIZE):
            for y in range(MACRO_SIZE):
                r, g, b = self.data[x][y]
                self.data[x][y] = hsv_to_rgb(r, g, b)
        self.data_type = "rgb"