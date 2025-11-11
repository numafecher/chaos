# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 10:14:08 2025

@author: pcynf3
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:14:44 2025

@author: pcynf3
"""

import numpy as np
import matplotlib.pyplot as plt
#import time
import sys
sys.path.insert(1,"C:\\python")
import y2daq  

switchon = True
# Add input/output
a = y2daq.analog(fast=True) # create analog data acquisition object
a.addInput(0)
a.addInput(1)
a.addOutput(0) #output AO0
#a.Nscans = 10000
freq = 475

duration = 1


# Set up plots
plt.figure(1, figsize=(11, 7))

# phase space plot
axes1 = plt.axes([0.2, 0.6, 0.35, 0.3])
axes1.cla()
axes1.set_xlabel('Height')
axes1.set_ylabel('Velocity')

# poincare section diagram
axes2 = plt.axes([0.2, 0.15, 0.35, 0.3])
axes2.cla()
axes2.set_xlabel('h')
axes2.set_ylabel('v')


amps = np.arange(0.8,2,0.02)

for amp in amps:
    print(round(amp,2))
    a.Rate = freq*100
    t = np.arange(0,duration+1/a.Rate,1/a.Rate)
    signal = amp*np.sin(2*np.pi*freq*t)
    data, tstamps = a.run(signal)
    
    vb = data[0]
    vc = data[1]
    
    indices = np.arange(int(0.25*100),len(vb),int(100))
    vbvals = vb[indices]
    vcvals = vc[indices]

    
    axes1.cla()
    axes1.plot(vb[int(0.25*len(vb)):-int(0.25*len(vb))],vc[int(0.25*len(vc)):-int(0.25*len(vc))],'.',markersize=2,color='g')
    axes1.set_xlabel('Height')
    axes1.set_ylabel('Velocity')
    axes1.relim()
    axes1.autoscale()
    
    axes2.cla()
    axes2.plot(vbvals[int(0.25*len(vbvals)):-int(0.25*len(vbvals))],vcvals[int(0.25*len(vcvals)):-int(0.25*len(vcvals))],'.',markersize=2,color='g')
    axes2.set_xlabel('Height')
    axes2.set_ylabel('Velocity')
    axes2.relim()
    axes2.autoscale()
    
    plt.pause(1)