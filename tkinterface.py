##!/usr/bin/env python
import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox

programname = "MouseDitection"
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*.mp4")]
tkinter.messagebox.showinfo(programname,'Please select video file.')
file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = "~")

tkinter.messagebox.showinfo(programname,'Please select output folder.')
folder = tkinter.filedialog.askdirectory(initialdir = "~")
print("hoge")
