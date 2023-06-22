import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import mplcursors

# energy table [keV]
# line:    TH232  RA226  U235/8  AC227  Others
U235_1  =                 143.8
CE141   =                                145.4
U235_2  =                 185.7
RA226   =         186.2
LU176_1 =                                202.0
AC228_1 =  209.3
TH227   =                         236.0
PB212   =  238.6
SE75_1  =                                264.7
RA223   =                         269.5
TI208_1 =  277.4
SE75_2  =                                279.5
PB214_1 =         295.2
LU176_2 =                                307.0
AC228_2 =  338.3
PB214_2 =         351.9
BA133   =                                356.0
CS134_1 =                                569.3
TI208_2 =  583.2
CS134_2 =                                604.7
BI214_1 =         609.3
CS137   =                                661.7
NB95    =                                765.8
BI214_2 =         768.0
CS134_3 =                                795.9
MN54    =                                834.9
TI208_3 =  860.5
AC228_3 =  911.2
AC228_4 =  969.0
BI214_3 =        1120.3
CO60_1  =                               1173.2
BI214_4 =        1238.0
CO60_2  =                               1332.5
K40     =                               1460.8
BI214_5 =        1764.5


# channel calibration (ADC channel)
channel_calibration_x0    = 90
channel_calibration_cs137 = 1302
channel_calibration_k40   = 2880

# 2 factors (for 2 lines) because of slight non-linearity (1 kink at CS137)
channel_calibration_factor_cs137_1 = CS137 / (channel_calibration_cs137 - channel_calibration_x0)
channel_calibration_factor_cs137_2 = (K40 - CS137) / (channel_calibration_k40 - channel_calibration_cs137)

# x axis max visible range
xaxis_max_kev = 1800

def lowPassZeroPhase(input, output, smoothing):
    temp = [0 for _ in range(len(input))]
    in_len = len(input)
    value = input[0]
    for i in range(1, in_len):
        currentValue = input[i]
        value += (currentValue - value) / smoothing
        temp[i] = value
    value = input[in_len - 1]
    for i in range(1, in_len):
        currentValue = input[in_len - 1 - i]
        value += (currentValue - value) / smoothing
        output[in_len - 1 - i] = (temp[in_len - 1 - i] + value) / 2.0

dataframe_1 = pd.read_json(sys.argv[1])
x_data = list(dataframe_1.index.values)

# scale x data values (1 kink at CS137)
x_offset = 0
for i in range(0, channel_calibration_cs137):
    x_data[i] = x_offset + (x_data[i] - channel_calibration_x0) * channel_calibration_factor_cs137_1
x_offset = (x_data[channel_calibration_cs137] - channel_calibration_x0) * channel_calibration_factor_cs137_1
for i in range(channel_calibration_cs137, len(x_data)):
    x_data[i] = x_offset + (x_data[i] - channel_calibration_cs137) * channel_calibration_factor_cs137_2

time_1 = list(dataframe_1.time.values)[0]
minutes_1 = list(dataframe_1.minutes.values)[0]
cpm_1  = list(dataframe_1.avr_cpm.values)[0]
events_1 = list(dataframe_1.events.values)[0]
y_data_1 = list(dataframe_1.data.values)
y_datafilt_1 = [0 for _ in range(len(x_data))]

lowPassZeroPhase(y_data_1, y_datafilt_1, 10.0)

for i in range(0, len(x_data)):
    y_data_1[i] = y_data_1[i] / minutes_1
    y_datafilt_1[i] = y_datafilt_1[i] / minutes_1

mpl.rcParams['toolbar'] = 'None'
fig = plt.figure()
fig.canvas.manager.set_window_title('Gamma Spectrum: ' + sys.argv[1])
major_ticks = list(range(0, xaxis_max_kev, 500))
minor_ticks = list(range(0, xaxis_max_kev, 100))
ax1 = fig.add_subplot(111)
ax1.set(title='time elapsed: ' + time_1 + '  -  total events: ' + str(events_1) + '  -  average cpm: ' + str(cpm_1) + '\n\n\n')
ax1.set_xticks(major_ticks)
ax1.set_xticks(minor_ticks, minor=True)
ax1.grid(which='minor', alpha=0.2)
ax1.grid(which='major', alpha=0.5)
ax1.set_yscale("log", nonpositive='clip')
ax1.set_xlim(100, xaxis_max_kev)
ax1.set_ylim(0.001, 2)
ax1.set_xlabel("energy [keV]")
ax1.set_ylabel("cpm")
ax1.plot(x_data, y_data_1, lw=1, label="Raw Radiation")
ax1.legend(loc="upper right")
ax1.plot(x_data, y_datafilt_1, alpha=0.8, lw=1, label="Filtered Radiation")
ax1.legend(loc="upper right")


plt.axvline(x=U235_1, color='b', linestyle='--')
plt.text(U235_1, 2.4,'U235', color='b', fontsize=6)
plt.axvline(x=U235_2, color='b', linestyle='--')
plt.text(U235_2, 2.4,'U235', color='b', fontsize=6)

plt.axvline(x=TH227, color='g', linestyle='--')
plt.text(TH227, 2.4,'TH227', color='g', fontsize=6)
plt.axvline(x=RA223, color='g', linestyle='--')
plt.text(RA223, 2.4,'RA223', color='g', fontsize=6)

