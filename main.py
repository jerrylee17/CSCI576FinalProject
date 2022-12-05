import sys
from util.io import read_video, display_video, display_frame, display_video_foreground
from util.background import generate_background
from objects.frame import Frame, test_read_into_blocks
from objects.terrain import Terrain
from typing import List

def main():
    input_video_path = sys.argv[1]
    # Read input into list of frames
    print("Reading video")
    input_frames: List[Frame] = read_video(input_video_path)

    print("Calculating motion vectors")
    # Calculate the first frame
    # previous_frame_data = input_frames[1].get_frame_data()
    # input_frames[0].calculate_block_motion_vector(previous_frame_data)
    # input_frames[0].calculate_average_motion_vector()
    # input_frames[0].set_block_visibility()
    input_frames[0].position = (0, 0)

    for i in range(len(input_frames) - 1):
        print(f'Processing frame {i+1}/{len(input_frames)}')
        previous_frame_data = input_frames[i].get_frame_data()
        input_frames[i+1].calculate_block_motion_vector(previous_frame_data)
        # Attempt getting motion vector with average
        input_frames[i+1].calculate_average_motion_vector()
        input_frames[i+1].set_block_visibility()
        input_frames[i+1].calculate_frame_position(input_frames[i])

    # Intermediate step: Separate into background and foreground
    # Store background and foreground in terrains
    # Make sure background and foreground have the same dimensions
    background: Terrain = Terrain(input_frames, 0)
    foreground: List[Frame] = input_frames[1:]

    print("Displaying background")
    background_pixels = background.get_terrain()
    background_frame = Frame(-1, len(background_pixels[0]), len(background_pixels))
    background_frame.read_into_blocks(background_pixels)
    display_frame(input_frames[0])
    display_frame(background_frame)
    print("Displaying foreground")
    display_video_foreground(foreground)

    # background, foreground = get_foreground_and_background(input_frames)

    # Output step:
    # 1. Display motion trails
    # 2. Display new video around the foreground object
    # 3. Remove objects from video

    # video_no_objects = display_video_no_objects(background)
    # video_around_foreground = display_video_around_foreground(background)
    # composite_trial = composite_trial(background, foreground)


# Do this last
def composite_trial(background: Terrain, frames: List[Frame]):
    background.paste_foreground_frames(frames[::50])
    return background

def display_video_around_foreground(background: Terrain):
    """Display video around foreground"""
    return background.get_frames_around_foreground()

def display_video_no_objects(background: Terrain):
    """Display video with objects removed"""
    return background.get_background_frame_positions()

if __name__ == '__main__':
    main()
