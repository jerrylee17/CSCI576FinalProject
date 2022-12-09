from typing import List
import numpy as np
import cv2
import sys
from util.io import read_video
from objects.frame import Frame


def get_warped_panorama(frames: List[Frame]):
    imgs = []
    for i in range(0, len(frames), 8):
        img = frames[i].get_frame_data()
        img = img[:frames[i].height - frames[i].pad_x, :frames[i].width - frames[i].pad_y, :]
        img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
        imgs.append(img)

    stitcher = cv2.Stitcher.create(mode=0)  # 我的是OpenCV4
    (status, pano) = stitcher.stitch(imgs)
    if status != cv2.Stitcher_OK:
        print("Cannot stitch pictures, error code = %d" % status)
        sys.exit(-1)
    print("Success.")
    cv2.imshow('pano', pano)
    cv2.imwrite("pano.jpg", pano)
    cv2.waitKey(0)




if __name__ == '__main__':
    frames = read_video("/Users/lyb/Documents/Workplace/PyCharm/CSCI576FinalProject/videos/test1_480_270_404")
    get_warped_panorama(frames)