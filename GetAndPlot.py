###########################################
######### GET AND PLOT ECG PLOTS ##########
###########################################

import wfdb
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Cursor, Button

###########################################
##### Place to write down data bases ######


dbs = [

    {
        "name": 'ltdb', 
        "attr_format": 'atr', 
        "record":'14046',
        "channels": 'ECG1',
        "data_points": 5*128
    },
    # {
    #     "name": 'wctecgdb', 
    #     "attr_format": 'hea', 
    #     "record":'patient008/seg01', 
    #     "channels": 'I'
    # },
]

##############################################
# Downloading data and setting up parameters #


def maybe_download_db(db):

  if(os.path.isdir(db)):
    return
  else:
    wfdb.dl_database(db, db)


for db in dbs:

  maybe_download_db(db['name'])
  records = wfdb.get_record_list(db['name'])
  selected_rec = db["record"] if "record" in db else records[0]

  record = wfdb.rdrecord(db['name'] + '/' + selected_rec)

  sampto = 10000 if record.sig_len > 10000 else record.sig_len
#   sampto = record.sig_len

  info = wfdb.rdsamp(db['name'] + '/' + selected_rec, sampto=sampto)

  record, fields = wfdb.rdsamp(
      db['name'] + '/' + selected_rec, sampto=sampto, channels=[0])
  annotation = wfdb.rdann(
      db['name'] + '/' + selected_rec, db['attr_format'], sampto=sampto)

###########################################
#### Changing Data points to time axis ####

  dataPointIndex = 0
  ox = []
  oyData = []
  oxData = []

  for x in record:

    ox = dataPointIndex/fields['fs']
    oxData.extend([ox])

    dataPointIndex += 1

  temp = np.array(oxData)
  temp.transpose()

#     print(temp)

  oyData = np.array(record)
  oxData = np.array(temp)

#     print(oyData.shape, oxData.shape)

###########################################
######### Adjusting grid in sec ###########

  fig, ax = plt.subplots(nrows=1, figsize=(16, 6))
  plt.subplots_adjust(bottom=0.25)
  ax.minorticks_on()

  major_tick_time = 1
  minor_tick_time = 0.05

  major_ticks = np.arange(-1, sampto/fields['fs'] + 1, major_tick_time)
  minor_ticks = np.arange(-1, sampto/fields['fs'] + 1, minor_tick_time)

  ax.set_xticks(major_ticks)
  ax.set_xticks(minor_ticks, minor=True)
  ax.set_yticks(major_ticks)
  ax.set_yticks(minor_ticks, minor=True)

###########################################
############# Ploting leads ###############

#   plt.figure()

  ax.grid(which='major', linestyle='-',
          color='red', linewidth='1.0', alpha=0.5)
  ax.grid(which='minor', linestyle=':',
          color='black', linewidth='0.5', alpha=0.2)
  plt.title(db['name'] + " ECG record " + selected_rec +
            " - channel_name: " + db['channels'])

  plt.plot(oxData, oyData)

  # Choose the Slider color
slider_color = 'White'

# Set the axis and slider position in the plot
axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                         facecolor=slider_color)
slider_position = Slider(axis_position,
                         'Pos', -0.5, sampto/fields['fs'] - 6.5)

# update() function to change the graph when the
# slider is in use


def update(val):
    pos = slider_position.val
    ax.axis([pos, pos+7, min(oyData) -  min(oyData) * 0.2, max(oyData) + max(oyData) * 0.2])
    fig.canvas.draw_idle()


# update function called using on_changed() function
slider_position.on_changed(update)

# plt.show()

###########################################
######### Printing info at end ############

# print("grid: ", minor_tick_time, " / ", major_tick_time, " s")
# cursor = Cursor(ax, color='green', linewidth=1)


plt.show()
