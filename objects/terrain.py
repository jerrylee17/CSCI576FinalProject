from objects.frame import Frame
from objects.block import Block
from objects.constants import MACRO_SIZE
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
        self.stitch_frames()
        return self.pixels

    def synchronize(self, background):
        """Synchronize foreground pixel indecies with background terrain size"""
        if self.mode == 0:
            return
        pass

    def paste_foreground_frames(self, frames: List[Frame]):
        for frame in frames:
            for block in frame.blocks:
                # Must be foreground
                if block.type != 1: continue
                y_start = frame.position[1] + block.position[1] + self.y_offset
                x_start = frame.position[0] + block.position[0] + self.x_offset
                x_end, y_end = x_start + MACRO_SIZE, y_start + MACRO_SIZE
                self.pixels[y_start: y_end, x_start: x_end] = block.data
    
    def get_frames_around_foreground(self) -> List[List[List[List[int]]]]:
        frames = []
        for frame in self.frames:
            x_center, y_center = frame.get_frame_foreground_center()
            x_start = self.x_offset + frame.position[0] + (x_center - frame.width) // 2
            y_start = self.y_offset + frame.position[1] + (y_center - frame.height) // 2
            x_end, y_end = x_start + frame.width, y_start + frame.height
            # Currently has background
            new_frame = self.pixels[y_start: y_end, x_start: x_end]
            for block in frame.blocks:
                # Must be foreground
                if block.type != 1: continue
                block_x_start = block.position[0] + (x_center - frame.width) // 2
                block_y_start = block.position[1] + (y_center - frame.height) // 2
                block_x_end, block_y_end = block_x_start + MACRO_SIZE, block_y_start + MACRO_SIZE
                new_frame[block_y_start: block_y_end, block_x_start: block_x_end] = block.data
            frames.append(new_frame)
        return frames

    def get_background_frame_positions(self) -> List[List[List[List[int]]]]:
        frames = []
        for frame in self.frames:
            x_start = self.x_offset + frame.position[0]
            y_start = self.y_offset + frame.position[1]
            x_end, y_end = x_start + frame.width, y_start + frame.height
            new_frame = self.pixels[y_start: y_end, x_start: x_end]
            frames.append(new_frame)
        return frames
