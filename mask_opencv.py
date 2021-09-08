#!/usr/bin/env python
import cv2
import numpy as np

img = cv2.imread("./data/test_picture (1).png", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert BGR -> HSV

lower = np.array([60, 25, 50], dtype=np.uint8)
upper = np.array([120, 225, 225], dtype=np.uint8)

mask = cv2.inRange(hsv, lower, upper)
img_out = img
img_out[mask > 0] = (0, 0, 255)

cv2.imwrite("test.png", img_out)
