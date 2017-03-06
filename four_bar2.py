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

from matplotlib import patches
import matplotlib.animation as animation
#Defines crossed or open configuration
ROTATION = 'cxw'
MODE = 'open'
#Lengths of the linkages, 
#a,b,c,d represent linkages starting from left fixed and going clockwise
#makes sure that the grashoff condition is satisfied
#Since linkage a is the driving linkage, b+c must be greater than a+d

a,b,c,d = 200,350,280,300
assert(b + c >= d + a)

#the angle that the linkages make wrt xaxis of the fixed points a,d
#step controls how fast the linkage drives
step = 0.01
if ROTATION == 'cw':
    th_a = np.arange(2*np.pi,0,-step*np.pi)
else:
    th_a = np.arange(0,2*np.pi,step*np.pi)

#Degrees, used for drawing arcs
th_a_d = th_a * 180/np.pi

#==============================================================================
# Calculating theta_d
#==============================================================================
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
if MODE =='open':
    th_d = 2*np.arctan((-B - np.sqrt(disc) )/(2*A))
else:
    th_d = 2*np.arctan((-B + np.sqrt(disc) )/(2*A))
#Degrees, used for drawing arcs
th_d_d = th_d * 180/np.pi

#==============================================================================
# Determining axes limits
#==============================================================================
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

bord = 100 #give the animation an offset
ax = fig.add_subplot(111, autoscale_on=False,
                     xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
ax.grid()
line, = ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)

#Initialize an arc patch
#patch1 -> angle of point1 etc.
patch1 = patches.Arc((x1,y1),100,100,0,0,0,color='r')
patch4 = patches.Arc((x4,y4),100,100,0,0,0,color = 'b')

#
ang_text = ax.text(0.5, 0.1, '', transform=ax.transAxes)
#Initialize lines and patches
def init():
    line.set_data([], [])
    ax.add_patch(patch1)
    ax.add_patch(patch4)
    
    ang_text.set_text('')
    return line, ang_text
    
#Animate
def animate(i):
    #This uses global angles in degrees
    global th_a_d,patch1
    global th_d_d,patch4
    
    #This draws the linkages
    thisx = [x1, x2[i],x3[i],x4]
    thisy = [y1, y2[i],y3[i],y4]
    line.set_data(thisx, thisy)
    
    #This draws the angles
    ax.patches.remove(patch1)
    ax.patches.remove(patch4)
    patch1= patches.Arc((x1,y1),100,100,0,0,th_a_d[i],color='r')
    patch4 = patches.Arc((x4,y4),100,100,0,0,th_d_d[i],color = 'b')
    ax.add_patch(patch1)
    ax.add_patch(patch4)
    
    #This displays the angles
    text = \
    'Angle1 (red): ' + str(round(th_a_d[i],2)) + '\n' + \
    'Angle4 (blue): ' + str(round(th_d_d[i],2)) + '\n'
    ang_text.set_text(text)
    return line, patch1,patch4,ang_text
    pass


ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y2)),
                              interval=30, blit=True, init_func=init)
#Save animation
#ani.save('four_bar_linkage.mp4', fps=60,extra_args=['-vcodec', 'libx264'])
plt.show()