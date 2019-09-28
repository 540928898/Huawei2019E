   # -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 19:40:48 2019

@author: Gupeng
"""

import pandas as pd
import numpy as np

import os
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = os.getcwd()
print(path)
#从表格提取数据
colum = ['Date/Time', 'Year', 'Month', 'Day', 'Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)', 'Total Rain (mm)']   

datalist = os.listdir(path+'\\data1')
citydic = {}
#获取城市列表
for i in datalist:
    if i[:-8] not in citydic:
        citydic[i[:-8]]  = 0
    citydic[i[:-8]] += 1
    
def replace(x):
    try :
        return float(x)
    except ValueError:
        return np.nan 
    
def readdata(path,name):
    with open(path + name, encoding='utf-8') as data_obj:
        line = data_obj.readline()
        data = [[],[],[]]
        count = 0
        while(line != ''):    
            if len(line) == 1:
                count +=1
                line = data_obj.readline()
                continue
            data[count].append(line.split(','))
            line = data_obj.readline()
        temp = data[2][1:]
        df_temp = pd.DataFrame(temp,columns = data[2][0])
        df_temp.columns = [i[1:-1] for i in df_temp.columns]
        for i in df_temp.columns :
            df_temp[i] = df_temp[i].apply(lambda x: x[1:-1])
        tegu = df_temp[colum].copy(deep =True)
        for i in ['Max Temp (°C)','Min Temp (°C)','Mean Temp (°C)', 'Total Rain (mm)']:
            tegu[i] = tegu[i].apply(replace)
        return tegu
     
def caloneStation(path,name):
    data1 = readdata(path,name)
    data1list = []
    #写的太蠢 
    data1list.append(data1['Max Temp (°C)'].max())
    data1list.append(data1['Max Temp (°C)'].min())
    data1list.append(data1['Max Temp (°C)'].mean())
    data1list.append(data1['Min Temp (°C)'].max())
    data1list.append(data1['Min Temp (°C)'].min())
    data1list.append(data1['Min Temp (°C)'].mean())
    data1list.append(data1['Mean Temp (°C)'].max())
    data1list.append(data1['Mean Temp (°C)'].min())
    data1list.append(data1['Mean Temp (°C)'].mean())
    return data1list

path = 'C:\\Users\\Gupeng\\Desktop\\E\\dataall\\Prov_AB\\'
sumlabel = ['MaxMaxTemp','MinMaxTemp','MeanMaxTemp','MaxMinTemp','MinMinTemp','MeanMinTemp','MaxMeanTemp','MinMeanTemp','MeanMeanTemp',]

#省份的计算
def calProvcine(pro):
    path = 'C:\\Users\\Gupeng\\Desktop\\E\\dataall\\Prov_{}\\'.format(pro)
    sumlabel = ['MaxMaxTemp','MinMaxTemp','MeanMaxTemp','MaxMinTemp','MinMinTemp','MeanMinTemp','MaxMeanTemp','MinMeanTemp','MeanMeanTemp',]
    result = []
    for year in range(1990,2019,1):
        print(year)
        listyear =[]
        datalist = [i for i in os.listdir(path) if str(year) in i]
        for stn in datalist:
            listyear.append(caloneStation(path,stn))
        result.append(pd.DataFrame(listyear,columns = sumlabel).mean().values.reshape(1,9)[0])    
    df_result = pd.DataFrame(result,columns = sumlabel)
    return df_result


bc = calProvcine('BC')
yt = calProvcine('YT')
nu = calProvcine('NU')
qc = calProvcine('QC')
sk = calProvcine('SK')
ab = calProvcine('AB')
ns = calProvcine('NS')
nb = calProvcine('NB')
mb = calProvcine('MB')
on = calProvcine('ON')

ns_nb = (ns+nb)/2
low = (bc+ab+sk+mb+on+qc+ns_nb)/7
from scipy.optimize import curve_fit
def f_fit(x, a, b, c):
    return a*x**2+b*x+c



##最高AB温度的时间特性 
tt = ab['MaxMaxTemp'].copy(deep = True).values
windows = 4
rer = []
for i in range(len(tt)-1):
    rer.append(np.mean(tt[i:i+windows]))
X = [i for i in range(len(rer))]
Y = rer
yxin = [0.003*i*i-0.008*i+31 for i in X]
plt.plot([i+ 1990 for i in X],Y)    
plt.plot([i+ 1990 for i in X],yxin)
plt.title('太平洋沿海城市AB最高温度时间趋势图') 
plt.xlabel('时间')
plt.ylabel('年最高温度')
plt.legend(['历史曲线','拟合曲线'])
 
#AB的平均气温
tt = ab['MeanMeanTemp'].copy(deep = True).values
plt.plot([i+ 1990 for i in range(len(tt))],tt)
plt.title('太平洋沿海城市AB平均温度时间趋势图') 
plt.xlabel('时间')
plt.ylabel('年平均温度')
plt.legend(['历史曲线'])


##最低AB温度的时间特性 
tt = ab['MinMinTemp'].copy(deep = True).values
windows = 4
rer = []
for i in range(len(tt)-windows):
    rer.append(np.mean(tt[i:i+windows]))
X = [i for i in range(len(rer))]
Y = rer
yxin = [0.003*i*i-0.13*i-33 for i in X]
plt.plot([i+ 1992 for i in X],Y)    
plt.plot([i+ 1992 for i in X],yxin)
plt.title('太平洋沿海城市AB最低温度时间趋势图') 
plt.xlabel('时间')
plt.ylabel('年最低温度')
plt.legend(['历史曲线','拟合曲线'])
 

## 最小温度的空间特性  
plt.plot([1990+i for i in range(len(nu['MinMinTemp']))],nu['MinMinTemp'])      
plt.plot([1990+i for i in range(len(bc['MinMinTemp']))],bc['MinMinTemp'])  
plt.plot([1990+i for i in range(len(ns_nb['MinMinTemp']))],ns_nb['MinMinTemp']) 
plt.plot([1990+i for i in range(len(ab['MinMinTemp']))],ab['MinMinTemp'])  
plt.plot([1990+i for i in range(len(qc['MinMinTemp']))],qc['MinMinTemp']) 
plt.plot([1990+i for i in range(len(sk['MinMinTemp']))],sk['MinMinTemp'])  
plt.legend(['nu','bc','ns_nb','ab','qc','sk'])
plt.title('加拿大最低温度时空对比') 
plt.xlabel('时间')
plt.ylabel('最低温度变化')

## 最高温度的空间特性  
plt.plot([1990+i for i in range(len(nu['MaxMaxTemp']))],nu['MaxMaxTemp'])      
plt.plot([1990+i for i in range(len(bc['MaxMaxTemp']))],bc['MaxMaxTemp'])  
plt.plot([1990+i for i in range(len(ns_nb['MaxMaxTemp']))],ns_nb['MaxMaxTemp']) 
plt.plot([1990+i for i in range(len(ab['MaxMaxTemp']))],ab['MaxMaxTemp'])  
plt.plot([1990+i for i in range(len(qc['MaxMaxTemp']))],qc['MaxMaxTemp']) 
plt.plot([1990+i for i in range(len(sk['MaxMaxTemp']))],sk['MaxMaxTemp'])  
plt.legend(['nu','bc','ns_nb','ab','qc','sk'])
plt.title('加拿大最高温度时空对比') 
plt.xlabel('时间')
plt.ylabel('最高温度变化')

#需要查询2004年 大事件 最高温度 全部低？？


#计算整个加拿大的低纬度的温度变化 

plt.plot([1990+i for i in range(len(low['MinMinTemp']))],low['MinMinTemp'])   
plt.title('加拿大最低温度整体时间特性') 
plt.xlabel('时间')
plt.ylabel('最低温度变化')
plt.legend(['历史曲线','拟合曲线'])
plt.plot([1990+i for i in range(len(low['MeanMeanTemp']))],low['MeanMeanTemp'])   
plt.plot([1990+i for i in range(len(low['MaxMaxTemp']))],low['MaxMaxTemp'])   

#excel 的 热力图
exceltemp = pd.read_excel('cityupdate.xlsx')

exceltemp.groupby('Prov')

def countStn(x,year):
    path = 'C:\\Users\\Gupeng\\Desktop\\E\\dataall\\Prov_{}\\'.format(x[3])
    datalist = [i for i in os.listdir(path) if x[0] in i]
    sumlabel = ['MaxMaxTemp','MinMaxTemp','MeanMaxTemp','MaxMinTemp','MinMinTemp','MeanMinTemp','MaxMeanTemp','MinMeanTemp','MeanMeanTemp',]
    if len(datalist) == 0:
        return np.nan
    data_listtmp = [i for i in datalist if str(year) in i]
    temp = []
    for k in data_listtmp:
        temp.append(caloneStation(path,k))
    return pd.DataFrame(temp,columns = sumlabel).mean().values.reshape(1,9)  

tt = bc['MinMinTemp'].copy(deep = True).values
windows = 4
rer = []
for i in range(len(tt)-windows):
    rer.append(np.mean(tt[i:i+windows]))
X = [i for i in range(len(rer))]
Y = rer
#yxin = [0.003*i*i-0.13*i-33 for i in X]
plt.plot([i+ 1992 for i in X],Y)    
#plt.plot([i+ 1992 for i in X],yxin)
plt.title('太平洋沿海城市BC最低温度时间趋势图') 
plt.xlabel('时间')
plt.ylabel('年最低温度')
plt.legend(['历史曲线','拟合曲线'])
