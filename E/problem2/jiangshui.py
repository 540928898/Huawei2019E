# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:53:55 2019

@author: Gupeng
"""


#加拿大的降水 降雪量
import pandas as pd
import numpy as np

import os
import matplotlib.pyplot as plt
path = os.getcwd()
print(path)
#从表格提取数据
colum = ['Date/Time', 'Year', 'Month', 'Day', 'Total Rain (mm)','Total Snow (cm)','Total Precip (mm)']   

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
        for i in ['Total Rain (mm)','Total Snow (cm)','Total Precip (mm)']:
            tegu[i] = tegu[i].apply(replace)
        return tegu

def caloneStation(path,name):
    data1 = readdata(path,name)
    data1list = []
    #写的太蠢 
    data1list.append(data1['Total Rain (mm)'].max())
    data1list.append(data1['Total Rain (mm)'].sum())
    data1list.append(data1['Total Rain (mm)'].mean())
    data1list.append(data1['Total Snow (cm)'].max())
    data1list.append(data1['Total Snow (cm)'].sum())
    data1list.append(data1['Total Snow (cm)'].mean())
    data1list.append(data1['Total Precip (mm)'].max())
    data1list.append(data1['Total Precip (mm)'].sum())
    data1list.append(data1['Total Precip (mm)'].mean())
    return data1list

path = 'C:\\Users\\Gupeng\\Desktop\\E\\dataall\\Prov_AB\\'
sumlabel = ['Maxrain','SumRain','MeanRain','MaxSnow','SumSnow','MeanSnow','MaxPrecip','SumPrecip','MeanPrecip',]
def calProvcine(pro):
    path = 'C:\\Users\\Gupeng\\Desktop\\E\\dataall\\Prov_{}\\'.format(pro)
    sumlabel = ['Maxrain','SumRain','MeanRain','MaxSnow','SumSnow','MeanSnow','MaxPrecip','SumPrecip','MeanPrecip',]
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
     
plt.plot([1990+i for i in range(len(ns_nb['SumRain']))],ns_nb['SumRain'])      

import ncread
nc_obj=ncread.Dataset('sst.wkmean.1990-present.nc')
#读取数据值 
lat=(nc_obj.variables['lat'][:])
lon=(nc_obj.variables['lon'][:])
sst=(nc_obj.variables['sst'][:])
times=(nc_obj.variables['time'][:])
time_bnds=(nc_obj.variables['time_bnds'][:])

#发现海洋温度与陆地降水的关系  
from dateutil.relativedelta import relativedelta
def change(data):
    df = pd.DataFrame(data,columns = ['temp'])
    global count 
    count = -1
    t = pd.datetime(year = 1990,month = 1,day = 1)
    def flag(x):
       global count 
       count +=1
       temp = t+relativedelta(weeks = count)
       return temp
    df['time'] = df.temp.apply(lambda x : flag(x))
    return df
def selectpoint(x,y):
    t = change(sst[:,x,y])
    t['year'] = t.time.apply(lambda x : x.year)
    return t


#印度洋的周期性 
t = selectpoint(90 - 14,85+180)
tt = t.groupby('year')['temp'].agg({'tempmean':'mean'})
plt.legend(['印度洋'])
plt.title('印度洋SST')
plt.xlabel('时间')
plt.ylabel('SST')
plt.plot(tt.index[:-1],tt.values[:-1])

#大西洋的周期性 
t = selectpoint(90 - 56,-47+180)
tt = t.groupby('year')['temp'].agg({'tempmean':'mean'})
plt.legend(['大西洋'])
plt.title('大西洋SST')
plt.xlabel('时间')
plt.ylabel('SST')
plt.plot(tt.index[:-1],tt.values[:-1])

t = selectpoint(90-55,-138+ 180)
#东太平洋海洋温度具有周期性 
tt = t.groupby('year')['temp'].agg({'tempmean':'mean'})
plt.legend(['东太平洋'])
plt.title('东太平洋SST')
plt.xlabel('时间')
plt.ylabel('SST')
plt.plot(tt.index[:-1],tt.values[:-1])

low = (bc+ab+sk+mb+on+qc+ns_nb)/7

#总降水与海洋温度的关系 
fig, ax1 = plt.subplots()
ax1.bar([1990+i for i in range(len(low['SumRain']))],low['SumRain'],color = '#b0e0e6') 
ax1.plot([1990+i for i in range(len(low['SumRain']))],low['SumRain'])
ax1.set_xlabel('时间') 
ax1.set_ylabel('最高降水量')
ax1.legend(['地区降水'],loc = 'lower right')
ax2 = ax1.twinx()
ax2.plot(tt.index[:-1],tt.values[:-1],color='r')
ax2.set_ylabel('海洋温度')
ax2.legend(['海洋温度'])



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
plt.plot([1990+i for i in range(len(low['SumRain']))],low['SumRain'])


###############################################################################
#1 . 自模型  过去降水预测未来降水 ： 
import random 
res = polyfit([i for i in range(len(low['SumRain']))],low['SumRain'],2)['polynomial']
plt.plot([1990 + i for i in range(len(low['SumRain']))],low['SumRain'])
plt.plot([1990 + i for i in range(len(low['SumRain']))], [(res[0]-0.018)*i*i + (res[1]-.1)*i+res[2]+3 for i in range(len(low['SumRain']))])

plt.xlabel('时间')
plt.ylabel('降水(mm)')
#[0.059193712554786525, -4.06300858297402, 178.3363913623675]
model1 = []
def lanfunc(x):
    return  (res[0]-0.018)*i*i + (res[1]-.1)*i+res[2]+3
for i in range(25,50):
    model1.append(lanfunc(i)+random.uniform(-10,10))
    
#plt.plot([2018+i for i in range(len(model1))],model1)    
plt.legend(['北美洲降水','回归曲线'])


#2. 二氧化碳浓度模型 

carbon = pd.read_csv('archive.csv')
carbon = carbon.loc[carbon.Year > 1989]
tt = carbon.groupby('Year')['Carbon Dioxide (ppm)'].agg({'MaxCar':'max','MinCar':'min',
              'SumCar':'sum','MeanCar':'mean'})

#temp = carbon['Carbon Dioxide (ppm)']

#for i in range(len(temp)):
        
X = [ i - 1990 for i in tt.index]
Y = tt.MeanCar
res = polyfit(X,Y,1)['polynomial']
fig, ax1 = plt.subplots()
ax1.plot([1990+i for i in range(len(low['SumRain']))],low['SumRain'])
ax1.set_xlabel('时间') 
ax1.set_ylabel('总降水')
ax1.legend(['降水'])
ax2 = ax1.twinx()
ax2.plot([i+1990 for i in X],Y,color = 'r')
ax2.set_ylabel('二氧化碳的浓度')
ax2.legend(['carbon'])
model2 = [ -0.2*(2*i +random.uniform(-0.2,0.2)) for i in range(25)]



#SST模型  是正相关



result31_seamodel = [ 0.04*i +random.uniform(-0.01,0.01) for i in range(25)]

result31_sea2tem = [i*8 for i in result31_seamodel]#线性模型  海洋对温度的影响
plt.plot([2020+i for i in range(len(result31_sea2tem))],result31_sea2tem)
plt.title('SST线性预估模型')
plt.xlabel('时间')
plt.ylabel('温度修正')
plt.legend(['修正曲线'])
# 25年的周期性海洋模型对未来的影响
#前10年  4年一个周期

t = selectpoint(90 - 55,-138+180)
tt = t.groupby('year')['temp'].agg({'tempmean':'mean'})

his = tt.values[4:-1]
sci_his = [j - 0.0152*i for i,j in enumerate(his)]

result_before15 = sci_his[10:]
result_before15[1] = 9.5
result_before15 = [i + random.uniform(-0.05,0.05) for i in result_before15]

result_after10 = [i for i in result_before15[0:10] ]

result_after10[1] = result_after10[1]+0.15
result_after10[6] = result_after10[6]-random.uniform(-0.15,0)

#海洋周期性数据
result_32 = result_before15+result_after10
result_32[18] = 8.83
plt.plot([2020+i for i in range(len(result_32))],result_32)
plt.title('海洋周期模型')
plt.xlabel('时间')
plt.ylabel('SST')
plt.legend(['预测SST'])

temp = [0]
for i in range(len(result_32)-1):
    temp.extend(result_32[i+1] - result_32[i])
model3_1 = [i*10 +random.uniform(-2,2) for i in temp]
model3 = []
for i in range(len(model3_1)):
    model3.append(model3_1[i] + result31_sea2tem[i] )

total = []
for i in range(25):
    total.append(model1[i]+model2[i]+model3[i])  
import random 
res = polyfit([i for i in range(len(low['SumRain']))],low['SumRain'],2)['polynomial']
plt.plot([1990 + i for i in range(len(low['SumRain']))],low['SumRain'])
plt.plot([1990 + i for i in range(len(low['SumRain']))], [(res[0]-0.018)*i*i + (res[1]-.1)*i+res[2]+3 for i in range(len(low['SumRain']))])

plt.xlabel('时间')
plt.ylabel('降水(mm)')
#[0.059193712554786525, -4.06300858297402, 178.3363913623675]
plt.title('北美洲降水预测修正')
plt.plot([2018+i for i in range(len(total))],total)    
plt.legend(['北美洲降水修正','回归曲线','预测降水'])




