import cv2
import numpy as np
from typing import List

from PIL import Image

from objects.block import Block
from objects.frame import Frame
from objects.constants import MACRO_SIZE
from util.human_detection import DetectorAPI
from util.io import read_rgb_image_


class Object_Segmentation:
  def __init__(self, frame) -> None:
    self.net = cv2.dnn.readNetFromTensorflow(
      r"C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\util\dnn\frozen_inference_graph_coco.pb",
      r"C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\util\dnn\mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")
    self.img = frame.get_frame_data().astype(np.uint8)
    self.frame = frame
    self.block_coverage_threshold = 0.20# area rate of mask in the block
    self.mask_threshold = 0.15# get object from area
  def get_human_box(self):
    detector = DetectorAPI()
    human_boxs = detector.get_human_position(self.img)
    return human_boxs
  def set_moving_object_blocks(self):
    human_boxs = self.get_human_box()
    mask = self.get_frame_mask()
    self.set(mask, human_boxs)

  def set(self, mask, human_boxs):

    for block in self.frame.blocks:
      # backfround
      if self.in_boxes(human_boxs, block.position) == False:
        block.type = 0
      else:
        # cv2.imshow("img", cv2.cvtColor(block.data.astype(np.uint8), cv2.COLOR_RGB2BGR))
        # cv2.waitKey(0)
        pos = block.position
        if (self.objects_cover_block(mask[pos[1]:pos[1] + MACRO_SIZE, pos[0]: pos[0] + MACRO_SIZE]) == True):
          block.type = 1
        else:
          block.type = 0

  def objects_cover_block(self, block_in_mask):
    target = (255,255,255)
    sum = np.sum(np.array_equal(target,item) for sublist in block_in_mask for item in sublist)
    #print(f"Coverage Ratio: {sum >= (self.block_coverage_threshold * MACRO_SIZE* MACRO_SIZE)}")

    return sum >= (self.block_coverage_threshold * MACRO_SIZE* MACRO_SIZE)

  def in_boxes(self, human_boxs, position):
    for box in human_boxs:
      box = ( box[0] // MACRO_SIZE * MACRO_SIZE, box[1] // MACRO_SIZE * MACRO_SIZE, box[2] // MACRO_SIZE * MACRO_SIZE,box[3] // MACRO_SIZE * MACRO_SIZE)
      if box[0] <= position[1] <= box[2] and box[1] <= position[0] <= box[3]:
        return True
    return False

  def get_frame_mask(self):

    height, width, _ = self.img.shape
    colors = np.random.randint(0, 255, (80, 3))
    # Detect objects
    blob = cv2.dnn.blobFromImage(self.img, swapRB=True)
    self.net.setInput(blob)

    boxes, masks = self.net.forward(["detection_out_final", "detection_masks"])
    detection_count = boxes.shape[2]
    frame_mask = np.zeros((height, width, 3), np.uint8)
    for i in range(detection_count):
      box = boxes[0, 0, i]
      class_id = box[1]
      score = box[2]
      if score < 0.5:
        continue
        # Get box Coordinates
      x = int(box[3] * width)
      y = int(box[4] * height)
      x2 = int(box[5] * width)
      y2 = int(box[6] * height)

      roi = frame_mask[y: y2, x: x2]
      roi_height, roi_width, _ = roi.shape

      # Get the mask
      mask = masks[i, int(class_id)]
      mask = cv2.resize(mask, (roi_width, roi_height))
      _, mask = cv2.threshold(mask, self.mask_threshold, 255, cv2.THRESH_BINARY)
      # print(mask.shape)
      # cv2.rectangle(self.img, (x, y), (x2, y2), (255, 0, 0), 3)

      # Get mask coordinates
      contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      color = colors[int(class_id)]
      for cnt in contours:
        cv2.fillPoly(roi, [cnt], (255, 255, 255))
        # cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))
        # cv2.imshow("roi", roi)
        # cv2.waitKey(0)
    # cv2.imshow("result", frame_mask)
    # cv2.imshow("img", cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)
    # img = Image.new("RGB", (width, height))
    # for col in range(width):
    #   for row in range(height):
    #     img.putpixel((col, row), (
    #       int(frame_mask[row][col][0]),
    #       int(frame_mask[row][col][1]),
    #       int(frame_mask[row][col][2])))
    # img.show()
    # print(frame_mask.shape)
    return frame_mask

  def read_into_blocks(self, pixels: List[List[List[int]]]) -> None:
    """Read 2D array of pixels into self.blocks"""
    pixels = np.array(pixels)
    self.pad_x, self.pad_y = self.get_zero_padding_size_(self.width, self.height)
    self.width = self.width + self.pad_y
    self.height = self.height + self.pad_x
    pixels = np.pad(
      pixels,
      [(0, self.pad_x), (0, self.pad_y), (0, 0)],
      mode='constant', constant_values=0)
    split_x = [x for x in range(0, self.width, MACRO_SIZE)]
    split_y = [y for y in range(0, self.height, MACRO_SIZE)]
    for y in split_y:
      for x in split_x:
        data = pixels[y:y + MACRO_SIZE, x:x + MACRO_SIZE, ]

        block = Block(data, self.index, (x, y))
        self.blocks.append(block)

  def show(self):
    pixels = self.frame.get_frame_foreground()

    img = Image.new("RGB", (width, height))
    for col in range(width):
      for row in range(height):
        img.putpixel((col, row), (
          int(pixels[row][col][0]),
          int(pixels[row][col][1]),
          int(pixels[row][col][2])))
    img.show()

def read(file_name: str, width: int, height: int):
  with open(file_name, "rb") as f:
    content = [byte for byte in bytearray(f.read())]
    # pad_x, pad_y = get_zero_padding_size_(width, height)

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
    return np.array(image)

class Grab_Cut:
  def __init__(self, frame) -> None:
    self.img = frame.get_frame_data().astype(np.uint8)
    self.frame = frame

  def get_human_box(self):
    detector = DetectorAPI()
    human_boxs = detector.get_human_position(self.img)
    print(f"human boxs{human_boxs}")
    x1,y1,x2,y2 = human_boxs[0]
    return (y1,x1,y2,x2)

  def perform(self,rect):
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    mask = np.zeros(self.img.shape[:2], np.uint8)
    cv2.grabCut(self.img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    height = 270
    width = 480
    pixels = self.img * mask2[:,:,np.newaxis]
    img = Image.new("RGB", (width, height))
    for col in range(width):
      for row in range(height):
        img.putpixel((col, row), (
          int(pixels[row][col][0]),
          int(pixels[row][col][1]),
          int(pixels[row][col][2])))
    img.show()


if __name__ == '__main__':
  detector = DetectorAPI()
  f = r"C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\videos\test3_480_270_595\test3_480_270_595.005.rgb"
  height = 270
  width = 480
  frame = read_rgb_image_(f, 1, width,height)

  pd = Object_Segmentation(frame)
  #
  pd.set_moving_object_blocks()
  pd.show()
  #
  # gc = Grab_Cut(frame)
  # gc.perform(gc.get_human_box())

