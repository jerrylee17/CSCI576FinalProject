from PIL import Image
from objects.frame import Frame
from typing import List
from objects.constants import FPS
import cv2
import numpy


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


def display_frame(frame: Frame):
# def display_frame(frame: Frame, pixels: List[List[List[int]]]):
    """Displays a given frame."""
    img = Image.new("RGB", (frame.width, frame.height))
    pixels = frame.get_frame_data()  # Command this line when test
    for col in range(frame.width):
        for row in range(frame.height):
            img.putpixel((col, row), (pixels[row][col][0], pixels[row][col][1], pixels[row][col][2]))
    img.show()


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


# def read_video(file_path: str) -> List[Frame]:
#     """Read videos into frames."""
#     frames = []
#     info = get_video_info_from_name(file_path)
#     for i in range(1, info["frame_number"] + 1):
#         image_name = file_path + info["name"] + "_" + str(info["width"]) + "_" + str(info["height"]) + "_" \
#                      + str(info["frame_number"]) + "." + str(i).zfill(3) + ".rgb"
#         image = read_rgb_image(image_name, info["width"], info["height"])
#         frame = Frame(i, info["width"], info["height"])
#         frame.read_into_blocks(image)
#         frames.append(frame)
#     return frames


def read_video(file_path: str) -> List[List[List[List[int]]]]:
    """Read videos into frames."""
    frames = []
    info = get_video_info_from_name(file_path)
    for i in range(1, info["frame_number"] + 1):
        image_name = file_path + info["name"] + "_" + str(info["width"]) + "_" + str(info["height"]) + "_" \
                     + str(info["frame_number"]) + "." + str(i).zfill(3) + ".rgb"
        image = read_rgb_image(image_name, info["width"], info["height"])
        frames.append(image)
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

        frame_cvt = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
        video.write(frame_cvt)

        # cv2.imshow('CSCI 576 Project', frame_cvt) # Display video on the fly
        # cv2.waitKey(1)                            # Display video on the fly

    video.release()
    # Display video after generation
    play_video(FPS)

# def display_video(frames: List[List[List[List[int]]]]):
#     """Generate resultant video, and play it by calling play_video."""
#     video_dims = (490, 270)
#     fourcc = cv2.VideoWriter_fourcc(*'avc1')
#     video = cv2.VideoWriter("test.mp4", fourcc, FPS, video_dims)
#     img = Image.new('RGB', video_dims, color='darkred')
#     for i in range(len(frames)):
#         for col in range(490):
#             for row in range(270):
#                 img.putpixel((col, row), (frames[i][row][col][0], frames[i][row][col][1], frames[i][row][col][2]))
#
#         frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
#         video.write(frame)
#
#         # cv2.imshow('frame', frame) # Display video on the fly
#         # cv2.waitKey(1)             # Display video on the fly
#
#     video.release()
#     play_video(FPS)


def test_image():
    # print(os.getcwd())
    image = (read_rgb_image("../videos/Stairs_490_270_346/Stairs_490_270_346.001.rgb", 490, 270))
    frame = Frame(1, 490, 270)
    # frame.read_into_blocks(image)
    display_frame(frame, image)


def test_video():
    video = read_video("../videos/Stairs_490_270_346/")
    display_video(video)


# if __name__ == '__main__':
    # test_image()
    # test_video()
