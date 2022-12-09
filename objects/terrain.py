from copy import deepcopy
from objects.frame import Frame
from objects.block import Block
from objects.constants import MACRO_SIZE,FILLINFRAMES
from typing import List
import numpy as np

class Terrain:
    def __init__(self, frames: List[Frame], mode=0) -> None:
        """Used for background and foreground
        pixels - terrain pixels
        frames - a list of frames from the video
        mode - background(0), foreground(1)
        """
        self.pixels: List[List[List[int]]]
        self.frames: List[Frame] = frames
        # List of frame offsets [x_offset, y_offset]
        self.frame_offsets: List[List[int]] = []
        self.mode: int = mode
        self.y_offset = 0
        self.x_offset = 0
    
    def get_frame_position_bounds_(self):
        """Returns min/max x/y for frame position"""
        frame_x = self.frames[0].width
        frame_y = self.frames[0].height
        min_x_index = min(frame.position[0] for frame in self.frames)
        max_x_index = max(frame.position[0] for frame in self.frames) + frame_x
        min_y_index = min(frame.position[1] for frame in self.frames)
        max_y_index = max(frame.position[1] for frame in self.frames) + frame_y
        return min_x_index, max_x_index, min_y_index, max_y_index
    
    def stitch_frames(self) -> None:
        """Stitch frames together and convert to a 2d array of pixels"""
        min_x, max_x, min_y, max_y = self.get_frame_position_bounds_()
        # Add offset from (0,0) in the terrain pixels
        x_offset, y_offset = abs(min_x), abs(min_y)
        self.x_offset, self.y_offset = x_offset, y_offset
        x_length, y_length = max_x - min_x, max_y - min_y
        self.pixels = np.zeros((y_length, x_length, 3))
        self.pixels.fill(-1)
        for frame in self.frames:
            for block in frame.blocks:
                if block.type != self.mode: continue
                y_start = frame.position[1] + block.position[1] + y_offset
                x_start = frame.position[0] + block.position[0] + x_offset
                x_end, y_end = x_start + MACRO_SIZE, y_start + MACRO_SIZE
                # If these pixels are untouched, directly replace them
                untouched_pixels = np.zeros((y_length, x_length, 3))
                untouched_pixels.fill(-1)
                if np.array_equal(self.pixels[y_start: y_end, x_start: x_end],
                    untouched_pixels):
                    self.pixels[y_start: y_end, x_start: x_end] = block.data
                # Otherwise, need some calculations
                else:
                    # Temporarily setting this right now
                    self.pixels[y_start: y_end, x_start: x_end] = block.data
                    # Please set self.frame_offsets[i] as [x_offset, y_offset]

    def get_terrain(self) -> List[List[List[int]]]:
        """Return entire terrain"""
        # self.stitch_frames()
        return self.pixels

    def synchronize(self, background):
        """Synchronize foreground pixel indecies with background terrain size"""
        if self.mode == 0:
            return
        pass

    def paste_foreground_frames(self, frames: List[Frame]):
        untouched_pixels = np.ones((MACRO_SIZE, MACRO_SIZE, 3))*255
        for frame in frames:
            for block in frame.blocks:
                # Must be foreground
                if block.type != 1: continue
                y_start = frame.position[1] + block.position[1] + self.y_offset
                x_start = frame.position[0] + block.position[0] + self.x_offset
                x_end, y_end = x_start + MACRO_SIZE, y_start + MACRO_SIZE
                self.pixels[y_start: y_end, x_start: x_end] = block.data
    
    def get_frame_path(self) -> List[List[List[List[int]]]]:
        """
        Calculate x/y interval --> len(width) / num frames, len(height) / num_frames
        For each frame --> temporarily paste foreground on background and query from there
        """
        width = len(self.pixels[0])
        height = len(self.pixels)
        frame_width = self.frames[0].width
        frame_height = self.frames[0].height
        x_interval = max((width - frame_width) // len(self.frames), 1)
        y_interval = max((height - frame_height) // len(self.frames), 1)
        split_x = [x for x in range(0, width - frame_width, x_interval)]
        split_y = [y for y in range(0, height - frame_height, y_interval)]
        # Populate split y / x
        if len(split_y) < len(split_x):
            len_diff = len(split_x) - len(split_y)
            split_y = [0] * len_diff + split_y
        if len(split_x) < len(split_y):
            len_diff = len(split_y) - len(split_x)
            split_x = [0] * len_diff + split_x
        frames = []
        for i, (x_start, y_start) in enumerate(zip(split_x, split_y)):
            if i >= len(self.frames):
                break
            frame = self.frames[i]
            tmp_pixels = deepcopy(self.pixels)
            for block in frame.blocks:
                # Must be foreground
                if block.type != 1: continue
                block_y_start = frame.position[1] + block.position[1] + self.y_offset
                block_x_start = frame.position[0] + block.position[0] + self.x_offset
                block_x_end, block_y_end = block_x_start + MACRO_SIZE, block_y_start + MACRO_SIZE
                tmp_pixels[block_y_start: block_y_end, block_x_start: block_x_end] = block.data
            x_end, y_end = x_start + frame_width, y_start + frame_height
            new_frame = tmp_pixels[y_start: y_end, x_start: x_end]
            new_frame = np.array(new_frame)
            frames.append(new_frame)
        return frames

    def get_background_frame_positions(self) -> List[List[List[List[int]]]]:
        frames = []
        for frame in self.frames:
            x_blocks = frame.width // MACRO_SIZE
            y_blocks = frame.height // MACRO_SIZE
            blocks = deepcopy(frame.blocks)
            for block in blocks:
                if block.type == 1:
                    block.data = np.ones((MACRO_SIZE, MACRO_SIZE, 3)) * -1
            blocks = np.array(blocks)
            blocks = blocks.reshape(y_blocks, x_blocks)
            frame_data = []
            for block_row in blocks:
                block_row = [x.data for x in block_row]
                block_row = np.concatenate(block_row, axis=1)
                frame_data.extend(block_row)
            frame_data = np.array(frame_data)
            # Change pixels that are [-1,-1,-1]
            for y in range(len(frame_data)):
                for x in range(len(frame_data[0])):
                    if frame_data[y][x][0] != -1: continue
                    x_index = frame.position[0] + x + self.x_offset
                    y_index = frame.position[1] + y + self.y_offset
                    frame_data[y, x] = self.pixels[y_index, x_index]
            frames.append(frame_data)
        return frames

    def fill_hole(self):
        step=FILLINFRAMES
        filledFrames=[]
        #not fill in the last frames 
        for index in range(len(self.frames)-step):
            tmpFrame=self.frames[index]
            blockInd=0
            for block in tmpFrame.blocks:
                backupBlock=block
                roundCnt=1
                sum_offset_x=0
                sum_offset_y=0
                while backupBlock.type == 1 and (index+step*roundCnt)<len(self.frames):
                    round_offset_x,round_offset_y=self.get_backup_block(roundCnt,index)
                    sum_offset_x+=round_offset_x
                    sum_offset_y+=round_offset_y
                    offset_Ind=self.calculate_block_offset((-1)*sum_offset_x,(-1)*sum_offset_y)
                    if blockInd+offset_Ind<len(self.frames[index+step*roundCnt].blocks):
                        backupBlock=self.frames[index+step*roundCnt].blocks[blockInd+offset_Ind]
                    roundCnt+=1
                if block.type==1:
                    if backupBlock.type == 0:
                        self.frames[index].blocks[blockInd]=deepcopy(backupBlock)
                    # elif (index-step*2)>=0:
                        # backupBlockRev=self.fill_hole_reverse(index,block,blockInd)
                        # if backupBlockRev.type== 0:
                            # self.frames[index].blocks[blockInd]=deepcopy(backupBlockRev)
                        # self.frames[index].blocks[blockInd]=deepcopy(backupBlockRev)
                blockInd+=1
            filledFrames.append(self.frames[index])
        self.frames=filledFrames

    def calculate_block_offset(self,offset_x,offset_y):
        block_width= self.frames[0].width // MACRO_SIZE
        offset_ind_x=offset_x//MACRO_SIZE
        offset_ind_y=offset_y//MACRO_SIZE
        offset_Ind=(-1)*offset_ind_y*block_width+offset_ind_x
        return offset_Ind
    
    def get_backup_block(self,roundCnt,index):
        step=FILLINFRAMES
        round_offset_x=0
        round_offset_y=0
        for s in range(step):
            round_offset_x+=self.frames[index+step*(roundCnt-1)+s].vector[0]
            round_offset_y+=self.frames[index+step*(roundCnt-1)+s].vector[1]
        return round_offset_x,round_offset_y

    def fill_hole_reverse(self,index,block,blockInd)->Block:
        step=FILLINFRAMES
        # roundCnt=0
        sum_offset_x=0
        sum_offset_y=0
        backupBlockRev=block
        # for ind_frame in range(index,-1,-1):
            # round_offset_x=0
            # round_offset_y=0
        for s in range(step*2):
            sum_offset_x+=self.frames[index-s].vector[0]
            sum_offset_y+=self.frames[index-s].vector[1]
        revInd=self.calculate_block_offset((-1)*sum_offset_x,(-1)*sum_offset_y)
        backupBlockRev=self.frames[index-step*2].blocks[blockInd+revInd]
        return backupBlockRev