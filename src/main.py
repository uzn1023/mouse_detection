##!/usr/bin/env python
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import csvproc
import movieproc


def plotgraph(Threshold,bout,csv_out):
    plt.close()
    fig = csvproc.proc(csv_out,Threshold,bout)
    plt.pause(0.01)


programname = "MouseDitection"
root = tk.Tk()
root.withdraw()
fTyp = [("","*.mp4")]
tkinter.messagebox.showinfo(programname,'Please select video file.')
movie = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = "..")
tkinter.messagebox.showinfo(programname,'Please select output folder.')
outdir = tkinter.filedialog.askdirectory(initialdir = "..")

csv_out = movieproc.proc(movie,outdir)    # mouse ditection and calclate moving -> csv file

win = tk.Tk()
win.title('Input parameter')
win.geometry("300x200")

label1 = ttk.Label(win, text='Threshold')
label1.grid(row=1,column=1)
label1.grid_configure(padx=10, pady=15)

var = tk.IntVar(win)
var.set(500)
sp1 = tk.Spinbox(win,textvariable=var,from_=0,to=100000,increment=100)
sp1.grid(row=1,column=2)
sp1.grid_configure(padx=10, pady=15)

label2 = ttk.Label(win, text='Bout')
label2.grid(row=2,column=1)
label2.grid_configure(padx=10, pady=15)

var2 = tk.DoubleVar()
var2.set(0.25)
ary=[0, 0.25, 0.5, 1, 2]
sp2 = tk.Spinbox(win,textvariable=var2,value=ary,state='readonly')
sp2.grid(row=2,column=2)
sp2.grid_configure(padx=10, pady=15)

frame = ttk.Frame(win)
frame.grid(row=3,column=2)
frame.grid_configure(padx=10, pady=15)
#button = tk.Button(frame, text="Calculate", command=lambda:plotgraph(var.get(),var2.get(),csv_out))
button = tk.Button(frame, text="Calculate", command=lambda:print(var2.get()))
button.grid()

win.mainloop()
