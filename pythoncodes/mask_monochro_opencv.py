#!/usr/bin/env python
import cv2
import numpy as np

imgs = []
imgs.append(cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m44s177.png"))
imgs.append(cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m46s772.png"))
imgs.append(cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m49s402.png"))
imgs.append(cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m50s537.png"))
imgs.append(cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m51s707.png"))
imgs.append(cv2.imread(r"E:\SSG_Share_1\Uezono\data\scene3\mouse_2021-11-18-15h48m52s927.png"))

for i in range(len(imgs)):
    img = imgs[i]
    h,w = img.shape[:2]
    # Mask for mouse (black region)
    lower = np.array(0, dtype=np.uint8)
    upper = np.array(35, dtype=np.uint8)
    mask_mouse = cv2.inRange(img, lower, upper)
    # Mask for cable (white region) 
    lower = np.array(230, dtype=np.uint8)
    upper = np.array(255, dtype=np.uint8)
    mask_cable = cv2.inRange(img, lower, upper)
    # Mask for inCage region
    mask_cage = np.zeros((h,w),dtype=np.uint8)
    x, y, r = 175, 100, 125
    cv2.circle(mask_cage,center=(x,y),radius=r,color=255,thickness=-1)

    mask_mouse[mask_cage == 0] = 0  # Exclude out of cage
    # Morphorogy precessing
    mask_mouse = cv2.morphologyEx(mask_mouse,cv2.MORPH_OPEN, np.ones((2,2),np.uint8))
    mask_mouse = cv2.morphologyEx(mask_mouse,cv2.MORPH_CLOSE, np.ones((2,2),np.uint8))
    mask_mouse = cv2.dilate(mask_mouse,np.ones((5,5),np.uint8),iterations = 1)  # 胴体と体の分離、ケーブルによるマウス領域の分離を防ぐ

    # Selecting most biggest region (should be mouse region)
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_mouse, 4)
    max_idx = np.argmax(stats[1:,:], axis=0)[4] + 1
    mask_mouse[labels == max_idx, ] = 255
    mask_mouse[labels != max_idx, ] = 0
    mask_mouse = cv2.erode(mask_mouse,np.ones((5,5),np.uint8),iterations = 1)   # Recovering from dilate

    # Taking difference of mouse region
    if i > 0:
        xor = cv2.bitwise_xor(mask_mouse,mask_mouse_old)
        xor[(mask_cable != 0) | (mask_cable_old != 0)] = 0  # ケーブルがマウスの上を動いたことがマウスの動きと判定されるのを防ぐ
        cv2.imshow("test_4_3.png", xor)
        cv2.waitKey(0)
    mask_mouse_old = mask_mouse
    mask_cable_old = mask_cable
    cv2.destroyAllWindows()
   
    

    #cv2.imwrite(r"E:\SSG_Share_1\Uezono\result\20211118\mouse_select.png",img_out)
