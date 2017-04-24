# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:08:40 2017

@author: John
asdftoger

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


#

a = 25,37.5,50
b= 60,160,180,200,220
c = 50,100,200

d = 200


def grashoff(a,b,c,d):
    q,w,e,r = sorted([a,b,c,d])
    if q + r < w+e:
#        print("a:{},b:{},c:{},d:{}".format(a,b,c,d))
#    
#        print("Grashoff")
        pass
    elif q + r == w+e:
#        print("a:{},b:{},c:{},d:{}".format(a,b,c,d))
#        
#        print("Special grashoff")
        pass
    else:
        print("a:{},b:{},c:{},d:{}".format(a,b,c,d))
        print("Non-Grashoff")
        
        pass
    return None

    pass

for i in a:
    for j in b:
        for k in c:
            grashoff(i,j,k,d)