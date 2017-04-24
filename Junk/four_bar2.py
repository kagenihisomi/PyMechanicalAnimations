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
ROTATION = 'ccw'
MODE = 'open'
#Lengths of the linkages, 
#a,b,c,d represent linkages starting from left fixed and going clockwise
#makes sure that the grashoff condition is satisfied
#Since linkage a is the driving linkage, b+c must be greater than a+d

a,b,c,d = 50,60,200,200
assert(b + c >= d + a)

#the angle that the linkages make wrt xaxis of the fixed points a,d
#step controls how fast the linkage drives
step = 20/180
if ROTATION == 'cw':
    th_a = np.arange(2*np.pi,0,-step*np.pi)
else:
    th_a = np.arange(0,2*np.pi+0.0001,step*np.pi)

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
# Calculating theta_b
#==============================================================================

#x1,x2 ... y1,y2 refer to the points starting from 0,0 going clockwise
#1 and 4 are fixed
x1,x4 = 0,d
y1,y4 = 0,0
#2 and 3 are updating
#x3 needs d to be added
x2,x3 = a*np.cos(th_a), d + c*np.cos(th_d)
y2,y3 = a*np.sin(th_a), c*np.sin(th_d)

#theta b is the arctan of point 3 and 2
th_b = np.arctan((y3-y2)/(x3-x2))
#Degrees, used for drawing arcs
th_b_d = th_b * 180/np.pi


#==============================================================================
# Determining axes limits
#==============================================================================


#Defining xandylims of the plot
temp = x1,x2,x3,x4
xmin = np.amin([np.amin(mini) for mini in temp])
xmax = np.amax([np.amax(mini) for mini in temp])
temp = y1,y2,y3,y4
ymin = np.amin([np.amin(mini) for mini in temp])
ymax = np.amax([np.amax(mini) for mini in temp])
#xmin,xmax

fig = plt.figure()
fig.set_size_inches(6,4.8,True)
plt.axis('off')
plt.tight_layout()
bord = 200 #give the animation an offset
ax = fig.add_subplot(111, autoscale_on=True,
                     xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
ax.grid()
#Draw linkages
line, = ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)
#==============================================================================
# Follower curve
#==============================================================================
    
#==============================================================================
# Drawing angles
#==============================================================================
#Draw maximum angle subtended by output linkage
len_arrow = 300
#Max and min angles, radians
a_min = np.amin(th_d)
a_max = np.amax(th_d)
#draw arrows
ax.arrow(x4,y4,
         len_arrow * np.cos(a_min), len_arrow * np.sin(a_min),
         fc='b', ec='b')
ax.arrow(x4,y4,
         len_arrow * np.cos(a_max), len_arrow * np.sin(a_max)
         ,fc='b', ec='b')
#Max and min angles, degrees
a_min = np.amin(th_d_d)
a_max = np.amax(th_d_d)
#Draw angle between the arrows
ang_radius = 200 #for both drawing and writing
ang_subtended = a_max - a_min #angle subtended
ang_patch = patches.Arc((x4,y4),ang_radius,ang_radius,a_min,0,ang_subtended)
ax.add_patch(ang_patch)

#Write angle
#x,y = (x4 + ang_radius*np.cos(a_min),y4 + ang_radius*np.sin(a_min))
#s = str(round(ang_subtended,2) )
#ang_text = ax.text(x,y,'')
#ang_text.set_text(s)

#Initialize an arc patch
#patch1 -> angle of point1 etc.
patch1 = patches.Arc((x1,y1),100,100,0,0,0,color='r')
patch2 = patches.Arc((x2[0],y2[0]),100,100,0,0,0,color='g')
patch4 = patches.Arc((x4,y4),100,100,0,0,0,color = 'b')

#Transmisson angle
len_arrow = 100
#arrow direction: use 0[i] - 0[i-1]/dt
v_b = (np.roll(th_d,1) - np.roll(th_d,-1))*30

