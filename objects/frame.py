from objects.block import Block
from objects.constants import MACRO_SIZE, THREHOLDX, THREHOLDY
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
        for i in range(len(self.blocks)):
            self.blocks[i].calculate_motion_vector(previous_frame_data)
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
                data = pixels[y:y + MACRO_SIZE, x:x + MACRO_SIZE,]
                block = Block(data, self.index, (x, y))
                self.blocks.append(block)

    def calculate_average_motion_vector(self) -> None:
        """Determine camera movement by average motion vector"""
        #assume self.blocks is not empty
        numBlocks=len(self.blocks)
        summ=[0,0]
        for i in range(numBlocks):
            tmpVector=self.blocks[i].vector
            summ[0]+=tmpVector[0]
            summ[1]+=tmpVector[1]
        self.vector=(round(summ[0]/numBlocks),round(summ[1]/numBlocks))

    def calculate_mode_motion_vector(self) -> None:
        """Determine camera movement by most occuring motion vector"""
        allVector=[]
        for block in self.blocks:
            allVector.append(block.vector)
        self.vector=max(set(allVector), key = allVector.count)

    def set_block_visibility(self) -> None:
        """Set blocks to foreground or background"""
        numBlocks=len(self.blocks)
        threhold=[THREHOLDX,THREHOLDY]
        for i in range(numBlocks):
            if self.blocks[i].vector[0]>threhold[0] and self.blocks[i].vector[1]>threhold[1]:
                self.blocks[i].type=1
            else:
                self.blocks[i].type=0

    def get_frame_data(self) -> List[List[List[int]]]:
        """Retrieve all values in frame"""
        x_blocks = self.width // MACRO_SIZE
        y_blocks = self.height // MACRO_SIZE
        blocks = np.array(self.blocks).reshape(y_blocks, x_blocks)
        frame_data = []
        for block_row in blocks:
            # print([np.array(x.data).shape for x in block_row])
            block_row = [x.data for x in block_row]
            block_row = np.concatenate(block_row, axis = 1)
            frame_data.extend(block_row)
        frame_data = np.array(frame_data)
        return frame_data

    def get_frame_foreground_center(self)-> List[Tuple[int, int]]:
        """Calculate center position of frame"""
        x_blocks = self.width // MACRO_SIZE
        y_blocks = self.height // MACRO_SIZE
        blocks = np.array(self.blocks).reshape(y_blocks, x_blocks)
        x_count, x_sum, y_count, y_sum = 0
        for y, column in enumerate(blocks):
            for x, cell in enumerate(column):
                if cell.type == 0: continue
                x_count += 1
                y_count += 1
                x_sum += y
                x_sum += x
        x_center = MACRO_SIZE * (x_sum / x_count)
        y_center = MACRO_SIZE * (y_sum / y_count)
        return (x_center, y_center)
            

    def get_frame_foreground(self) -> List[List[List[int]]]:
        x_blocks = self.width // MACRO_SIZE
        y_blocks = self.height // MACRO_SIZE
        blocks = np.array(self.blocks)
        for block in blocks:
            if block.type == 0:
                block.data = np.zeros((MACRO_SIZE, MACRO_SIZE))
        blocks = blocks.reshape(y_blocks, x_blocks)
        frame_data = []
        for block_row in blocks:
            # print([np.array(x.data).shape for x in block_row])
            block_row = [x.data for x in block_row]
            block_row = np.concatenate(block_row, axis = 1)
            frame_data.extend(block_row)
        frame_data = np.array(frame_data)
        return frame_data

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
    frame = Frame(0, height, width,0,0)
    testVector=[(1,1),(2,2),(2,2),(4,4)]
    for i in range(len(testVector)):
        testBlock=Block(0,0,0)
        testBlock.vector=testVector[i]
        frame.blocks.append(testBlock)
    frame.calculate_mode_motion_vector()
    print(frame.vector)

def test_calculate_average_motion_vector():
    width = 496
    height = 272
    frame = Frame(0, height, width,0,0)
    testVector=[(1,1),(2,2),(3,3),(4,4),(5,5)]
    for i in range(len(testVector)):
        testBlock=Block(0,0,0)
        testBlock.vector=testVector[i]
        frame.blocks.append(testBlock)
    frame.calculate_average_motion_vector()
    print(frame.vector)

def test_set_block_visibility():
    width = 496
    height = 272
    frame = Frame(0, height, width,0,0)
    testVector=[(1,1),(2,2),(2,2),(4,4)]
    for i in range(len(testVector)):
        testBlock=Block(0,0,0)
        testBlock.vector=testVector[i]
        frame.blocks.append(testBlock)
    frame.set_block_visibility()
    for i in frame.blocks:
        print("The type for "+str(i.vector)+" is: "+str(i.type))


# test_calculate_mode_motion_vector()
# test_calculate_average_motion_vector()
# test_set_block_visibility()
# test_read_into_blocks()