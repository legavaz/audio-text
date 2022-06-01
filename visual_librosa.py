from tkinter import Variable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# https://librosa.org/doc/0.7.2/tutorial.html
import librosa as lr 

# Variable
file_name = r"tmp\20210227_135213_test.m4a"
# file_name = r"tmp\AUD-20220518-WA0000.m4a"


audio,sfreq = lr.load(file_name)

# time = np.arange(0,len(audio)) / sfreq
# print(time)

# fig,ax = plt.subplots()
# ax.plot(time,audio)
# ax.set(xlabel = 'time',ylabel='sound')
# plt.show()

lr.
print(len(audio),audio)