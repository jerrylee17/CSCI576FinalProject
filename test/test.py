import cv2

from util.io import read_video, display_video, read_rgb_image_, display_frame, read_jpg_image, get_video_info_from_name_
import numpy as np
from objects.frame import Frame
from PIL import Image
import copy
import time
import matplotlib.pyplot as plt
from util.human_detection import Human_Detection, DetectorAPI


def test_video():
  video = read_video("../videos/SAL_490_270_437")
  display_video(video)


def test_by_video_frame():
  f1 = "../videos/video2_240_424_383/video2_240_424_383.050.rgb"
  f2 = "../videos/video2_240_424_383/video2_240_424_383.051.rgb"
  file_name, width, height, num_frames = get_video_info_from_name_("../videos/video2_240_424_383")
  frame1 = read_rgb_image_(f1, 1, width, height)
  frame2 = read_rgb_image_(f2, 2, width, height)
  # display_frame(frame1)
  # display_frame(frame2)
  tmp = frame1.get_frame_data()

  start = time.time()
  frame2.calculate_block_motion_vector(frame1.get_frame_data())
  frame2.calculate_average_motion_vector()
  frame2.set_block_visibility()
  end = time.time()
  print("Motion Vector Computation Time:" + str(end - start))
  # /np.linalg.norm(block.vector)
  V = np.array([block.vector / np.linalg.norm(block.vector) for block in frame2.blocks])
  vX = V[:, 0]
  vY = V[:, 1]

  posX = np.array([block.position[0] for block in frame2.blocks])
  posY = np.array([block.position[1] for block in frame2.blocks])
  origin1 = np.array([posX, posY])

  x_ticks = np.arange(0, width, 32)
  y_ticks = np.arange(0, height, 16)
  plt.xticks(x_ticks)
  plt.yticks(y_ticks)
  plt.gca().invert_yaxis()

  plt.quiver(*origin1, vX, vY)
  plt.show()

  pixels = frame2.get_frame_foreground()
  img = Image.new("RGB", (width, height))
  for col in range(width):
    for row in range(height):
      img.putpixel((col, row), (
        int(pixels[row][col][0]),
        int(pixels[row][col][1]),
        int(pixels[row][col][2])))
  img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
  cv2.imshow('image', img)
  cv2.waitKey(0)


def test_by_video_frame_with_vector_on_image():
  path = "../videos"
  name = "/video3_240_424_193"
  f1 = ".090.rgb"
  f2 = ".091.rgb"
  file_name, width, height, num_frames = get_video_info_from_name_(path+name)
  frame1 = read_rgb_image_(path +name +name+f1, 1, width, height)
  frame2 = read_rgb_image_(path +name +name+f2, 2, width, height)
  display_frame(frame1)
  display_frame(frame2)
  tmp = frame1.get_frame_data()

  start = time.time()
  frame2.calculate_block_motion_vector(frame1.get_frame_data())
  frame2.calculate_average_motion_vector()
  frame2.set_block_visibility()
  end = time.time()
  print("Motion Vector Computation Time:" + str(end - start))
  # /np.linalg.norm(block.vector)

  pixels = frame2.get_frame_foreground()
  img = Image.new("RGB", (width, height))
  for col in range(width):
    for row in range(height):
      img.putpixel((col, row), (
        int(pixels[row][col][0]),
        int(pixels[row][col][1]),
        int(pixels[row][col][2])))
  img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

  for block in frame2.blocks:
    img = cv2.arrowedLine(img, block.position,
                          (block.position[0] + block.vector[0], block.position[1] + block.vector[1]), (0, 0, 255), 1,
                          tipLength=0.5)
  cv2.imshow('image', img)
  cv2.waitKey(0)


def test_by_reference_frame(width, height, f1, f2):
  frame1 = read_jpg_image(f1, 1, width, height)
  frame2 = read_jpg_image(f2, 2, width, height)
  # display_frame(frame1)
  # display_frame(frame2)
  tmp = frame1.get_frame_data()
  start = time.time()
  frame2.calculate_block_motion_vector(frame1.get_frame_data())
  end = time.time()
  print("Motion Vector Computation Time:" + str(end - start))
  V = np.array([block.vector for block in frame2.blocks])
  vX = V[:, 0]
  vY = -V[:, 1]

  posX = np.array([block.position[0] for block in frame2.blocks])
  posY = np.array([block.position[1] for block in frame2.blocks])
  origin1 = np.array([posX, posY])

  x_ticks = np.arange(0, width, 32)
  y_ticks = np.arange(0, height, 16)
  plt.xticks(x_ticks)
  plt.yticks(y_ticks)
  plt.gca().invert_yaxis()

  plt.quiver(*origin1, vX, vY)
  plt.show()
  frame2.calculate_mode_motion_vector()
  print("Frame vector: " + str(frame2.vector))


