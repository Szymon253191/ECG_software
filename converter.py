
import matplotlib.pyplot as plt
import numpy as np
import csv
import tkinter
from matplotlib.figure import Figure
import tkinter.filedialog

# with open("mitdb\\test.csv", "r") as f:
#     lines = list(csv.reader(f, delimiter=","))
# lines = np.array(lines[2:], dtype=np.float32)
# print(lines.shape)
# lines.transpose()
# print(lines.shape)

my_csv = np.genfromtxt('test\\test.csv', delimiter=",")

time = my_csv[:,0]
data1 = my_csv[:,1]
# data2 = my_csv[:,2]
# plt.plot(time,data1)
print(time[-1]+time[3])
plt.show()

# ecg_path = tkinter.filedialog.askopenfilename()
# ecg_data = np.fromfile(ecg_path, dtype=np.float32)


# fs = 320
# time = np.arange(ecg_data.size) / fs

# f = Figure(figsize=(10,6), dpi=100)
# a = f.add_subplot(111)
# a.set_xlabel("time in s")
# a.set_ylabel("ECG in mV")
# a.set_title("ECG Signal")
# a.set_xlim(0, 10)

# a.plot(time,ecg_data);