plt.axvline(x=AC228_1, color='#ff8000', linestyle='--')
plt.text(AC228_1, 2.8,'AC228', color='#ff8000', fontsize=6)
plt.axvline(x=PB212, color='#ff8000', linestyle='--')
plt.text(PB212, 2.8,'PB212', color='#ff8000', fontsize=6)
plt.axvline(x=TI208_1, color='#ff8000', linestyle='--')
plt.text(TI208_1, 2.8,'TI208', color='#ff8000', fontsize=6)
plt.axvline(x=AC228_2, color='#ff8000', linestyle='--')
plt.text(AC228_2, 2.8,'AC228', color='#ff8000', fontsize=6)
plt.axvline(x=TI208_2, color='#ff8000', linestyle='--')
plt.text(TI208_2, 2.8,'TI208', color='#ff8000', fontsize=6)
plt.axvline(x=TI208_3, color='#ff8000', linestyle='--')
plt.text(TI208_3, 2.8,'TI208', color='#ff8000', fontsize=6)
plt.axvline(x=AC228_3, color='#ff8000', linestyle='--')
plt.text(AC228_3, 2.8,'AC228', color='#ff8000', fontsize=6)
plt.axvline(x=AC228_4, color='#ff8000', linestyle='--')
plt.text(AC228_4, 2.8,'AC228', color='#ff8000', fontsize=6)

plt.axvline(x=RA226, color='#ff00ff', linestyle='--')
plt.text(RA226, 3.2,'RA226', color='#ff00ff', fontsize=6)
plt.axvline(x=PB214_1, color='#ff00ff', linestyle='--')
plt.text(PB214_1, 3.2,'PB214', color='#ff00ff', fontsize=6)
plt.axvline(x=PB214_2, color='#ff00ff', linestyle='--')
plt.text(PB214_2, 3.2,'PB214', color='#ff00ff', fontsize=6)
plt.axvline(x=BI214_1, color='#ff00ff', linestyle='--')
plt.text(BI214_1, 3.2,'BI214', color='#ff00ff', fontsize=6)
plt.axvline(x=BI214_2, color='#ff00ff', linestyle='--')
plt.text(BI214_2, 3.2,'BI214', color='#ff00ff', fontsize=6)
plt.axvline(x=BI214_3, color='#ff00ff', linestyle='--')
plt.text(BI214_3, 3.2,'BI214', color='#ff00ff', fontsize=6)
plt.axvline(x=BI214_4, color='#ff00ff', linestyle='--')
plt.text(BI214_4, 3.2,'BI214', color='#ff00ff', fontsize=6)
plt.axvline(x=BI214_5, color='#ff00ff', linestyle='--')
plt.text(BI214_5, 3.2,'BI214', color='#ff00ff', fontsize=6)

plt.axvline(x=CE141, color='r', linestyle='--')
plt.text(CE141, 2.1,'CE141', color='r', fontsize=6)
plt.axvline(x=LU176_1, color='r', linestyle='--')
plt.text(LU176_1, 2.1,'LU176', color='r', fontsize=6)
plt.axvline(x=SE75_1, color='r', linestyle='--')
plt.text(SE75_1, 2.1,'SE75', color='r', fontsize=6)
plt.axvline(x=SE75_2, color='r', linestyle='--')
plt.text(SE75_2, 2.1,'SE75', color='r', fontsize=6)
plt.axvline(x=LU176_2, color='r', linestyle='--')
plt.text(LU176_2, 2.1,'LU176', color='r', fontsize=6)
plt.axvline(x=BA133, color='r', linestyle='--')
plt.text(BA133, 2.1,'BA133', color='r', fontsize=6)
plt.axvline(x=CS134_1, color='r', linestyle='--')
plt.text(CS134_1, 2.1,'CS134', color='r', fontsize=6)
plt.axvline(x=CS134_2, color='r', linestyle='--')
plt.text(CS134_2, 2.1,'CS134', color='r', fontsize=6)
plt.axvline(x=CS137, color='r', linestyle='--')
plt.text(CS137, 2.1,'CS137', color='r', fontsize=6)
plt.axvline(x=NB95, color='r', linestyle='--')
plt.text(NB95, 2.1,'NB95', color='r', fontsize=6)
plt.axvline(x=CS134_3, color='r', linestyle='--')
plt.text(CS134_3, 2.1,'CS134', color='r', fontsize=6)
plt.axvline(x=MN54, color='r', linestyle='--')
plt.text(MN54, 2.1,'MN54', color='r', fontsize=6)
plt.axvline(x=CO60_1, color='r', linestyle='--')
plt.text(CO60_1, 2.1,'CO60', color='r', fontsize=6)
plt.axvline(x=CO60_2, color='r', linestyle='--')
plt.text(CO60_2, 2.1,'CO60', color='r', fontsize=6)
plt.axvline(x=K40, color='r', linestyle='--')
plt.text(K40, 2.1,'K40', color='r', fontsize=6)

cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_add(sel):
    energy = sel.target[0]
    cpm = sel.target[1]
    ann = sel.annotation
    ann.set_text('Energy: {:.1f} keV\nCpm: {:.5f}'.format(energy, cpm))

plt.show()
