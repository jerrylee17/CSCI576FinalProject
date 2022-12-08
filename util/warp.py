import numpy as np
import matplotlib.pyplot as plt
import cv2

class Stitcher:
  def __init__(self,images):
    self.imags = images

  def perform(self):
    img_1 = cv2.imread(r'C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\warp\savedImage01.jpg')
    img_2 = cv2.imread(r'C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\warp\savedImage047.jpg')
    img1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()


    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m in matches:
      if (m[0].distance < 0.5 * m[1].distance):
        good.append(m)


    matches = np.asarray(good)
    print(len(matches[:, 0]))
    if (len(matches[:, 0]) >= 4):
      src = np.float32([kp1[m.queryIdx].pt for m in matches[:, 0]]).reshape(-1, 1, 2)
      dst = np.float32([kp2[m.trainIdx].pt for m in matches[:, 0]]).reshape(-1, 1, 2)
      H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    else:
      raise AssertionError('Can’t find enough keypoints.')

    dst = cv2.warpPerspective(img_1, H, ((img_1.shape[1] + img_2.shape[1]), img_2.shape[0]))  # wraped image
    dst[0:img_2.shape[0], 0:img_2.shape[1]] = img_2  # stitched image

    cv2.imwrite(r'C:\Users\12237\Desktop\CSCI576\CSCI576FinalProject\warp\output.jpg', self.trim(dst))


  def trim(self, frame):
    # crop top
    if not np.sum(frame[0]):
      return self.trim(frame[1:])
    # crop bottom
    elif not np.sum(frame[-1]):
      return self.trim(frame[:-2])
    # crop left
    elif not np.sum(frame[:, 0]):
      return self.trim(frame[:, 1:])
      # crop right
    elif not np.sum(frame[:, -1]):
      return self.trim(frame[:, :-2])
    return frame

if __name__ == '__main__':
  stitcher = Stitcher(None)

  stitcher.perform()
