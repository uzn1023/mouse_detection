##!/usr/bin/env python
import cv2
import numpy as np
import PySimpleGUI as sg


def setparam(movie):
    mc_up = 20
    x, y, r = 175, 100, 125
    vidFile = cv2.VideoCapture(movie)
    # GUI preparation
    sg.theme('Black')
    column = [sg.Text('Mouse color upper',size=(15,1), background_color='#F7F3EC', text_color='#000'),\
              sg.Slider(range=(0, 255),size=(15, 10), default_value=20, orientation='h', key='mc_up')],\
             [sg.Text('Mask center pos X',size=(15,1), background_color='#F7F3EC', text_color='#000'),\
              sg.Slider(range=(0, 320),size=(15, 10), default_value=175, orientation='h', key='x')],\
             [sg.Text('Mask center pos Y',size=(15,1), background_color='#F7F3EC', text_color='#000'),\
              sg.Slider(range=(0, 240),size=(15, 10), default_value=100, orientation='h', key='y')],\
             [sg.Text('Mask radius',size=(15,1), background_color='#F7F3EC', text_color='#000'),\
              sg.Slider(range=(0, 500),size=(15, 10), default_value=125, orientation='h', key='r')],\

    layout = [[sg.Column(column, background_color='#F7F3EC')], [sg.Image(filename='', key='frame'), sg.Image(filename='', key='image')],[sg.Button('Done', size=(10, 1), font='Helvetica 14')]]
    window = sg.Window('SelectParameter', layout, no_titlebar=False, location=(0, 0), resizable=True)
    while(1):
        event, values = window.read(timeout=0)
        mc_up = values['mc_up']
        x, y, r = int(values['x']), int(values['y']), int(values['r'])
        ret, frame = vidFile.read()
        if not ret:
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, 1)
            continue
        h,w = frame.shape[:2]
        lower = np.array(0, dtype=np.uint8)
        upper = np.array(mc_up, dtype=np.uint8)
        img = cv2.inRange(frame, lower, upper)
        mask_cage = np.zeros((h,w),dtype=np.uint8)
        #cv2.circle(img,center=(x,y),radius=r,color=255,thickness=-1)
        cv2.circle(mask_cage,center=(x,y),radius=r,color=255,thickness=-1)
        img[mask_cage == 0] = 127
        frame[mask_cage == 0] = (127, 127, 127)
        framebytes = cv2.imencode('.png', frame)[1].tobytes()
        imgbytes = cv2.imencode('.png', img)[1].tobytes()
        window['frame'].update(data=framebytes)
        window['image'].update(data=imgbytes)
        if event in ('Done', None):
            break
    return mc_up, x, y, r




