##!/usr/bin/env python
import copy
import io
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk

import cv2
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import csvproc
import movieproc


def runmovie(moviename):
    vidFile = cv2.VideoCapture(moviename)
    num_frames = vidFile.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vidFile.get(cv2.CAP_PROP_FPS)

    sg.theme('Black')

    layout = [    [sg.Image(filename='', key='-graph-'), sg.Image(filename='', key='-image-')],
                  [sg.Slider(range=(0, num_frames),size=(50, 10), orientation='h', key='-slider-')],
                  [sg.Button('Exit', size=(7, 1), font='Helvetica 14')]]

    window = sg.Window('MouseDitection', layout, no_titlebar=False, location=(0, 0), resizable=True)

    image_elem = window['-image-']
    slider_elem = window['-slider-']

    window.read(timeout=0)
    fig = plt.figure()
    fig.canvas.draw()
    fig,ax1,ax2 = csvproc.proc(csv_out,1000,0.25,fig)
    ax1.axvline(x=0,color="g")
    ax2.axvline(x=0,color="g")
    item = io.BytesIO()
    fig.savefig(item, format='png') 
    window['-graph-'].update(data=item.getvalue())
    
    cur_frame = 0
    while vidFile.isOpened():
        # イベントを取得
        event, values = window.read(timeout=0)

        # 「Exit」ボタン押下時の処理
        if event in ('Exit', None):
            break

        #　ビデオファイルからの読み込み
        ret, frame = vidFile.read()

        #　データが不足している場合は、ループを停止させます。
        if not ret:  # if out of data stop looping
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        #　スライダーを手動で動かした場合は、指定したフレームにジャンプします
        if int(values['-slider-']) != cur_frame-1:
            cur_frame = int(values['-slider-'])
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)

        #　スライダー表示を更新
        slider_elem.update(cur_frame)
        cur_frame += 1

        #　カメラ映像を圧縮して、画像表示画面'-image-'を更新する
        frame = cv2.resize(frame,(int(frame.shape[1] / 3),int(frame.shape[0] / 3)))
        secs = cur_frame // 30
        sec = secs % 60
        mins = secs // 60
        min = mins % 60
        hr = mins //60

        timestump = str(hr) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)
        cv2.putText(frame, timestump, org=(30,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0,color=(0,0,0),thickness=2, lineType=cv2.LINE_4)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        image_elem.update(data=imgbytes)



programname = "MouseDitection"
root = tk.Tk()
root.withdraw()
fTyp = [("","*.mp4")]
tkinter.messagebox.showinfo(programname,'Please select video file.')
movie = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = "..")
tkinter.messagebox.showinfo(programname,'Please select output folder.')
outdir = tkinter.filedialog.askdirectory(initialdir = "..")

csv_out = movieproc.proc(movie,outdir)    # mouse ditection and calclate moving -> csv file
runmovie(movie)
