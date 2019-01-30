# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:31:29 2019

@author: John
"""
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class inter_anim():
    def __init__(self):
        self.labels='A','k','v',
        self.frontend()
        pass
    def frontend(self):
        #Main window
        root = tk.Tk()
        root.title('Interactive sine wave')
        #Create frames in main window
        f1=tk.Frame(root)
        f2=tk.Frame(root)
        f2_1=tk.Frame(f2)
        f2_2=tk.Frame(f2)   
        f1.pack(side='left')
        f2.pack(side='left')
        f2_1.pack(side='top')
        f2_2.pack(side='top')
        #Create figure canvas
        self.fig = plt.Figure()        
        canvas = FigureCanvasTkAgg(self.fig, master=f1)
        canvas.get_tk_widget().grid(column=0,row=1)
        
        #Create grid entry boxes
        l0=tk.Label(f2_1,text='|A|sin(kx+vt)')
        l0.grid(row=0)
        self.grid_label_entry_button(f2_1,self.labels)

        self.A=self.grids['A']['DoubleVar'].get()
        self.k=self.grids['k']['DoubleVar'].get()
        self.v=self.grids['v']['DoubleVar'].get()
        
        #Driver of animation
        x = np.arange(0, 2*np.pi, 0.01)        # x-array
        self.draw_anim(x)
        
        #Create buttons to control animation
        self.t=tk.StringVar()
        self.t.set('t=0.0')
        self.t_label=tk.Label(f2_2,textvariable=self.t)
        self.t_label.pack(side='top')
        b1=tk.Button(f2_2,text='Start animation',command=self.start_anim)
        b2=tk.Button(f2_2,text='Stop animation',command=self.stop_anim)
        b3=tk.Button(f2_2,text='Create new animation',command=lambda:self.redraw_anim(x))
        b1.pack(side='top')
        b2.pack(side='top')
        b3.pack(side='top')
        
        #Execute GUI program
        tk.mainloop()
        
    def stop_anim(self):
        self.anim.event_source.stop()
    def start_anim(self):
        self.anim.event_source.start()
    def func_anim(self,i,x,line,t_text):
        #Repeated function call for animation
        line.set_ydata(self.A*np.sin(self.k*x+self.v*i))  # update the data
        self.t.set('t={:.3f}'.format(i))
        return line,
    
    def grid_label_entry_button(self,frame,labels):
        #Creates grid for entry boxes
        self.grids={}
        for i,label in enumerate(labels):
            va = tk.DoubleVar()
            va.set(1.0)
            la = tk.Label(frame, text=label)
            en = tk.Entry(frame, textvariable=va,width=10)
            #bt = tk.Button(frame, text='Button {}'.format(i))
            
            la.grid(row=i,column=1)
            en.grid(row=i,column=2)
            #bt.grid(row=i,column=3)
            
            self.grids[label]={'DoubleVar':va,'Entry':en}#,'Button':bt}
            
    def redraw_anim(self,x):
        
        self.fig.delaxes(self.ax)
        self.A=self.grids['A']['DoubleVar'].get()
        self.k=self.grids['k']['DoubleVar'].get()
        self.v=self.grids['v']['DoubleVar'].get()
        self.draw_anim(x)
        
    def draw_anim(self,x):
        self.ax = self.fig.add_subplot(111)
        self.t_text=self.ax.text(x=1,y=1,s='')
        self.line, = self.ax.plot(x, self.A*np.sin(self.k*x))
        self.anim = animation.FuncAnimation(self.fig, self.func_anim, frames=np.arange(0,10,0.1),fargs=(x,self.line,self.t_text), interval=25, blit=False)
if __name__=='__main__': 
    my=inter_anim()