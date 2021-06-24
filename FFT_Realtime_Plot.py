from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
from scipy import fftpack


global data_display

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')

curve = p.plot()
sampling_freq = 48000                 
raw=serial.Serial("com6",baudrate=115200,bytesize=8,stopbits=1,timeout=1)

data_display = []


chunk_size=1000# smaller chunk size = slower data
def update():
	
	global  data_display
	
	current_data = np.zeros(chunk_size,dtype=int)
	
	for i in range(chunk_size):
		current_data[i]=raw.readline()

	freq_sig = np.abs(fftpack.fft(current_data)*2*np.pi/chunk_size)
	maximum = np.amax(current_data)
	print(maximum)
	freqs = fftpack.fftfreq(len(current_data))*sampling_freq

	curve.setData(freqs, freq_sig)
	
	app.processEvents()




timer = QtCore.QTimer()
timer.start() 
timer.timeout.connect(update)



if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()