def test_by_block():
  width = 320
  height = 160

  frame1 = Frame(1, width, height)
  frame2 = Frame(2, width, height)
  frame1.read_into_blocks(set_block_in_frame(create_empty_frame(width, height), 16, 16, (255, 233, 0)))
  frame2.read_into_blocks(set_block_in_frame(create_empty_frame(width, height), 0, 0, (255, 233, 0)))
  display_frame(frame1)
  display_frame(frame2)
  tmp = frame1.get_frame_data()
  frame2.calculate_block_motion_vector(frame1.get_frame_data())
  V = np.array([block.vector / np.linalg.norm(block.vector) for block in frame2.blocks])
  vX = V[:, 0]
  vY = -V[:, 1]

  posX = np.array([block.position[0] for block in frame2.blocks])
  posY = np.array([block.position[1] for block in frame2.blocks])
  origin1 = np.array([posX, posY])
  x_ticks = np.arange(0, width, 16)
  y_ticks = np.arange(0, height, 16)
  plt.xticks(x_ticks)
  plt.yticks(y_ticks)
  plt.gca().invert_yaxis()
  plt.quiver(*origin1, vX, vY)

  plt.show()


def create_empty_frame(w, h):
  rgbArray = np.zeros((h, w, 3), 'uint8')
  # rgbArray[..., 0] =  np.random.randint(low = 0, high=255, size=(100,100))
  # rgbArray[..., 1] = np.random.randint(low = 0, high=255, size=(100,100))
  # rgbArray[..., 2] = np.random.randint(low = 0, high=255, size=(100,100))
  rgbArray[..., 0] = 0
  rgbArray[..., 1] = 0
  rgbArray[..., 2] = 0

  return rgbArray


def set_block_in_frame(frame, x, y, color):
  block_size = 20

  frame[x:x + block_size, y:y + block_size] = color

  return frame


def read_jpg():
  width = 960
  height = 540
  frame1 = read_jpg_image("../videos/test/reference.jpg", 1, width, height)
  display_frame(frame1)


def human_detection():
  width = 240
  height = 424

  file = "../videos/video2_240_424_383/video2_240_424_383.001.rgb"
  frame = read_rgb_image_(file, 1, width, height)
  display_frame(frame)

  image = np.array(frame.get_frame_data())
  # #HOGDescriptor
  # # HD = Human_Detection()
  # # HD.get_human_postition(image)
  # #
  detector = DetectorAPI()
  detector.get_human_position(image)


def frame_block_detection():
  detector = DetectorAPI()
  width = 240
  height = 424
  f1 = "../videos/video3_240_424_193/video3_240_424_193.074.rgb"
  f2 = "../videos/video3_240_424_193/video3_240_424_193.075.rgb"
  # frame1 = read_rgb_image_(f1, 1, width, height)
  frame2 = read_rgb_image_(f2, 2, width, height)
  # display_frame(frame1)
  # display_frame(frame2)
  # frame2.calculate_block_motion_vector(frame1.get_frame_data())
  # frame2.calculate_average_motion_vector()
  # frame2.set_block_visibility()
  frame2.human_detection(detector)
  pixels = frame2.get_frame_foreground()
  img = Image.new("RGB", (width, height))
  for col in range(width):
    for row in range(height):
      img.putpixel((col, row), (
        int(pixels[row][col][0]),
        int(pixels[row][col][1]),
        int(pixels[row][col][2])))
  img.show()


if __name__ == '__main__':
  # f1 = "../videos/test/imageonline-co-pixelated.png"
  # f2 = "../videos/test/imageonline-co-pixelated2.png"
  # test_by_reference_frame(512,512,f1,f2)
  test_by_video_frame_with_vector_on_image()
