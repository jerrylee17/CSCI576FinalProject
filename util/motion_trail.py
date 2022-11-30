import copy
from typing import List
from objects.foreground import Foreground
from objects.frame import Frame
from objects.terrain import Terrain


# def composite_trail(background: Terrain, foreground: List[Foreground]) -> List[List[List[int]]]:
#     trail = copy.deepcopy(background.pixels)
#     for frame_idx in range(0, len(foreground), 50):
#         frame_offset_x = background.frame_offsets[frame_idx][0]
#         frame_offset_y = background.frame_offsets[frame_idx][1]
#         for x_idx in range(len(foreground[frame_idx].pixels)):
#             for y_idx, pixel in enumerate(foreground[frame_idx].pixels[x_idx]):
#                 pixel_idx_x = frame_offset_x + x_idx
#                 pixel_iex_y = frame_offset_y + y_idx
#                 if foreground[frame_idx].is_foreground[x_idx][y_idx]:
#                     trail[pixel_idx_x][pixel_iex_y] = pixel
#     return trail


def composite_trial(background: Terrain, frames: List[Frame]):
    background.paste_foreground_frames(frames[::50])


