#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 22:37:34 2017

This python code loads FE radar data that was processed onboard and sent via sat modem.

@author: hpm
"""
#from IPython import get_ipython
#get_ipython().magic('reset -sf')

from climata.snotel import StationHourlyDataIO
import pandas as pd
import glob
import numpy as np
import os
import time
#import plotly.plotly as py
import matplotlib
# matplotlib.use('Agg')
matplotlib.rcParams['figure.figsize']=[15,12]
import matplotlib.pyplot as plt

#%pylab inline
#pylab.rcParams['figure.figsize'] = (20, 6)
# import cufflinks as cf
#SatDataDir='../SATDATA/10_101_0_42_sky-*' # uncomment this line for use on ice.boisestate.edu
SatDataDir='SatFrom/10_101_0_42_sky-*'
print('Loading all Winter 2017-18 radar data...\n')
DFall=pd.DataFrame({'date': pd.Timestamp('Wed Sept 1 00:00:00 2017'),'depth': pd.Series(0)}) # initialize
DFall=DFall.set_index('date') # set date as index
for filename in glob.glob(SatDataDir): # loop over all pit files
    #print(filename)
    fdate=pd.Timestamp(time.ctime(os.path.getmtime(filename)))
    #print(fdate)
    cnames=['date','time','flag','SWE1','SWE2','depth','LWC','density','Gindex','Sindex','Temp']
    try:
        df=pd.read_csv(filename, header=None, names=cnames)
        df2=pd.DataFrame({'date': fdate,'depth': df['depth'],'SWE1': df['SWE1'],'density': df['density'],'LWC': df['LWC']})
        df2=df2.set_index('date')
        DFall=pd.concat([DFall,df2])   
    except:
        print(filename)
        print('error reading file')
Ix=DFall.index>pd.Timestamp(2017,10,1)
DFall=DFall[Ix]
print(DFall)
# now get the SNotel data
print('loading Snotel data...\n')
params = StationHourlyDataIO(
    station='312:ID:SNTL',
    start_date='2017-10-01',
    end_date='2018-1-31',
    )
tstart=pd.Timestamp(2017,12,1,12)
tstart=tstart.to_pydatetime()
tend=pd.Timestamp(2018,1,31,12)
tend=tend.to_pydatetime()


Pnames=[str(param.element_name) for param in params] # list of parameter names
Pnames.append('DateTime')
df = pd.DataFrame(np.nan, index=[0], columns=Pnames) # initialize pandas data frame
# df=df.set_index('DateTime')
for param in params:
    #print param.element_name
    p=0
    for row in param.data:
        # print "   ", row.datetime, row.value, param.storedunitcd
        df.loc[p,param.element_name]=row.value
        df.loc[p,'DateTime']=pd.to_datetime(row.datetime)
        p=p+1
df=df.set_index('DateTime')
# now plot
print('plotting result...\n')
plt.style.use('ggplot')

print('open new figure with subplots')
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
plt.subplot(221)
t=df.index.to_pydatetime()
Ix9=(t>tstart) & (t<tend)
Tair=(df['AIR TEMPERATURE OBSERVED']-32.0)*5/9.0
T0=np.zeros(np.size(df.index))
lines=plt.plot(t[Ix9],T0[Ix9],t[Ix9],Tair[Ix9])
plt.setp(lines, color='black',linewidth=2.0)
plt.fill_between(t[Ix9],T0[Ix9],Tair[Ix9],where=Tair[Ix9]>0,color='red',alpha='0.5')
plt.fill_between(t[Ix9],T0[Ix9],Tair[Ix9],where=Tair[Ix9]<0,color='blue',alpha='0.5')
plt.ylabel('air temp [deg C]', fontsize=16)
print('plot the second subplot')
plt.subplot(223)
# grab Snotel data and convert
SWEsnotel=df['SNOW WATER EQUIVALENT']*2.54
Ix2=df['PRECIPITATION ACCUMULATION']*2.54<30
Psnotel=df['PRECIPITATION ACCUMULATION']*2.54-14.25
Dsnotel=df['SNOW DEPTH']*2.54
# grab radar data with good values
t2=DFall.index.to_pydatetime()
Ix10=(t2>tstart) & (t2<tend)
print(DFall)
SWEradar=DFall['SWE1']*100-4.39
# define some lines
d0=np.ones(np.size(t))*8.5*2.54*0.25
dL=np.ones(np.size(t))*-7
# Ix3=t<pd.Timestamp(2017,10,31)
# plt.fill_between(t[Ix3],dL[Ix3],d0[Ix3], color='grey', alpha='0.5')
#tRain=pd.Timestamp(2017,11,21,12)
#tRain2=pd.Timestamp(2017,11,28,12)
#tRain=tRain.to_pydatetime()
#tRain2=tRain2.to_pydatetime()
#Ix4=(t>tRain) & (t<tRain2)
#plt.fill_between(t,-7,32,where=Ix4, color='grey',alpha='0.5')
lines=plt.plot(t[Ix9],d0[Ix9],t[Ix9],Dsnotel[Ix9]*0.25,t[Ix9],SWEsnotel[Ix9],t[Ix9],Psnotel[Ix9],t2[Ix10],SWEradar[Ix10])
print('change the line widths')
plt.setp(lines, linewidth=8.0)
plt.setp(lines[0], color='black')
plt.setp(lines[1], linewidth=2.0, color='green')
plt.setp(lines[3], linewidth=2.0, color='cyan')
plt.setp(lines[4], linewidth=4.0,color='red')
#plt.setp(lines[3], color='k')
plt.legend(lines, ['8.5 in min depth req.','SnoTEL depth x 250 kg/m^3','SnoTEL SWE','SnoTEL Cum Precip','Radar SWE'])
plt.gcf().autofmt_xdate()
fig.suptitle('Banner Summit SWEdar', fontsize=20)
plt.xlabel('Water Year 2018', fontsize=16)
plt.ylabel('water equivalent [cm]', fontsize=16)  
A=plt.gca()
z=A.get_xlim()
plt.xlim((z[0],z[1]))
plt.ylim((12,27))
#plt.show
#fig.savefig("BannerSWEdar.png",bbox_inches='tight')


# now plot scatter plot of radar vs SnowTEL SWE and precip during valid periods
print('now interpolate radar to SNOTEL time intervals')
from scipy.interpolate import Rbf
tS=pd.Timestamp(2017,11,1)
tS=tS.to_pydatetime()
tS2=pd.Timestamp(2018,1,31,0)
tS2=tS2.to_pydatetime()
#SWEradar=SWEradar[Ix]
#t2=t2[Ix]
IxS=(t>tS) & (t<tS2)
IxS2=(t2>tS) & (t2<tS2)
tsec=[]
print('change t to seconds since 1970, convert to np.array')
for myt in t:
    tsec.append(time.mktime(myt.timetuple()))
tsec=np.array(tsec) # convert to numpy array
tsec2=[]
print('change t2 to seconds since 1970, convert to np.array')
for myt in t2:
    tsec2.append(time.mktime(myt.timetuple()))
tsec2=np.array(tsec2)
SWEr=np.array(SWEradar)
SWEs=np.array(SWEsnotel)
Ps=np.array(Psnotel)
Ts=np.array(Tair)
Ds=np.array(Dsnotel)
# use radial basis functions
print('radial basis functions')
rbf=Rbf(tsec2[IxS2],SWEr[IxS2],)
SWEr2=rbf(tsec[IxS])
SWEs2=SWEs[IxS]
Ps2=Ps[IxS]
Ts2=Ts[IxS]
Ds2=Ds[IxS]

print('scatter plot')
plt.subplot(222)
plt.plot(range(25),range(25),color='black')
plt.scatter(SWEr2,SWEs2,c=Ts2, cmap='jet')
plt.colorbar()
plt.plot(range(20),range(20),color='black')
plt.suptitle('radar SWE vs SnoTEL SWE, colored by temperature [deg C]', fontsize=20)
plt.xlabel('radar estimated SWE [cm]', fontsize=16)
plt.ylabel('SnoTEL reported hourly SWE [cm]', fontsize=16)
A=plt.gca()
plt.xlim((0,30))
plt.ylim((0,30))



#plt.show()
#fig.savefig("BannerSWEdarScatter.png",bbox_inches='tight')


print('time series of 3 variables')
plt.subplot(224)
tS=pd.Timestamp(2017,11,1)
tS=tS.to_pydatetime()
tS2=pd.Timestamp(2018,1,31,0)
tS2=tS2.to_pydatetime()
#SWEradar=SWEradar[Ix]
#t2=t2[Ix]
IxS=(t>tS) & (t<tS2)
# lets get indicies to the last week
t3=t[IxS]
IxW=tsec[IxS]>(tsec[-1]-(7*24*60*60))
IxW1=np.where(IxW)
IxW1=IxW1[0][0]
# fix the precip
deltaP=Ps2[IxW1]-SWEs2[IxW1] 
#lines=plt.plot(t3[IxW],SWEr2[IxW],t3[IxW],SWEs2[IxW],t3[IxW],Ps2[IxW]-deltaP,t3[IxW],Ds2[IxW]*0.25)
#lines=plt.plot(t[IxS],SWEr2,t[IxS],SWEs2,t[IxS],Ps2,t[IxS],Dsnotel[IxS]*0.25)
lines=plt.plot(t3[IxW],SWEr2[IxW]-SWEr2[IxW1],t3[IxW],SWEs2[IxW]-SWEs2[IxW1],t3[IxW],Ps2[IxW]-Ps2[IxW1],t3[IxW],Ds2[IxW]*0.25-Ds2[IxW1]*0.25)
plt.setp(lines[0], linewidth=6.0, color='red')
plt.setp(lines[1], linewidth=6.0, color='purple')
plt.setp(lines[2], linewidth=4.0,color='cyan')
plt.setp(lines[3], linewidth=4.0,color='green')
plt.legend(lines, ['radar SWE','SnoTEL SWE','SnoTEL precip','SnoTEL depth x 250 kg/m^3'])
plt.suptitle('Banner SWEdar thru: ' + str(t2[-1]) + ' and SnoTEL thru: ' + str(t[-1]), fontsize=16)
plt.xlabel('Water Year 2018', fontsize=16)
plt.ylabel('change in water equivalent [cm]', fontsize=16)
A=plt.gca()
z=A.get_xlim()
z2=A.get_ylim()
plt.xlim((z[0],z[1]))
plt.ylim((z2[0],z2[1]))
plt.gcf().autofmt_xdate()
plt.show()
fig.savefig("BannerSWEdar.png",bbox_inches='tight')
#fig.savefig("BannerSWEdarOct1TS.png",bbox_inches='tight')

# calculate some stats
print('calculate RMSEs and linear regressions')
from scipy.stats import linregress
import math
RMSE=math.sqrt(np.mean(np.square(SWEr2-SWEs2)))
print(RMSE)
RMSE2=math.sqrt(np.mean(np.square(SWEr2-Ps2)))
RMSE3=math.sqrt(np.mean(np.square(SWEs2-Ps2)))
L1=linregress(SWEr2,SWEs2)
L2=linregress(SWEr2,Ps2)


#rbf=Rbf(t[IxS],SWEsnotel[IxS])



    



        
#Ix=np.logical_and(DFall['density']<1,DFall['depth']<1)
#plt.scatter(DFall[Ix]['depth'],DFall[Ix]['density'])
#plt.plot(DFall.index[Ix],DFall[Ix]['SWE1']*100)
