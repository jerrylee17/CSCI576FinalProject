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
        type - background(0), foreground(1)
        vector - motion vector of block
        """
    self.data: List[List[List[int]]] = data
    self.data_type = "rgb"
    self.index: int = index
    self.position: Tuple[int, int] = position
    self.type: int = 0
    self.vector: Tuple[int, int] = (0, 0)

  def calculate_motion_vector(self, previous_frame_data: List[List[List[int]]]) -> None:
    """Calculates motion vector based on MAD"""
    # Convert to hsv

    self.convert_to_hsv()
    self.frame_convert_to_hsv(previous_frame_data)
    min_MAD: float = sys.float_info.max
    for i in range(self.position[0] - MACRO_SIZE, self.position[0] + MACRO_SIZE, 1):
      for j in range(self.position[1] - MACRO_SIZE, self.position[1] + MACRO_SIZE, 1):
        if self.isValid(i, j, previous_frame_data):
          previous_frame_block = previous_frame_data[i:i + MACRO_SIZE, j:j + MACRO_SIZE]
          MAD: float = self.calculate_block_MAD(previous_frame_block)
          if MAD < min_MAD:
            min_MAD = MAD
            self.vector = (i-self.position[0], j-self.position[1])
    #print(self.vector)
    #print(min_MAD)

  def calculate_block_MAD(self, previous_frame_block: list[list[list[int, int, int]]]) -> int:
    sum: float = 0
    for k in range(MACRO_SIZE):
      for l in range(MACRO_SIZE):
        sum += abs(self.data[k][l][0] - previous_frame_block[k][l][0])
    return sum / (MACRO_SIZE * MACRO_SIZE)

  # def calculate_block_MAD(self, previous_frame_block: list[list[list[int, int, int]]]) -> int:
  #     return np.mean(np.abs(self.data - previous_frame_block))[0]

  def isValid(self, x: int, y: int, previous_frame_data: list[list[list[int, int, int]]]) -> bool:
    return 0 <= x <= len(previous_frame_data) - MACRO_SIZE and 0 <= y <= len(
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

  def frame_convert_to_hsv(self,frame_data:List[List[List[int]]]) -> None:
    for x in range(len(frame_data)):
      for y in range(len(frame_data[0])):
        r, g, b = frame_data[x][y]
        frame_data[x][y] = rgb_to_hsv(r, g, b)

  def convert_to_rgb(self) -> None:
    """Convert pixels to RGB"""
    if self.data_type == "rgb":
      return
    for x in range(MACRO_SIZE):
      for y in range(MACRO_SIZE):
        r, g, b = self.data[x][y]
        self.data[x][y] = hsv_to_rgb(r, g, b)
    self.data_type = "rgb"

def shift_to_right_by_one():
  original_data = np.random.rand(MACRO_SIZE,MACRO_SIZE,3)
  data1 = np.random.rand(MACRO_SIZE,1,3)
  frame =np.concatenate((data1, original_data), axis=1)

  my_block = Block(original_data,1,(0,0))
  my_block.calculate_motion_vector(frame)

def shift_up_by_one():
  original_data = np.random.rand(MACRO_SIZE,MACRO_SIZE,3)
  data1 = np.random.rand(1,MACRO_SIZE,3)
  frame =np.concatenate((data1, original_data), axis=0)

  my_block = Block(original_data,1,(0,0))
  my_block.calculate_motion_vector(frame)

def shift_down_by_one():
  original_data = np.random.rand(MACRO_SIZE,MACRO_SIZE,3)
  my_block = Block(original_data, 1, (1, 0))

  data1 = np.random.rand(1,MACRO_SIZE,3)
  frame = np.concatenate((original_data, data1), axis=0)

  my_block.calculate_motion_vector(frame)

def not_0_0_block():
  original_data = np.random.rand(MACRO_SIZE, MACRO_SIZE, 3)
  my_block = Block(original_data, 1, (10, 10))
  frame = np.random.rand(100, 100, 3)
  index = (3,3)
  frame[index[0]:index[0] + MACRO_SIZE, index[1]: index[1] + MACRO_SIZE] = original_data
  my_block.calculate_motion_vector(frame)

def not_same_data():

  original_data = np.ones((MACRO_SIZE, MACRO_SIZE, 3)) * 10
  my_block = Block(original_data, 1, (0, 0))
  frame = np.ones((100, 100, 3)) * 15
  add = np.ones((MACRO_SIZE, MACRO_SIZE, 3)) * 11

  index = (20, 11)
  frame[index[0]:index[0] + MACRO_SIZE, index[1]: index[1] + MACRO_SIZE] = add
  my_block.calculate_motion_vector(frame)

if __name__ == '__main__':
  #(0,1)
  shift_to_right_by_one()
  # (1,0)
  shift_up_by_one()
  #(-1, 0)
  shift_down_by_one()
  #(3,3)
  not_0_0_block()
