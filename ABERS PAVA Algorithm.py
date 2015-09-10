# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:25:39 2013

@author: jgenser

Adapted from code by Fabian Pedregosa at :https://github.com/fabianp
His implementation has since been updated to include weighting. 
Andrew Tulloch has updated the implementation to work at 5000x the speed: https://github.com/ajtulloch
"""


temp = "F:/Competition/RMiller-Mizia15798.00-Sunshine/Analysis/NewCOS/JKG/temp/"
out = "F:/Competition/RMiller-Mizia15798.00-Sunshine/Analysis/NewCOS/JKG/output/"
import pandas as pd
import numpy as np




def ABERS(data):
    """
    "data" is an array that contains the 'count' field and the 'vote' field.
    The 'vote' field is the observed sample for which a mean is to be calculated.
    The 'count' field is the weight that corresponds to each 'vote' value. 
    """
    y = np.asarray(data['count'])
    x = np.asarray(data['vote']/data['count'])
    data['pooling']=0
    n_samples = len(y)
    v = x.copy()
    count = y.copy()
    vote = data['vote'].copy()
    
    lvls = np.arange(n_samples)
    lvlsets = np.c_[lvls, lvls, y, x]
    flag = 1
    while flag:
        deriv = np.diff(v)
        if np.all(deriv <=0):
            break
        
        viol = np.where(deriv > 0)[0]
        start = lvlsets[viol[0],0]
        last = lvlsets[viol[0] + 1, 1]
        
        s = 0
        num  = 0
        denom = 0
        for i in range( int(start), int(last) + 1):
            s += v[i]
            num +=vote[i]
            denom +=count[i]
            

        newval = (num*1.0) / (denom*1.0)
        
        for i in range( int(start), int(last) + 1):
            v[i] = newval
            lvlsets[i, 0] = start
            lvlsets[i, 1] = last
            data['pooling']=1

    v = pd.DataFrame(v,columns=['pct'])
    v['count'] = data['count']
    v['bid'] = data['bid']
    v['vote'] = data['vote']
    v['pooling']=data['pooling']
    return v
        
        






