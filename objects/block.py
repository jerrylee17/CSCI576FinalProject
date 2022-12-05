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
    self.HSV_data: List[List[List[int]]] = np.zeros((len(data),len(data[0]),3))
    self.data_type = "rgb"
    self.index: int = index
    self.position: Tuple[int, int] = position
    self.type: int = 0
    self.vector: Tuple[int, int] = (0, 0)

  #position: m x n  previous_frame_data: n x m
  def calculate_motion_vector(self, previous_frame_data: List[List[List[int]]]) -> None:
    """Calculates motion vector based on MAD"""
    self.convert_to_hsv()
    min_MAD: float = sys.float_info.max
    for i in range(self.position[0] - MACRO_SIZE, self.position[0] + MACRO_SIZE + 1, 1):
      for j in range(self.position[1] - MACRO_SIZE, self.position[1] + MACRO_SIZE + 1, 1):
        if self.isValid(i, j, previous_frame_data):
          previous_frame_block = previous_frame_data[j:j + MACRO_SIZE, i:i + MACRO_SIZE, [0, 1, 2]]
          dx = i - self.position[0]
          dy = j - self.position[1]
          MAD: float = self.calculate_block_MAD(previous_frame_block, i, j)

          if MAD < min_MAD:
            min_MAD = MAD
            self.vector = (dx, dy)
          elif MAD == min_MAD and (abs(self.vector[0]) + abs(self.vector[1]) > abs(dx) + abs(dy)):
            self.vector = (dx, dy)
          else:
            continue
    print(self.vector)
    print(min_MAD)

  def calculate_motion_vector_1(self, previous_frame_data: List[List[List[int]]]) -> None:
    """Calculates motion vector based on MAD"""
    min_MAD: float = sys.float_info.max
    for i in range(self.position[0] - MACRO_SIZE, self.position[0] + MACRO_SIZE + 1, 1):
      for j in range(self.position[1] - MACRO_SIZE, self.position[1] + MACRO_SIZE + 1, 1):
        if self.isValid(i, j, previous_frame_data):
          previous_frame_block = previous_frame_data[j:j + MACRO_SIZE, i:i + MACRO_SIZE,:]
          dx = i - self.position[0]
          dy = j - self.position[1]
          MAD: float = self.calculate_block_MAD_1(previous_frame_block)
          if MAD < min_MAD:
            min_MAD = MAD
            self.vector = (dx, dy)
          elif MAD == min_MAD and (abs(self.vector[0]) + abs(self.vector[1]) > abs(dx) + abs(dy)):
            self.vector = (dx, dy)
          else:
            continue
    print(self.vector)

  def calculate_block_MAD(self, previous_frame_block: List[List[List[int]]], i, j) -> float:
    # print(self.HSV_data[:, :, 1])
    # res = np.sum(np.abs(self.HSV_data[:, :, 0] - previous_frame_block[:, :, 0]))

    print(len(self.HSV_data[0][0]), len(previous_frame_block[0][0]))
    #
    res = np.sum(np.abs(self.HSV_data[:, :, 0] - previous_frame_block[:, :, 0]))
    # print("debug 1:" + str(res))
    res += np.sum(np.abs(self.HSV_data[:, :, 1] - previous_frame_block[:, :, 1]))
    # print("debug 2:" + str(res))
    res += np.sum(np.abs(self.HSV_data[:, :, 2] - previous_frame_block[:, :, 2]))
    # print("debug 3:" + str(res))

    # if res == 0 and i != 0 and j != 0:
    #   print("\n===============debug start===============\n")
    #   print(self.HSV_data[:, :, 0])
    #   print(previous_frame_block[:, :, 0])
    #   print("\n===============debug end===============\n")

    return res

  def calculate_block_MAD_1(self, previous_frame_block: List[List[List[int]]]) -> float:
    tmp = np.sum(np.abs(self.data[:, :, :] - previous_frame_block[:, :, :]))
    return np.sum(np.abs(self.data[:, :, :] - previous_frame_block[:, :, :]))


  def isValid(self, x: int, y: int, previous_frame_data: List[List[List[int]]]) -> bool:
    return 0 <= x <= len(previous_frame_data[0]) - MACRO_SIZE and 0 <= y <= len(
      previous_frame_data) - MACRO_SIZE

  def convert_to_hsv(self) -> None:
    """Convert pixels to HSV"""
    if self.data_type == "hsv":
      return
    for x in range(MACRO_SIZE):
      for y in range(MACRO_SIZE):
        r, g, b = self.data[x][y]
        r, g, b = rgb_normalized(r, g, b)
        self.HSV_data[x][y] = hsv_denormalized(rgb_to_hsv(r, g, b))
    self.data_type = "hsv"



  def convert_to_rgb(self) -> None:
    """Convert pixels to RGB"""
    if self.data_type == "rgb":
      return
    for x in range(MACRO_SIZE):
      for y in range(MACRO_SIZE):
        h, s, v = self.data[x][y]
        h, s, v = hsv_normalized(h, s, v)
        self.data[x][y] = rgb_denormalized(hsv_to_rgb(h, s, v))
    self.data_type = "rgb"

h_max = 360
s_max = 100
v_max = 100
def hsv_normalized( h, s, v):
  return (h / h_max, s / s_max, v / v_max)

def hsv_denormalized( ary):
  # print("Debug H: " + str(ary[0]) + " " + str(int(round(ary[0] * h_max))))
  # print("Debug S: " + str(ary[1]) + " " + str(int(round(ary[1] * s_max))))
  # print("Debug V: " + str(ary[2]) + " " + str(int(round(ary[2] * v_max))))
  return (int(round(ary[0] * h_max)), int(round(ary[1] * s_max)), int(round(ary[2] * v_max)))

def rgb_normalized( r, g, b):
  return (r / 255., g / 255., b / 255.)

def rgb_denormalized( ary):
  return (ary[0] * 255, ary[1] * 255, ary[2] * 255)
