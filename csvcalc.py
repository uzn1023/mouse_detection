##!/usr/bin/env python
import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec

Threshold = 300
bout = 0.25

filename = "./result/20211021/green_long"
df = pd.read_csv(filename + '.csv',names=("time","move"),skiprows=1)
#plt.plot(df.time,df.move)
#plt.show()
df["bin"] = 0

frag_freeze = 0
df_freeze = pd.DataFrame(index=[],columns=["start","end","long"])
for i in range(len(df.time)):
    if df.iat[i,1] < Threshold:
        df.iat[i,2] = 1
        if frag_freeze == 0:
            freeze_start = df.iat[i,0]
        frag_freeze = 1
       
    else:
        if frag_freeze == 1:
            freeze_end = df.iat[i,0]
            rec = pd.Series([freeze_start, freeze_end, freeze_end-freeze_start], index = df_freeze.columns)
            df_freeze = df_freeze.append(rec, ignore_index = True)
        frag_freeze = 0
    print(i)
if frag_freeze == 1:
    freeze_end = df.iat[i,0]
    rec = pd.Series([freeze_start, freeze_end, freeze_end-freeze_start], index = df_freeze.columns)
    df_freeze = df_freeze.append(rec, ignore_index = True)


fig = plt.figure()
spec = gridspec.GridSpec(ncols = 1, nrows = 2, height_ratios=[3, 1])
ax1 = fig.add_subplot(spec[0])
ax1.hlines(Threshold, df.iat[0,0], df.iat[i,0], linestyle = "dashed", linewidth = 0.5, color = "red")
ax1.plot(df.time,df.move, linewidth = 0.5, color = "blue")
ax1.set_ylabel("Count of moving [px]")
ax1.set_title("bout=" + str(bout))

ax2 = fig.add_subplot(spec[1])

for j in range(len(df_freeze.start)):
    if df_freeze.iat[j,2] > bout:
        ax2.axvspan(df_freeze.iat[j,0], df_freeze.iat[j,1], color="black")
    else:
        ax2.axvspan(df_freeze.iat[j,0], df_freeze.iat[j,1], color="white")
    #ax2.axvspan(df_freeze.iat[j,1], df.iat[i,0], color="white")
ax2.set_xlabel("Time [s]")
plt.savefig(filename + "_bout"+str(bout)+".png")
plt.show()

df_freeze.to_csv(filename + "_duration.csv")
