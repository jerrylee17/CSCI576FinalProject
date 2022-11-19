import sys
from colorsys import rgb_to_hsv, hsv_to_rgb
from objects.constants import MACRO_SIZE
from typing import List, Tuple
import numpy as np


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
    self.data: List[List[List[int]]] = data
    self.data_type = "rgb"
    self.index: int = index
    self.position: Tuple[int, int] = position
    self.type: int
    self.vector: Tuple[int, int]

  def calculate_motion_vector(self, previous_frame_data: List[List[List[int]]]) -> None:
    """Calculates motion vector based on MAD"""
    # Convert to hsv
    self.convert_to_hsv()
    min_MAD: float = sys.float_info.max

    for i in range(self.position[0] - MACRO_SIZE, self.position[0] + MACRO_SIZE, 1):
      for j in range(self.position[1] - MACRO_SIZE, self.position[1] + MACRO_SIZE, 1):
        if self.isValid(i, j, previous_frame_data):
          previous_frame_block = previous_frame_data[i:i + MACRO_SIZE, j:j + MACRO_SIZE]
          MAD: float = self.calculate_block_MAD(previous_frame_block)
          if MAD < min_MAD:
            min_MAD = MAD
            self.vector = (i-self.position[0], j-self.position[1])

  def calculate_block_MAD(self, previous_frame_block: list[list[list[int, int, int]]]) -> int:
    sum: float = 0
    for k in range(MACRO_SIZE):
      for l in range(MACRO_SIZE):
        sum += abs(self.data[k][l][0] - previous_frame_block[k][l][0])
    return sum / (MACRO_SIZE * MACRO_SIZE)

  # def calculate_block_MAD(self, previous_frame_block: list[list[list[int, int, int]]]) -> int:
  #     return np.mean(np.abs(self.data - previous_frame_block))[0]

  def isValid(self, x: int, y: int, previous_frame_data: list[list[list[int, int, int]]]) -> bool:
    return 0 <= x < len(previous_frame_data) - MACRO_SIZE and 0 <= y < len(
      previous_frame_data[0]) - MACRO_SIZE

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
