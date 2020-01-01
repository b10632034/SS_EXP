import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal
from fractions import Fraction



#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)


#initial
fig, (ax,ax2,ax3,ax4,ax5) = plt.subplots(5,1,figsize=(20, 20))
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
plt.show(block = False)
plt.setp(line2,color = 'r')


PData= PlotData(500)
ax.set_ylim(0,100)
ax2.set_ylim(-1000,1000)
ax3.set_ylim(0,100)
ax5.set_ylim(-2,2)




# plot parameters
print ('plotting data...')
# open serial port
strPort='com3'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()

while True:
    
    for ii in range(10):

        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data-300)
        except:
            pass
    yf=(np.fft.fft(PData.axis_y))
    xf=np.arange(0,len(PData.axis_y)/100,1/100)
    yr=signal.lfilter([1/3, 1/3, 1/3], 1, PData.axis_y)
    w,h= signal.freqz([1/3, 1/3, 1/3])
    angle=np.linspace(-np.pi,np.pi,50)
    cirx=np.sin(angle)
    ciry=np.cos(angle)
    r=[np.exp(1j*1/3),np.exp(1j*1/3),np.exp(1j*1/3),np.exp(-1j*1/3),np.exp(-1j*1/3),np.exp(-1j*1/3)]	
    ax4.set_ylim(-0.5,np.max(h)+0.5)
    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(0,len(PData.axis_y)/100,1/100)
    ax3.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax4.set_xlim(0,np.pi)
    ax5.set_xlim(-10,10)
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(xf)
    line2.set_ydata(yf)
    line3.set_xdata(PData.axis_x)
    line3.set_ydata(yr)
    line4.set_xdata(w)
    line4.set_ydata(np.abs(h))
    line5, = ax5.plot(cirx,ciry,'k-')
    line5, = ax5.plot(np.real(r),np.imag(r),'o',markersize=2)
    plt.setp(line5,color = 'b')
    line5, = ax5.plot(np.real(0),np.imag(0),'x',markersize=2)
    plt.setp(line5,color = 'r')
    fig.canvas.draw()
    fig.canvas.flush_events()
