import os
import numpy as np
import cv2
import math
from scipy import ndimage


def determine_angle(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    angles = []

    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    median_angle = np.median(angles)
    return median_angle

def rotate_img(img, angle):
    return ndimage.rotate(img, angle)

def main():
    if not os.path.exists("./img/finished"):
        os.makedirs("./img/finished")
    
    files = os.listdir("./img")
    for img_filepath in files:
        if img_filepath.endswith(".png") or img_filepath.endswith(".jpg"):
            img = cv2.imread("./img/"+img_filepath)
            img_to_process = img.copy()
            angle = determine_angle(img_to_process)
            img_after = rotate_img(img, angle)
            cv2.imwrite("./img/finished/"+ img_filepath[:img_filepath.rfind('.')] +'_rotated-angle-{}.png'.format(angle), img_after)  


if __name__ == "__main__":
    main()
