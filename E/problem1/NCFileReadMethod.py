# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:48:39 2019

@author: Gupeng
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

nc_obj=Dataset('sst.wkmean.1990-present.nc')
#读取数据值
lat=(nc_obj.variables['lat'][:])
lon=(nc_obj.variables['lon'][:])
sst=(nc_obj.variables['sst'][:])
times=(nc_obj.variables['time'][:])
time_bnds=(nc_obj.variables['time_bnds'][:])

location_canada_west = sst[:,55,-138]
location_canada_east = sst[:,57,-54]

location_indian_west = sst[:,11,71]
location_indian_east = sst[:,13,-84]

def polyfit(x, y, degree):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    results['polynomial'] = coeffs.tolist()
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)
    sstot = np.sum((y - ybar)**2)
    results['determination'] = ssreg / sstot
    return results


def plotdouble(X,Y,name,xlabel,ylabel):
    z1 = polyfit(X, Y,2)
    print(z1)
    z1 = z1['polynomial']
    yxin = [z1[0]*i*i+z1[1]*i+z1[2] for i in X]
    plt.plot(X,rer)  
    plt.plot(X,yxin) 
    plt.title(name) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(['历史曲线','拟合曲线'])
    
ttt = sst[:,77,-172]
windows = 16
rer = []
for i in range(0,len(location_canada_west)-4,16):
    rer.append(np.mean(location_canada_west[i:i+windows]))
X=[i for i in range(len(rer))]
Y=rer

plotdouble(X,Y,'SST时间变化趋势图','t','sst')