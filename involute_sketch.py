# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:09:57 2017

@author: John
asdftoger

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

import cmath

#Creating np involutes
t = np.linspace(0,2*np.pi,1000)
r = 1
phase = [cmath.exp(1j*i) for i in t]
circle = r*np.array(phase)

#Decide how long you want the involute to be
inv_len = 250
path = (r-1j*(r*t[:inv_len]))*phase[:inv_len]

#sketch the involute
plt.plot(np.real(circle),np.imag(circle))
plt.plot(np.real(path),np.imag(path))
plt.axis('equal')
plt.show()