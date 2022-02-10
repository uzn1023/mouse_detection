##!/usr/bin/env python
import cv2
import numpy as np
import PySimpleGUI as sg


def setparam(movie):
    mc_up = 20
    X, Y, W, H = 175, 100, 250, 250
    vidFile = cv2.VideoCapture(movie)
    # GUI preparation
    sg.theme('Black')
    txt_mcu = sg.Text('Mouse color upper',size=(15,1), background_color='#F7F3EC', text_color='#000')
    sld_mcu = sg.Slider(range=(0, 255),size=(15, 10), default_value=mc_up, orientation='h', key='mc_up')
    txt_mcx = sg.Text('Mask center: pos X',size=(15,1), background_color='#F7F3EC', text_color='#000')
    sld_mcx = sg.Slider(range=(0, 320),size=(15, 10), default_value=X, orientation='h', key='x')
    txt_mcy = sg.Text('pos Y',size=(15,1), background_color='#F7F3EC', text_color='#000')
    sld_mcy = sg.Slider(range=(0, 240),size=(15, 10), default_value=Y, orientation='h', key='y')
    txt_mw = sg.Text('Mask width',size=(15,1), background_color='#F7F3EC', text_color='#000')
    sld_mw = sg.Slider(range=(0, 500),size=(15, 10), default_value=W, orientation='h', key='w')
    txt_mh = sg.Text('Mask height',size=(15,1), background_color='#F7F3EC', text_color='#000')
    sld_mh = sg.Slider(range=(0, 500),size=(15, 10), default_value=H, orientation='h', key='h')
    txt_ms = sg.Text('Mask shape',size=(15,1), background_color='#F7F3EC', text_color='#000')
    rad_cir = sg.Radio("Circle", size=(10, 1), group_id = "shape", key="cir", default=True)
    rad_rec = sg.Radio("Rectangle", size=(10, 1), group_id = "shape", key="rec")

    column = [txt_mcu, sld_mcu],\
             [txt_mcx, sld_mcx, txt_mcy,sld_mcy],\
             [txt_mw, sld_mw, txt_mh, sld_mh],\
             [txt_ms, rad_cir, rad_rec]

    layout = [[sg.Column(column, background_color='#F7F3EC')], [sg.Image(filename='', key='frame'), sg.Image(filename='', key='image')],[sg.Button('Done', size=(10, 1), font='Helvetica 14')]]
    window = sg.Window('SelectParameter', layout, no_titlebar=False, location=(0, 0), resizable=True)
    while(1):
        event, values = window.read(timeout=0)
        mc_up = values['mc_up']
        X, Y, W, H = int(values['x']), int(values['y']), int(values["w"]), int(values["h"])
        ret, frame = vidFile.read()
        if not ret:
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, 1)
            continue
        h,w = frame.shape[:2]
        lower = np.array(0, dtype=np.uint8)
        upper = np.array(mc_up, dtype=np.uint8)
        img = cv2.inRange(frame, lower, upper)
        mask_cage = np.zeros((h,w),dtype=np.uint8)
        if values["cir"] == True:
            center = (X,Y)
            axes = (W,H)
            box = (center, axes, 0)
            cv2.ellipse(mask_cage,box=box, color=255,thickness=-1)
            shape = "cir"
        else:
            pt1 = (int(X-W/2), int(Y-H/2))
            pt2 = (int(X+W/2), int(Y+H/2))
            cv2.rectangle(mask_cage, pt1=pt1, pt2=pt2, color=255, thickness=-1)
            shape = "rec"
        img[mask_cage == 0] = 127
        frame[mask_cage == 0] = (127, 127, 127)
        framebytes = cv2.imencode('.png', frame)[1].tobytes()
        imgbytes = cv2.imencode('.png', img)[1].tobytes()
        window['frame'].update(data=framebytes)
        window['image'].update(data=imgbytes)
        if event in ('Done', None):
            window.close()
            break
        param = [mc_up, X, Y, W, H, shape]
    return param
if __name__ == '__main__':
    setparam(r"E:\SSG_Share_1\Uezono\data\monochro\nV54_ptskC_Video.avi")




