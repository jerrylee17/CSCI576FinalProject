# import the necessary packages
import numpy as np
import cv2
import tensorflow.compat.v1 as tf
import time


class Human_Detection:
  def __init__(self) -> None:
    self.hog = cv2.HOGDescriptor()
    self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

  # frame = cv2.resize(frame, (640, 480))
  def get_human_postition(self, frame):
    # https://thedatafrog.com/en/articles/human-detection-video/
    # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # matx = np.zeros((200, 200,3))  # numpy array with width =200, height=200
    # matx[10:90,10:90] = (255,255,255)
    # cv2.imshow("Zeros matx", matx)
    frame = frame.astype(np.uint8)
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('frame', image)
    boxes, weights = self.hog.detectMultiScale(image, winStride=(1, 1))  # FinalThreshold: group people
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
      # display the detected boxes in the colour picture
      cv2.rectangle(image, (xA, yA), (xB, yB),
                    (0, 255, 0), 2)
    cv2.imshow('frame', image)

    # return boxes
    cv2.waitKey(0)

  # https: // medium.com / @ madhawavidanapathirana / real - time - human - detection - in -computer - vision - part - 2 - c7eda27115c6

#https://medium.com/@madhawavidanapathirana/real-time-human-detection-in-computer-vision-part-2-c7eda27115c6
class DetectorAPI:
  def __init__(self):
    tf.disable_v2_behavior()
    self.path_to_ckpt = r"C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\util\faster_rcnn_inception_v2_coco_2018_01_28\frozen_inference_graph.pb"
    self.detection_graph = tf.Graph()
    with self.detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    self.default_graph = self.detection_graph.as_default()
    self.sess = tf.Session(graph=self.detection_graph)

    # Definite input and output Tensors for detection_graph
    self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
    self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
    self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

  def processFrame(self, image):

    # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image, axis=0)
    # Actual detection.
    start_time = time.time()
    (boxes, scores, classes, num) = self.sess.run(
      [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
      feed_dict={self.image_tensor: image_np_expanded})
    end_time = time.time()

    print("Elapsed Time:", end_time - start_time)

    im_height, im_width, _ = image.shape
    boxes_list = [None for i in range(boxes.shape[1])]
    for i in range(boxes.shape[1]):
      boxes_list[i] = (int(boxes[0, i, 0] * im_height),
                       int(boxes[0, i, 1] * im_width),
                       int(boxes[0, i, 2] * im_height),
                       int(boxes[0, i, 3] * im_width))

    return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

  def close(self):
    self.sess.close()
    self.default_graph.close()

  def get_human_position(self,img):
    img = img.astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    boxes, scores, classes, num = self.processFrame(img)
    threshold = 0.7
    for i in range(len(boxes)):
      # Class 1 represents human
      if classes[i] == 1 and scores[i] > threshold:
        box = boxes[i]
        cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)

    cv2.imshow("preview", img)
    cv2.waitKey(0)