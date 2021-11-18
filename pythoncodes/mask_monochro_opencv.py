#!/usr/bin/env python
import cv2
import numpy as np

img = cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m44s177.png")
h,w = img.shape[:2]

lower = np.array(0, dtype=np.uint8)
upper = np.array(30, dtype=np.uint8)
mask_mouse = cv2.inRange(img, lower, upper)

mask_cage = np.zeros((h,w),dtype=np.uint8)
x, y, r = 175, 100, 125
cv2.circle(mask_cage,center=(x,y),radius=r,color=255,thickness=-1)

mask_mouse[mask_cage == 0] = 0
mask_mouse = cv2.morphologyEx(mask_mouse,cv2.MORPH_OPEN, np.ones((2,2),np.uint8))
mask_mouse = cv2.morphologyEx(mask_mouse,cv2.MORPH_CLOSE, np.ones((2,2),np.uint8))

nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_mouse, 4)
max_idx = np.argmax(stats[1:,:], axis=0)[4] + 1
mask_mouse[labels == max_idx, ] = 255
mask_mouse[labels != max_idx, ] = 0

img_out = img
img_out[mask_mouse > 0] = 255
img_out[mask_mouse == 0] = 0

cv2.imshow("test_4_3.png", img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(r"E:\SSG_Share_1\Uezono\result\20211118\mouse_select.png",img_out)
