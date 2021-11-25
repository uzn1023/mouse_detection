##!/usr/bin/env python
import copy
import io
import os
import time
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
    column = [sg.Text('Parameters', justification='center', size=(15, 1), background_color='#F7F3EC', text_color='#000')],\
             [sg.Text('Bout',size=(7,1), background_color='#F7F3EC', text_color='#000'),sg.Spin(values=('0.00', '0.25', '0.50', '1.00', '2.00'), initial_value='0.25', key='Bout')],\
             [sg.Text('Threshold',size=(7,1), background_color='#F7F3EC', text_color='#000'),sg.Spin([x*100 for x in range(100)], 500, key='Threshold')]

    layout = [    [sg.Column(column, background_color='#F7F3EC'),sg.Image(filename='', key='-graph-'), sg.Image(filename='', key='-image-')],
                  [sg.Slider(range=(0, num_frames),size=(50, 10), orientation='h', key='-slider-'),sg.Button('STOP/PLAY', size=(10, 1), font='Helvetica 14')],
                  [sg.Button('Exit', size=(10, 1), font='Helvetica 14')]]

    window = sg.Window('MouseDitection', layout, no_titlebar=False, location=(0, 0), resizable=True)

    image_elem = window['-image-']
    slider_elem = window['-slider-']
    graph_elem = window['-graph-']

    window.read(timeout=0)
    Threshold = 500
    Bout = 0.25
    def graph_renew():
        fig = plt.figure()
        fig.canvas.draw()
        fig,ax1,ax2 = csvproc.proc(csv_out,Threshold,Bout,fig)
        item = io.BytesIO()
        fig.savefig(item, format='png') 
        graph_elem.update(data=item.getvalue())
        figname = "graph_Threshold"+str(Threshold)+"_Bout"+str(Bout)+".png"
        fig.savefig(os.path.join(outdir,figname))
        fig.savefig(os.path.join(outdir,"pic.png"))
    graph_renew()

    cur_frame = 0
    play_flag = 1
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

        if event in ('STOP/PLAY', None):
            if play_flag == 1:
                play_flag = 0
            else:
                play_flag = 1
        
        if Threshold != int(values['Threshold']) or Bout != float(values['Bout']):
            Threshold = int(values['Threshold'])
            Bout = float(values['Bout'])
            graph_renew()
        
                # Write time bar on the graph
        graph = cv2.imread(os.path.join(outdir,"pic.png"))
        x = int(101 + (cur_frame / vidFile.get(cv2.CAP_PROP_FRAME_COUNT)) * (553 - 101))
        graph = cv2.line(graph,(x,58),(x,310),(0,255,0),2)
        graph = cv2.line(graph,(x,343),(x,427),(0,255,0),2)
        imgbytes_graph = cv2.imencode('.png',graph)[1].tobytes()
        graph_elem.update(data=imgbytes_graph)

        if play_flag == 0:
            continue

        #　スライダー表示を更新
        slider_elem.update(cur_frame)
        cur_frame += 1

        #　カメラ映像を圧縮して、画像表示画面'-image-'を更新する
        #frame = cv2.resize(frame,(int(frame.shape[1] / 3),int(frame.shape[0] / 3)))
        secs = cur_frame // 11
        sec = secs % 60
        mins = secs // 60
        min = mins % 60
        hr = mins //60

        timestump = str(hr) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)
        cv2.putText(frame, timestump, org=(30,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0,color=(0,0,0),thickness=2, lineType=cv2.LINE_4)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        time.sleep(0.04)
        image_elem.update(data=imgbytes)

programname = "MouseDitection"
root = tk.Tk()
root.withdraw()
fTyp = [("","*.mp4, *.avi")]
tkinter.messagebox.showinfo(programname,'Please select video file.')
movie = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = "..")
tkinter.messagebox.showinfo(programname,'Please select output folder.')
outdir = tkinter.filedialog.askdirectory(initialdir = "..")

csv_out = movieproc.proc(movie,outdir)    # mouse ditection and calclate moving -> csv file
runmovie(movie)
