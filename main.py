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

    # Intermediate step: Separate into background and foreground
    # Store background and foreground in terrains
    # Make sure background and foreground have the same dimensions
    background: Terrain = Terrain(input_frames, 0)
    foreground: List[Terrain]

    # background, foreground = get_foreground_and_background(input_frames)

    # Output step:
    # 1. Display motion trails
    # 2. Display new video around the foreground object
    # 3. Remove objects from video
    # display_motion_trails(background, foreground)
    # display_video_around_foreground(background, foreground)
    # display_video_no_objects(background)
    print("Writing video")
    display_video(input_frames)
    print("Program exited successfully")

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
