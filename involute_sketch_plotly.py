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

#Screw matplotlib, Create online graph
import plotly 

plotly.tools.set_credentials_file(username='asdftoger', 
                                  api_key='tJVUVmR9W4xQyto7jIL7',
                                  )
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

stream_ids = tls.get_credentials_file()['stream_ids']   

#Creating np involutes
t = np.linspace(0,2*np.pi,1000)
r = 1
phase = [cmath.exp(1j*i) for i in t]
circle = r*np.array(phase)

#Decide how long you want the involute to be
inv_len = 250
path = (r-1j*(r*t[:inv_len]))*phase[:inv_len]

##sketch the involute
#plt.plot(np.real(circle),np.imag(circle))
#plt.plot(np.real(path),np.imag(path))
#plt.axis('equal')
#plt.show()

trace0 = go.Scatter(
                 x = np.real(path),
                 y = np.imag(path),
                 mode = 'lines'
                 
                 )
trace1 = go.Scatter(
                    x = np.real(circle)
                    ,y= np.imag(circle)
                    ,mode='lines'
                    )
data = go.Data([trace0,trace1])

py.plot(data, filename = 'Involute plot')