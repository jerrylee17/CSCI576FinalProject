import sys
from util.io import read_video, display_video, display_frame, display_video_foreground,save_video_background
from util.human_detection import DetectorAPI
from util.background import generate_background
from objects.frame import Frame, test_read_into_blocks
from objects.terrain import Terrain
from typing import List
from copy import deepcopy

from util.object_segmentation import Object_Segmentation


def main():
    input_video_path = sys.argv[1]
    # Read input into list of frames
    print("Reading video")
    input_frames: List[Frame] = read_video(input_video_path)

    print("Calculating motion vectors")
    detector = DetectorAPI()

    # Calculate the first frame
    # previous_frame_data = input_frames[1].get_frame_data()
    # input_frames[0].calculate_block_motion_vector(previous_frame_data)
    # input_frames[0].calculate_average_motion_vector()
    # input_frames[0].set_block_visibility()
    input_frames[0].position = (0, 0)

    for i in range(len(input_frames) - 1):
        print(f'Processing frame {i+1}/{len(input_frames)}')
        #previous_frame_data = input_frames[i].get_frame_data()
        #input_frames[i+1].calculate_block_motion_vector(previous_frame_data)
        # Attempt getting motion vector with average
        #input_frames[i+1].calculate_mode_motion_vector()
        #input_frames[i+1].set_block_visibility()
        #input_frames[i+1].remove_individual_foreground_block()
        #input_frames[i + 1].human_detection(detector)
        #input_frames[i+1].calculate_frame_position(input_frames[i])
        pd = Object_Segmentation(input_frames[i+1])
        pd.set_moving_object_blocks()
        save_video_background(input_frames[i+1])
    foreground: List[Frame] = input_frames[1:]
    display_video_foreground(foreground)
    save_video_background(input_frames[1:])
    # Intermediate step: Separate into background and foreground
    # Store background and foreground in terrains
    # Make sure background and foreground have the same dimensions

    # background: Terrain = Terrain(input_frames[1:], 0)
    #
    # print("Displaying background")
    # background_pixels = background.get_terrain()
    # background_frame = Frame(-1, len(background_pixels[0]), len(background_pixels))
    # background_frame.read_into_blocks(background_pixels)
    # # display_frame(input_frames[0])
    # display_frame(background_frame)
    # print("Displaying foreground")
    # display_video_foreground(foreground)

    # background, foreground = get_foreground_and_background(input_frames)

    # Output step:
    # 1. Display motion trails
    # 2. Display new video around the foreground object
    # 3. Remove objects from video

    # print("Displaying composite trail")
    # composite_trail = get_composite_trail(background, foreground)
    # display_frame_from_pixels(composite_trail)
    #
    # print("Displaying video no objects")
    # video_no_objects = get_display_video_no_objects(background)
    # display_video_from_pixels(video_no_objects)
    #
    # print("Displaying video around foreground")
    # video_around_foreground = get_display_video_around_foreground(background)
    # display_video_from_pixels(video_around_foreground)
    # detector.close()

def display_frame_from_pixels(pixels: List[List[List[int]]]):
    frame = Frame(-1, len(pixels[0]), len(pixels))
    frame.read_into_blocks(pixels)
    display_frame(frame)

def display_video_from_pixels(pixels: List[List[List[List[int]]]]):
    frames = []
    for i, frame_pixels in enumerate(pixels):
        frame = Frame(i, len(frame_pixels[0]), len(frame_pixels))
        frame.read_into_blocks(frame)
        frames.append(frame)
    display_video(frames)

def get_composite_trail(background: Terrain, frames: List[Frame]):
    trail = deepcopy(background)
    trail.paste_foreground_frames(frames[::10])
    trail_pixels = trail.get_terrain()
    return trail_pixels

def get_display_video_around_foreground(background: Terrain) -> List[List[List[List[int]]]]:
    """Display video around foreground"""
    return background.get_frames_around_foreground()

def get_display_video_no_objects(background: Terrain) -> List[List[List[List[int]]]]:
    """Display video with objects removed"""
    return background.get_background_frame_positions()

if __name__ == '__main__':
    main()
