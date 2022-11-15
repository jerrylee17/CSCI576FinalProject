from PIL import Image, ImageTk
from objects.frame import Frame
from typing import List
import tkinter


def read_rgb_image(file_name: str, width: int, height: int) -> List[List[List[int]]]:
    """Read a single frame."""
    file = open(file_name, "rb")
    content = [byte for byte in bytearray(file.read())]

    image = []
    idx = 0
    for _ in range(height):
        col_list = []
        for _ in range(width):
            # Separate R, G, and B values
            rgb_list = [content[3 * idx] & 0xff, content[3 * idx + 1] & 0xff, content[3 * idx + 2] & 0xff]
            col_list.append(rgb_list)
            idx += 1
        image.append(col_list)

    return image


def get_video_info_from_name(file_path: str) -> dict:
    """Obtain frame number, width, and height from name."""
    split_path = file_path.split("/")
    file_name = split_path[-2] if len(split_path[-1]) == 0 else split_path[-1]
    split_name = file_name.split("_")
    return {
        "name": split_name[0],
        "width": int(split_name[1]),
        "height": int(split_name[2]),
        "frame_number": int(split_name[3])
    }


def read_video(file_path: str) -> List[Frame]:
    """Read videos into frames."""
    frames = []
    info = get_video_info_from_name(file_path)
    for i in range(1, info["frame_number"] + 1):
        image_name = file_path + info["name"] + "_" + str(info["width"]) + "_" + str(info["height"]) + "_" \
                     + str(info["frame_number"]) + "." + str(i).zfill(3) + ".rgb"
        image = read_rgb_image(image_name, info["width"], info["height"])
        frame = Frame(i, info["width"], info["height"])
        frame.read_into_blocks(image)
        frames.append(frame)
    return frames


# def read_video(file_path: str) -> List[List[List[List[int]]]]:
#     """Read videos into frames."""
#     frames = []
#     info = get_video_info_from_name(file_path)
#     for i in range(1, info["frame_number"] + 1):
#         image_name = file_path + info["name"] + "_" + str(info["width"]) + "_" + str(info["height"]) + "_" \
#                      + str(info["frame_number"]) + "." + str(i).zfill(3) + ".rgb"
#         image = read_rgb_image(image_name, info["width"], info["height"])
#         frames.append(image)
#     return frames


def display_video(frames: List[Frame]):
    """Displays video."""
    pass


def display_frame(frame: Frame):
# def display_frame(frame: Frame, pixels: List[List[List[int]]]):
    """Displays a given frame."""
    img = Image.new("RGB", (frame.width, frame.height))
    pixels = frame.get_frame_data()
    for col in range(frame.width):
        for row in range(frame.height):
            img.putpixel((col, row), (pixels[row][col][0], pixels[row][col][1], pixels[row][col][2]))
    img.show()


def test_image():
    # print(os.getcwd())
    image = (read_rgb_image("../videos/SAL_490_270_40/SAL_490_270_40.001.rgb", 490, 270))
    frame = Frame(1, 490, 270)
    # frame.read_into_blocks(image)
    display_frame(frame, image)


# if __name__ == '__main__':
#     test_image()
