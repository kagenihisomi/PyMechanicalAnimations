# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 12:03:04 2017

@author: John
asdftoger

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.animation as animation

#Lengths of the linkages, 
#a,b,c,d represent linkages starting from left fixed and going clockwise
#makes sure that the grashoff condition is satisfied
a,b,c,d = 50,220,250,100
#the angle that the linkages make wrt xaxis of the fixed points a,d
th_a = np.arange(0,10*np.pi,0.05*np.pi)

#Theta d is a long equation
K1 = d/a
K2 = d/c
K3 = (a**2-b**2+c**2+d**2)/(2*a*c)
A = np.cos(th_a) - K1 - K2*np.cos(th_a) + K3
B = -2*np.sin(th_a)
C = K1 - (K2+1)*np.cos(th_a) + K3

#Grashoff condition
disc = (B**2)-4*A*C 

#Checks if the four_bar linkage is grashoff
assert( np.greater_equal(disc,0).all())

#Final formula for other fixed angle
th_d = 2*np.arctan((-B - np.sqrt(disc) )/(2*A))

#x1,x2 ... y1,y2 refer to the points starting from 0,0 going clockwise
#1 and 4 are fixed
x1,x4 = 0, d
y1,y4 = 0,0
#2 and 3 are updating
#x3 needs d to be added
x2,x3 = a*np.cos(th_a), d + c*np.cos(th_d)
y2,y3 = a*np.sin(th_a), c*np.sin(th_d)

#Defining xandylims of the plot
temp = x1,x2,x3,x4
xmin = np.amin([np.amin(mini) for mini in temp])
xmax = np.amax([np.amax(mini) for mini in temp])
temp = y1,y2,y3,y4
ymin = np.amin([np.amin(mini) for mini in temp])
ymax = np.amax([np.amax(mini) for mini in temp])
#xmin,xmax

fig = plt.figure()

bord = 20 #give the animation an offset
ax = fig.add_subplot(111, autoscale_on=False,
                     xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
ax.grid()
line, = ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)

def init():
    line.set_data([], [])
#    time_text.set_text('')
    return line,


def animate(i):
    thisx = [x1, x2[i],x3[i],x4]
    thisy = [y1, y2[i],y3[i],y4]

    line.set_data(thisx, thisy)
#    time_text.set_text(time_template % (i*dt))
    return line,
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y2)),
                              interval=1000/60, blit=True, init_func=init)

ani.save('four_bar_linkage2.mp4', fps=60,extra_args=['-vcodec', 'libx264'])
plt.show()