arrow1 = patches.Arrow(x3[0],y3[0],0,0)
arrow2 = patches.Arrow(x3[0],y3[0],0,0)
arrow3 = patches.Arrow(x3[0],y3[0],0,0)
ang_text = ax.text(0.5, 0.1, '', transform=ax.transAxes)

#==============================================================================
# Animating
#==============================================================================
#Initialize lines and patches
def init():
    line.set_data([], [])
    ax.add_patch(patch1)
    ax.add_patch(patch2)
    ax.add_patch(patch4)
    
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    ax.add_patch(arrow3)
    ang_text.set_text('')
    return line, ang_text
    
#Animate
def animate(i):
    #This uses global angles in degrees
    global th_a_d,patch1
    global th_b_d,patch2
    global th_d_d,patch4
    
    global arrow1,arrow2,arrow3,len_arrow
    #This draws the linkages
    thisx = [x1, x2[i],x3[i],x4]
    thisy = [y1, y2[i],y3[i],y4]
    line.set_data(thisx, thisy)
    
    #This draws the angles
    ax.patches.remove(patch1)
    patch1= patches.Arc((x1,y1),100,100,0,0,th_a_d[i],color='r')
    ax.add_patch(patch1)
    
    ax.patches.remove(patch2)
    patch2= patches.Arc((x2[i],y2[i]),100,100,0,0,th_b_d[i],color='g')
    ax.add_patch(patch2)
    
    ax.patches.remove(patch4)
    patch4 = patches.Arc((x4,y4),100,100,0,0,th_d_d[i],color = 'b')
    ax.add_patch(patch4)
    
    #Draws tangential component
#    ax.patches.remove(arrow1)
#    arrow1 = patches.Arrow(x3[i],y3[i]
#                           ,len_arrow*v_b[i]*(np.cos(th_d[i]-th_b[i])*
#np.cos(np.pi + th_b[i] - th_d[i]) + np.sin(th_d[i]-th_b[i])*np.sin(np.pi + th_b[i] - th_d[i]))
#                           ,len_arrow*v_b[i]*(np.sin(th_d[i]-th_b[i])*
#np.cos(np.pi + th_b[i] - th_d[i]) - np.cos(th_d[i]-th_b[i])*np.sin(np.pi + th_b[i] - 
#th_d[i]))
#                           ,width = 20,color = 'y')
#    ax.add_patch(arrow1)
    #Draws radial component
    
    ax.patches.remove(arrow3)
    arrow3 = patches.Arrow(x3[i],y3[i],
                           len_arrow*np.cos(th_b[i])*v_b[i]*np.cos(np.pi + th_b[i]- th_d[i])
                           ,len_arrow*np.sin(th_b[i])*v_b[i]*np.cos(np.pi + th_b[i]- th_d[i])
                           ,width = 20,color = 'y')
    ax.add_patch(arrow3)
    
    #Draws actual component
    ax.patches.remove(arrow2)
    arrow2 = patches.Arrow(x3[i],y3[i],
                           len_arrow*np.cos(th_b[i])*v_b[i]
                           ,len_arrow*np.sin(th_b[i])*v_b[i]
                           ,width = 20,color = 'y')
    ax.add_patch(arrow2)
    
    #This displays the angles
#    ax.text(x1,y1)
    text = \
    'Angle1 (red): ' + str(round(th_a_d[i],2)) + '\n' + \
    'Angle2 (green): ' + str(round(th_b_d[i],2)) + '\n' + \
    'Angle4 (blue): ' + str(round(th_d_d[i],2)) + '\n' + \
    'Speed(yellow): ' + str(round(v_b[i],2)) + '\n'
    ang_text.set_text(text)
    
    return line, patch1,patch2,patch4,ang_text,arrow2,#arrow3,arrow1
    pass

sys.exit()
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y2)),
                              interval=30, blit=True, init_func=init)
#Save animation
Writer = animation.writers['ffmpeg']
writer = Writer(fps = 30,extra_args=['-vcodec', 'libx264'],bitrate = 3000)
dpi = 100

#ani.save('four_bar_linkage.mp4', writer = writer,dpi = dpi)
plt.show()