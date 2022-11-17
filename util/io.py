from PIL import Image
from objects.frame import Frame
from typing import List
from objects.constants import FPS, MACRO_SIZE
from os import listdir
import cv2
import numpy as np


def get_zero_padding_size(width: int, height: int):
    """Calculate the cols and rows of zeros that need to be padded."""
    zero_padding_cols = MACRO_SIZE - (width % MACRO_SIZE)
    if zero_padding_cols == MACRO_SIZE:
        zero_padding_cols = 0

    zero_padding_rows = MACRO_SIZE - (height % MACRO_SIZE)
    if zero_padding_rows == MACRO_SIZE:
        zero_padding_rows = 0

    return zero_padding_rows, zero_padding_cols


def read_rgb_image(file_name: str, index, width: int, height: int) -> Frame:
    """Read a single frame."""
    with open(file_name, "rb") as f:
        content = [byte for byte in bytearray(f.read())]
        pad_x, pad_y = get_zero_padding_size(width, height)

        image = []
        idx = 0
        for col in range(height):
            col_list = []
            for row in range(width):
                # Separate R, G, and B values
                rgb_list = [content[3 * idx] & 0xff, content[3 * idx + 1] & 0xff, content[3 * idx + 2] & 0xff]
                col_list.append(rgb_list)
                idx += 1

            image.append(col_list)
        image = np.array(image)
        image = np.pad(
            image, 
            [(0, pad_x), (0, pad_y), (0, 0)],
            mode='constant', constant_values=0)
        frame = Frame(index, width + pad_y, height + pad_x)
        frame.read_into_blocks(image)
        test = frame.get_frame_data()
        return frame


def display_frame(frame: Frame):
    """Displays a given frame."""
    img = Image.new("RGB", (frame.width, frame.height))
    pixels = frame.get_frame_data()  # Command this line when test
    for col in range(frame.width):
        for row in range(frame.height):
            # print(len(pixels), len(pixels[0]))
            img.putpixel((col, row), (pixels[row][col][0], pixels[row][col][1], pixels[row][col][2]))
    img.show()


def get_video_info_from_name(file_path: str) -> dict:
    """Obtain frame number, width, and height from name.
    Returns:
        file_name
        width
        height
        number of frames
    """
    file_name = file_path.split('/')[-1]
    _, width, height, num_frames = file_name.split('_')

    return [
        file_name,
        int(width),
        int(height),
        int(num_frames)
    ]


def read_video(file_path: str) -> List[Frame]:
    """Read videos into frames."""
    frames = []
    file_name, width, height, num_frames = get_video_info_from_name(file_path)
    # Using listdir rather than num frames
    file_names = listdir(file_path)
    for index, file_name in enumerate(file_names):
        image_name = f"{file_path}/{file_name}"
        image = read_rgb_image(image_name, index, width, height)
        frames.append(image)
        break
    return frames


def play_video(fps: int):
    """Play the generated video."""
    delay = round(1000 / fps)
    cap = cv2.VideoCapture('../output/test/mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('CSCI 576 Project', frame)
            # & 0xFF is required for a 64-bit system
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def display_video(frames: List[Frame]):
    """Generate resultant video, and play it by calling play_video."""
    video_dims = (frames[0].width, frames[0].height)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter("../output/test/mp4", fourcc, FPS, video_dims)
    img = Image.new('RGB', video_dims, color='darkred')
    for i in range(len(frames)):
        frame = frames[i].get_frame_data()
        for col in range(frames[0].width):
            for row in range(frames[0].height):
                img.putpixel((col, row), (frame[row][col][0], frame[row][col][1], frame[row][col][2]))

        frame_cvt = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        video.write(frame_cvt)

        # cv2.imshow('CSCI 576 Project', frame_cvt) # Display video on the fly
        # cv2.waitKey(1)                            # Display video on the fly

    video.release()
    # Display video after generation
    play_video(FPS)

