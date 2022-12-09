from objects.block import Block, rgb_normalized, hsv_denormalized
from objects.constants import MACRO_SIZE, THRESHOLDX, THRESHOLDY
from random import randint
import numpy as np
from typing import List, Tuple
from colorsys import rgb_to_hsv, hsv_to_rgb
from copy import deepcopy


# Holds a single frame
class Frame:
  def __init__(self, index, width, height) -> None:
    """
    index - chronological index of frame
    position - relative to frame 0, position of frame
    vector - motion vector of frame (from previous frame)
    """
    self.index: int = index
    # Revert position
    self.position: Tuple[int, int]
    self.vector: Tuple[int, int]
    self.width: int = width
    self.height: int = height
    # Store values in the blocks within the frame
    self.blocks: List[Block] = []
    self.pad_x = 0
    self.pad_y = 0

  def get_zero_padding_size_(self, width: int, height: int):
    """Calculate the cols and rows of zeros that need to be padded."""
    zero_padding_cols = MACRO_SIZE - (width % MACRO_SIZE)
    if zero_padding_cols == MACRO_SIZE:
      zero_padding_cols = 0

    zero_padding_rows = MACRO_SIZE - (height % MACRO_SIZE)
    if zero_padding_rows == MACRO_SIZE:
      zero_padding_rows = 0

    return zero_padding_rows, zero_padding_cols

  def calculate_block_motion_vector(self, previous_frame_data: List[List[List[int]]]) -> None:
    self.frame_convert_to_hsv(previous_frame_data)
    for i in range(len(self.blocks)):
    #   if i == 22:
    #     print("---")
    #   print("Block " + str(i) + ":")
      self.blocks[i].calculate_motion_vector(previous_frame_data)
      if not self.blocks[i].vector:
        print(i)

  def calculate_block_motion_vector_1(self, previous_frame_data: List[List[List[int]]]) -> None:
    for i in range(len(self.blocks)):
      self.blocks[i].calculate_motion_vector_1(previous_frame_data)
      if not self.blocks[i].vector:
        print(i)

  def read_into_blocks(self, pixels: List[List[List[int]]]) -> None:
    """Read 2D array of pixels into self.blocks"""
    pixels = np.array(pixels)
    self.pad_x, self.pad_y = self.get_zero_padding_size_(self.width, self.height)
    self.width = self.width + self.pad_y
    self.height = self.height + self.pad_x
    pixels = np.pad(
      pixels,
      [(0, self.pad_x), (0, self.pad_y), (0, 0)],
      mode='constant', constant_values=0)
    split_x = [x for x in range(0, self.width, MACRO_SIZE)]
    split_y = [y for y in range(0, self.height, MACRO_SIZE)]
    for y in split_y:
      for x in split_x:
        data = pixels[y:y + MACRO_SIZE, x:x + MACRO_SIZE, ]

        block = Block(data, self.index, (x, y))
        self.blocks.append(block)

  def calculate_frame_position(self, previous_frame):
    self.position = (
      previous_frame.position[0] + self.vector[0],
      previous_frame.position[1] + self.vector[1]
    )

  def calculate_average_motion_vector(self) -> None:
    """Determine camera movement by average motion vector"""
    # assume self.blocks is not empty
    numBlocks = len(self.blocks)
    summ = [0, 0]
    for i in range(numBlocks):
      tmpVector = self.blocks[i].vector
      summ[0] += tmpVector[0]
      summ[1] += tmpVector[1]
    self.vector = (round(summ[0] / numBlocks), round(summ[1] / numBlocks))

  def calculate_mode_motion_vector(self) -> None:
    """Determine camera movement by most occuring motion vector"""
    allVector = []
    for block in self.blocks:
      allVector.append(block.vector)
    self.vector = max(set(allVector), key=allVector.count)

  def set_block_visibility(self) -> None:
    """Set blocks to foreground or background"""
    numBlocks = len(self.blocks)
    block_width = self.width / MACRO_SIZE
    for i in range(numBlocks):
      if i < block_width or i >= numBlocks - block_width:
        continue
      if i % block_width == 0 or i % block_width == block_width - 1:
        continue
      if (abs(self.blocks[i].vector[0] - self.vector[0]) > THRESHOLDX) or (
       abs(self.blocks[i].vector[1] - self.vector[1]) > THRESHOLDY
      ):
        self.blocks[i].type = 1

  def remove_individual_foreground_block(self) -> None:
    """
    If a block is set to foreground but not adjacent to any other
    foreground block, set it back to background
    """
    num_blocks = len(self.blocks)
    block_width = self.width / MACRO_SIZE
    offsets = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    for i in range(num_blocks):
      if self.blocks[i].type != 1: continue

      is_individual = True

      x = int(i % block_width)
      y = int(i / block_width)
      for offset in offsets:
        nx = x + offset[0]
        ny = y + offset[1]
        nidx = int(nx + ny * block_width)
        if 0 <= nidx < num_blocks:
          if self.blocks[nidx].type == 1:
            is_individual = False
            break

      if (is_individual): self.blocks[i].type = 0

  def human_detection(self, detector) -> None:
    human_boxs = detector.get_human_position(self.get_frame_data())
    if len(human_boxs) == 0:
      return
    for block in self.blocks:
      if self.in_boxes(human_boxs, block.position):
        #block.type = 1
        continue
      else:
        block.type = 0

  def in_boxes(self, human_boxs, position):
    for box in human_boxs:
      box = ( box[0] // MACRO_SIZE * MACRO_SIZE, box[1] // MACRO_SIZE * MACRO_SIZE, box[2] // MACRO_SIZE * MACRO_SIZE,box[3] // MACRO_SIZE * MACRO_SIZE)
      if box[0] <= position[1] <= box[2] and box[1] <= position[0] <= box[3]:
        return True
    return False

  def get_frame_data(self) -> List[List[List[int]]]:
    """Retrieve all values in frame"""
    x_blocks = self.width // MACRO_SIZE
    y_blocks = self.height // MACRO_SIZE
    blocks = np.array(self.blocks).reshape(y_blocks, x_blocks)
    frame_data = []
    for block_row in blocks:
      block_row = [x.data for x in block_row]
      block_row = np.concatenate(block_row, axis=1)
      frame_data.extend(block_row)
    frame_data = np.array(frame_data)
    return frame_data

  def get_frame_foreground_center(self) -> List[Tuple[int, int]]:
    """Calculate center position of frame"""
    x_blocks = self.width // MACRO_SIZE
    y_blocks = self.height // MACRO_SIZE
    blocks = np.array(self.blocks).reshape(y_blocks, x_blocks)
    x_count, x_sum, y_count, y_sum = 0, 0, 0, 0
    for y, column in enumerate(blocks):
      for x, cell in enumerate(column):
        if cell.type == 0: continue
        x_count += 1
        y_count += 1
        x_sum += y
        x_sum += x
    try:
      x_center = MACRO_SIZE * (x_sum // x_count)
      y_center = MACRO_SIZE * (y_sum // y_count)
    except:
      x_center = 0
      y_center = 0
    return (x_center, y_center)

  def get_frame_foreground(self) -> List[List[List[int]]]:
    x_blocks = self.width // MACRO_SIZE
    y_blocks = self.height // MACRO_SIZE
    blocks = deepcopy(self.blocks)
    for block in blocks:
      if block.type == 0:
        block.data = np.ones((MACRO_SIZE, MACRO_SIZE, 3)) * 255
    blocks = np.array(blocks)
    blocks = blocks.reshape(y_blocks, x_blocks)
    frame_data = []
    for block_row in blocks:
      block_row = [x.data for x in block_row]
      block_row = np.concatenate(block_row, axis=1)
      frame_data.extend(block_row)
    frame_data = np.array(frame_data)
    return frame_data

  def frame_convert_to_hsv(self, frame_data: List[List[List[int]]]) -> None:
    for x in range(len(frame_data)):
      for y in range(len(frame_data[0])):
        r, g, b = frame_data[x][y]
        r, g, b = rgb_normalized(r, g, b)
        frame_data[x][y] = hsv_denormalized(rgb_to_hsv(r, g, b))


def test_read_into_blocks():
  width = 496
  height = 272
  test = np.array([[[randint(0, 255) for i in range(3)] for j in range(width)] for k in range(height)])
  # test = np.array([[0 for j in range(width)] for k in range(height)])
  frame = Frame(0, height, width)
  frame.read_into_blocks(test)
  # Check first and last frame
  # first_frame_expected = test[0:16, 0:16]
  # last_frame_expected = test[height - 16:height, width - 16:width]
  # print(first_frame_expected == frame.blocks[0].data)
  # print(last_frame_expected == frame.blocks[-1].data)
  frame_data = frame.get_frame_data()
  print("===========")
  print(frame_data.shape)


def test_calculate_mode_motion_vector():
  width = 496
  height = 272
  frame = Frame(0, height, width, 0, 0)
  testVector = [(1, 1), (2, 2), (2, 2), (4, 4)]
  for i in range(len(testVector)):
    testBlock = Block(0, 0, 0)
    testBlock.vector = testVector[i]
    frame.blocks.append(testBlock)
  frame.calculate_mode_motion_vector()
  print(frame.vector)


def test_calculate_average_motion_vector():
  width = 496
  height = 272
  frame = Frame(0, height, width, 0, 0)
  testVector = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
  for i in range(len(testVector)):
    testBlock = Block(0, 0, 0)
    testBlock.vector = testVector[i]
    frame.blocks.append(testBlock)
  frame.calculate_average_motion_vector()
  print(frame.vector)


def test_set_block_visibility():
  width = 496
  height = 272
  frame = Frame(0, height, width, 0, 0)
  testVector = [(1, 1), (2, 2), (2, 2), (4, 4)]
  for i in range(len(testVector)):
    testBlock = Block(0, 0, 0)
    testBlock.vector = testVector[i]
    frame.blocks.append(testBlock)
  frame.set_block_visibility()
  for i in frame.blocks:
    print("The type for " + str(i.vector) + " is: " + str(i.type))

# test_calculate_mode_motion_vector()
# test_calculate_average_motion_vector()
# test_set_block_visibility()
# test_read_into_blocks()
