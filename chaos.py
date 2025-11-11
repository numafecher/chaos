# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:14:44 2025

@author: pcynf3
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as w
#import time
import sys
sys.path.insert(1,"C:\\python")
import y2daq


def switchoffCallback(event):
    """ Callback function for button to switch off loop """
    global switchon
    global Voff
    switchon = False;
    print('switched off')
    
def plus5freqCallback(event):
    freqHandle.set_val(freqHandle.val+5)

def minus5freqCallback(event):
    freqHandle.set_val(freqHandle.val-5)

def plus01ampCallback(event):
    ampHandle.set_val(ampHandle.val+0.05)

def minus01ampCallback(event):
    ampHandle.set_val(ampHandle.val-0.05)
    
    
# Button to stop acquisition
offax=plt.axes([0.65,0.15,0.1,0.1])
offHandle=w.Button(offax,'off')
offHandle.on_clicked(switchoffCallback)

plus5freqax=plt.axes([0.8,0.42,0.05,0.05])
plus5freqHandle=w.Button(plus5freqax,'+5')
plus5freqHandle.on_clicked(plus5freqCallback)

minus5freqax=plt.axes([0.7,0.42,0.05,0.05])
minus5freqHandle=w.Button(minus5freqax,'-5')
minus5freqHandle.on_clicked(minus5freqCallback)

plus5ampax=plt.axes([0.8,0.72,0.05,0.05])
plus5ampHandle=w.Button(plus5ampax,'+0.05')
plus5ampHandle.on_clicked(plus01ampCallback)

minus01ampax=plt.axes([0.7,0.72,0.05,0.05])
minus01ampHandle=w.Button(minus01ampax,'-0.05')
minus01ampHandle.on_clicked(minus01ampCallback)

switchon = True
# Add input/output
a = y2daq.analog() # create analog data acquisition object
a.addInput(0)
a.addInput(1)
a.addOutput(0) #output AO0
a.Nscans = 10000
a.Rate = 30000

#Make signal generator
# Create a 500 Hz sine wave lasting for 1 second
duration = 1
t = np.arange(0,duration+1/a.Rate,1/a.Rate)
#signal = 10*np.sin(2*np.pi*freq*t)
# Output the sine wave

# Set up plots
plt.figure(1, figsize=(11, 7))

# xy plot
axes1 = plt.axes([0.2, 0.6, 0.35, 0.3])
axes1.cla()
axes1.set_xlabel('Height')
axes1.set_ylabel('Velocity')

freqax = plt.axes([0.65,0.35,0.25,0.05])
freqax.cla()
freqHandle=w.Slider(freqax, 'freq', 0, 2000, valinit = 475)

ampax = plt.axes([0.65,0.65,0.25,0.05])
ampax.cla()
ampHandle=w.Slider(ampax, 'amp', 0,10, valinit = 1)

# phase space diagram
axes2 = plt.axes([0.2, 0.15, 0.35, 0.3])
axes2.cla()
line2, = axes2.plot(0, 0, 'r-')
axes2.set_xlabel('x')
axes2.set_ylabel('y')

default_freq = freqHandle.val
while switchon == True:
    
    freq = freqHandle.val
    amp = ampHandle.val
    signal = amp*np.sin(2*np.pi*freq*t)
    data, tstamps = a.run(signal)
    #data, tstamps = a.read()
    vb = data[0]
    vc = data[1]
    axes2.cla()  
    axes2.plot(tstamps[2000:3000:2],vb[2000:3000:2],color = 'c')
    axes2.set_xlabel('Ball Displacement')
    axes2.set_ylabel('Amplitude')
    axes2.relim()
    axes2.autoscale()
    
    axes1.cla()
    axes1.plot(vb[5000:-5000:2],vc[5000:-5000:2],'.',markersize=2,color='c')
    axes1.set_xlabel('Height')
    axes1.set_ylabel('Velocity')
    axes1.relim()
    axes1.autoscale()
    plt.pause(1)