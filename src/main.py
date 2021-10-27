##!/usr/bin/env python
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import csvproc
import movieproc

programname = "MouseDitection"
root = tk.Tk()
root.withdraw()
fTyp = [("","*.mp4")]
tkinter.messagebox.showinfo(programname,'Please select video file.')
movie = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = "..")
tkinter.messagebox.showinfo(programname,'Please select output folder.')
outdir = tkinter.filedialog.askdirectory(initialdir = "..")

csv_out = movieproc.proc(movie,outdir)    # mouse ditection and calclate moving -> csv file

while(1):
    Threshold = float(input('Enter Threshould: '))
    bout = float(input('Enter bout: '))
    plt.close()
    fig = csvproc.proc(csv_out,Threshold,bout)
    plt.pause(0.01)
