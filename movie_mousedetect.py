##!/usr/bin/env python
import csv

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tqdm

cap = cv2.VideoCapture("./data/video/general_long.mp4")

divider = 1
frame_rate = 30.0 / divider
size = (1280, 960)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') 
writer = cv2.VideoWriter('./result/20211021/general_long.mp4', fmt, frame_rate, size) 
f = open("./result/20211021/general_long.csv","w")
writer_csv = csv.writer(f,lineterminator="\n")
writer_csv.writerow(["time[s]","amount of movement[px]"])
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

def img_proc(pic):
    bin_out = np.zeros((pic.shape[0],pic.shape[1]),np.uint8)
    hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)  # Convert BGR -> HSV
    
    lower_mouse = np.array([0, 0, 0], dtype=np.uint8)
    upper_mouse = np.array([255, 255, 30], dtype=np.uint8)

    lower_cable = np.array([80, 20, 20], dtype=np.uint8)
    upper_cable = np.array([140, 255, 255], dtype=np.uint8)

    mask_mouse = cv2.inRange(hsv, lower_mouse, upper_mouse)
    mask_mouse = cv2.morphologyEx(mask_mouse,cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    mask_cable = cv2.inRange(hsv, lower_cable, upper_cable)
    mask_cable = cv2.morphologyEx(mask_cable,cv2.MORPH_OPEN, np.ones((5,5),np.uint8))

    mask_mouse_inv = cv2.bitwise_not(mask_mouse)
    dst = cv2.distanceTransform(mask_mouse_inv,cv2.DIST_L2,maskSize=5)

    bin_dst = cv2.inRange(dst,0,20)
    mask_cable_mouse = cv2.bitwise_and(mask_cable,bin_dst)
    mask_mouse_fix = cv2.bitwise_or(mask_mouse,mask_cable_mouse)
    mask_mouse_fix = cv2.morphologyEx(mask_mouse_fix,cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    mask_mouse_fix = cv2.morphologyEx(mask_mouse_fix,cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_mouse_fix, 4)
    max_idx = np.argmax(stats[1:,:], axis=0)[4] + 1
    img_out = pic
    img_out[labels == max_idx, ] = (0, 0, 255)
    bin_out[labels == max_idx, ] = 255
    return bin_out,img_out

for i in tqdm.tqdm(range(frame_count)):
#for i in tqdm.tqdm(range(1800)):
    ret, frame = cap.read()
    bin_mouse, img_out = img_proc(frame)
    
    if (i > 0) and (i % divider == 0):
        img_xor = cv2.bitwise_xor(bin_mouse,bin_mouse_old)
        img_out[img_xor != 0] = (0, 255, 0)
        cnt = cv2.countNonZero(img_xor)
        writer_csv.writerow([str(i/30),cnt])

        if cnt >= 300:
            state = "Moving"
            color_state = (255,0,0)
        else:
            state = "Stopping"
            color_state = (0,255,0)

        cv2.putText(img_out, state, org=(100,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=color_state, thickness=3, lineType=cv2.LINE_4)
        txts = []
        txts.append("Time[s] = " + str(round(i/30,2)))
        txts.append("Move[px] = " + str(cnt))
        for j in range(len(txts)):
            cv2.putText(img_out, txts[j], org=(100,100+50*j), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(0,0,0), thickness=2, lineType=cv2.LINE_4)
        
        writer.write(img_out)
    if i % divider == 0:
        bin_mouse_old = bin_mouse
   
writer.release()
cap.release()
cv2.destroyAllWindows()
f.close()
