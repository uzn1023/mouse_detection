#!/usr/bin/env python
import cv2
import matplotlib.pyplot as plt
import numpy as np

img1 = cv2.imread(r"C:\Users\SSG_Share_1\Uezono\data\scene2\s00121.png", cv2.IMREAD_COLOR)
img2 = cv2.imread(r"C:\Users\SSG_Share_1\Uezono\data\scene2\s00151.png", cv2.IMREAD_COLOR)

imgs = [img1,img2]

for i in range(len(imgs)):
    imgs[i] = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2GRAY)
    imgs[i] = imgs[i] // 70
    imgs[i] = imgs[i] * 70

bitwise_xor = cv2.bitwise_xor(imgs[0],imgs[1])

plt.imshow(bitwise_xor, cmap = "gray")
plt.show()

threshold = 0
th, binaly = cv2.threshold(bitwise_xor, threshold, 255, cv2.THRESH_BINARY)

plt.imshow(binaly, cmap = "gray")
plt.show()

cv2.imwrite("./result/20210921/xor_121_151_2.png", binaly)
cv2.imwrite("./result/20210921/xor_121_151_2_b.png", binaly)
