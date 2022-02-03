##!/usr/bin/env python
import copy
import io
import os
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
import pandas as pd

import cv2
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import csvproc
import movieproc
import setparam

def runmovie(moviename,moviemask,outdir):
    vidFile = cv2.VideoCapture(moviename)
    num_frames = vidFile.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vidFile.get(cv2.CAP_PROP_FPS)

    vidFile2 = cv2.VideoCapture(moviemask)
    num_frames2 = vidFile2.get(cv2.CAP_PROP_FRAME_COUNT)
    fps2 = vidFile2.get(cv2.CAP_PROP_FPS)

    sg.theme('Black')
    column = [sg.Text('Parameters', justification='center', size=(15, 1), background_color='#F7F3EC', text_color='#000')],\
             [sg.Text('Bout',size=(7,1), background_color='#F7F3EC', text_color='#000'),sg.Spin(values=('0.00', '0.25', '0.50', '1.00', '2.00'), initial_value='0.25', key='Bout')],\
             [sg.Text('Threshold',size=(7,1), background_color='#F7F3EC', text_color='#000'),sg.Spin([x*100 for x in range(100)], 200, key='Threshold')],\
             [sg.Text('---------------------------', justification='center', size=(15, 1), background_color='#F7F3EC', text_color='#000')],\
             [sg.Text('CSV export', justification='center', size=(15, 1), background_color='#F7F3EC', text_color='#000')],\
             [sg.Text('Interval (sec)',size=(10,1), background_color='#F7F3EC', text_color='#000'),sg.Spin([x*10 for x in range(100)], 60, key='Interval')],\
             [sg.Button('Export', size=(10, 1), font='Helvetica 12')]
    column2 = [sg.Image(filename='', key='-image-')], [sg.Image(filename='', key='-image2-')]
    layout = [    [sg.Column(column,background_color='#F7F3EC'),sg.Image(filename='', key='-graph-'), sg.Column(column2)],
                  [sg.Text('0', justification='center', size=(5, 1), text_color='#000', background_color='#FFFFFF', key='-time-'), sg.Slider(range=(0, num_frames),size=(40, 10), orientation='h', key='-slider-'), sg.Button('STOP/PLAY', size=(10, 1), font='Helvetica 14'),sg.Button('SAVE', size=(10, 1), font='Helvetica 14'),sg.Button('ZOOMABLE', size=(10, 1), font='Helvetica 14')],
                  [sg.Button('Exit', size=(10, 1), font='Helvetica 14')]]

    window = sg.Window('MouseDitection', layout, no_titlebar=False, location=(0, 0), resizable=True)

    image_elem = window['-image-']
    image2_elem = window['-image2-']
    slider_elem = window['-slider-']
    graph_elem = window['-graph-']
    playtime_elem = window['-time-']

    window.read(timeout=0)
    Threshold = 200
    Bout = 0.25

    # グラフの更新
    def graph_renew():
        fig = plt.figure()
        fig.canvas.draw()
        fig,df_freeze, df = csvproc.proc(csv_out,Threshold,Bout,fig)
        item = io.BytesIO()
        fig.savefig(item, format='png')
        graph_elem.update(data=item.getvalue())
        #figname = "graph_Threshold"+str(Threshold)+"_Bout"+str(Bout)+".png"
        #fig.savefig(os.path.join(outdir,figname))
        fig.savefig(os.path.join(outdir,"pic.png"))
        return fig, df_freeze, df
    # インターバル時間ごとのフリーズ時間を計算
    def interval(df_freeze, interval):
        i = 1
        freeze_tot = 0
        freeze_tot_all = 0
        df_interval = pd.DataFrame(index=[],columns=["total of interval"])
        for j in range(len(df_freeze.start)):
            if df_freeze.iat[j,1] < interval * i:
                freeze_tot = freeze_tot + df_freeze.iat[j,2]
            else:
                freeze_tot = freeze_tot + (interval * i - df_freeze.iat[j,0])
                rec = pd.Series([freeze_tot], index = df_interval.columns)
                df_interval = df_interval.append(rec, ignore_index = True)
                freeze_tot = 0
                freeze_tot = freeze_tot + (df_freeze.iat[j,1] - interval * i)
                i = i + 1
        return df_interval
    fig, df_freeze, df = graph_renew()

    cur_frame = 0
    play_flag = 1
    zoom_flag = 0
    while vidFile.isOpened():
        # イベントを取得
        event, values = window.read(timeout=0)

        # 「Exit」ボタン押下時の処理
        if event in ('Exit', None):
            break

        #　ビデオファイルからの読み込み
        ret, frame = vidFile.read() 
        ret2, frame2 = vidFile2.read()

        #　データが不足している場合は、ループを停止させます。
        if not (ret and ret2):  # if out of data stop looping
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, 0)
            vidFile2.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        #　スライダーを手動で動かした場合は、指定したフレームにジャンプします
        if int(values['-slider-']) != cur_frame-1:
            cur_frame = int(values['-slider-'])
            vidFile.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
            vidFile2.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)

        if event in ('STOP/PLAY', None):
            if play_flag == 1:
                play_flag = 0
            else:
                play_flag = 1
        # グラフの画像保存: 別ウィンドウで保存ダイアログを表示し保存
        if event in ('SAVE', None):
            root = tk.Tk()
            root.withdraw()
            root.filename = tkinter.filedialog.asksaveasfilename(initialdir = "outdir",title = "Save as",filetypes =  [("img file","*.png")])
            fig.savefig(os.path.join(outdir,root.filename))
        # 拡大可能なグラフを別ウィンドウ表示
        if event in ('ZOOMABLE', None):
            plt.show(block=False)
        # CSV(Bout期間とインターバル)をエクスポート
        if event in('Export'):
            filename = "freezelist_" + "bout" +str(int(float(values['Bout'])*100)) + "thr" + str(values['Threshold']) + ".csv"
            df_freeze.to_csv(os.path.join(outdir,filename))
            df_interval = interval(df_freeze, int(values['Interval']))
            filename = "interval_" + "bout" +str(int(float(values['Bout'])*100)) + "thr" + str(values['Threshold']) + "intvl" + str(values['Interval']) + ".csv"
            df_interval.to_csv(os.path.join(outdir,filename))
        # パラメータが変更されたらグラフを更新
        if Threshold != int(values['Threshold']) or Bout != float(values['Bout']):
            Threshold = int(values['Threshold'])
            Bout = float(values['Bout'])
            plt.close()
            fig,_,df = graph_renew()

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
        cur_time = int(cur_frame/fps)
        playtime_elem.update(str(cur_time) + " s")
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
        if len(df) > cur_frame:
            if df.iat[cur_frame,2] == 1:
                txt = "Freezing"
                color = (255,0,0)
            else:
                txt = "Moving"
                color = (0,0,255)
            cv2.putText(frame, txt, org=(160,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75,color=color,thickness=2, lineType=cv2.LINE_4)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        time.sleep(0.04)
        image_elem.update(data=imgbytes)

        imgbytes2 = cv2.imencode('.png', frame2)[1].tobytes()
        image2_elem.update(data=imgbytes2)

# 起動画面
print("<<<MouseFreezingDetection>>>")
print("Ver. 0.3 : 2022.02.03")
print("For monochrome videos")

programname = "MouseDitection"
root = tk.Tk()
root.withdraw()
fTyp = [("","*.mp4, *.avi")]
tkinter.messagebox.showinfo(programname,'Please select video file.')
movie = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = "~")
tkinter.messagebox.showinfo(programname,'Please select output folder.')
outdir = tkinter.filedialog.askdirectory(initialdir = "~")

param = setparam.setparam(movie)
csv_out = movieproc.proc(movie, outdir, param)    # mouse ditection and calclate moving -> csv file
movie_mask = os.path.join(outdir,"masked.mp4")
runmovie(movie,movie_mask,outdir)
