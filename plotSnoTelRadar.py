#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 09:47:25 2017

@author: hpm
"""

# this script will create a nice plot, after running:
# loadBannerSummit.py and readFEradarSat.py
import matplotlib
matplotlib.rcParams['figure.figsize']
fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
plt.subplot(211)
t=df.index
Tair=(df['AIR TEMPERATURE OBSERVED']-32.0)*5/9.0
T0=np.zeros(np.size(df.index))
lines=plt.plot(t,T0,t,Tair)
plt.setp(lines, linewidth=2.0)
plt.subplot(212)
SWEsnotel=df['SNOW WATER EQUIVALENT']*2.54
Ix2=df['PRECIPITATION ACCUMULATION']*2.54<30
Psnotel=df[Ix2]['PRECIPITATION ACCUMULATION']*2.54-7
Ix=np.logical_and(DFall['density']<1,DFall['depth']<1)
t2=DFall.index[Ix]
SWEradar=DFall[Ix]['SWE1']*100-5.5
plt.plot(t,SWEsnotel,t[Ix2],Psnotel,t2,SWEradar)
plt.gcf().autofmt_xdate()
plt.show()







plt.show()

