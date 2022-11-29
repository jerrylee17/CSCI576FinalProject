import sys
from util.io import read_video, display_video, display_frame
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

    for i in range(len(input_frames) - 1):
        print(f'Processing frame {i+i}/{len(input_frames)}')
        previous_frame_data = input_frames[i].get_frame_data()
        input_frames[i+1].calculate_block_motion_vector(previous_frame_data)
        # Attempt getting motion vector with average
        input_frames[i+1].calculate_average_motion_vector()
        input_frames[i+1].set_block_visibility()

    # Intermediate step: Separate into background and foreground
    # Store background and foreground in terrains
    # Make sure background and foreground have the same dimensions
    background: Terrain = Terrain(input_frames, 0)
    foreground: List[Frame] = input_frames[1:]

    print("Displaying background")
    background_pixels = background.get_terrain()
    background_frame = Frame(-1, len(background_pixels[0]), len(background_pixels))
    background_frame.read_into_blocks(background_pixels)
    display_frame(background_frame)

    # background, foreground = get_foreground_and_background(input_frames)

    # Output step:
    # 1. Display motion trails
    # 2. Display new video around the foreground object
    # 3. Remove objects from video
    # display_motion_trails(background, foreground)
    # display_video_around_foreground(background, foreground)
    # display_video_no_objects(background)
    # print("Writing video")
    # display_video(input_frames)
    # print("Program exited successfully")

def display_motion_trails(background, foreground):
    """Display motion trails"""
    pass

def display_video_around_foreground(background, foreground):
    """Display video around foreground"""
    pass

def display_video_no_objects(background):
    """Display video with objects removed"""
    pass

def get_foreground_and_background(frames):
    """Wrapper function for getting foreground and background"""
    pass

if __name__ == '__main__':
    main()
