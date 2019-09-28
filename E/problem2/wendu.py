

# 地表温度预测模型

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

# 全球地热数据 
landtem = pd.read_csv('GlobalTemperatures.csv')
colm = landtem.columns
landtem['year'] = landtem['dt'].apply(lambda x: x.split('-')[0])
tt = landtem.groupby('year')[colm[1]].agg({'mean_land':'mean'}).reset_index()
tt2 = tt.loc[tt.year.astype(int) >= 1990].reset_index(drop = True)
tt2.plot()

res = polyfit(tt2.index,tt2.mean_land,2)
res = res['polynomial']

plt.plot(tt2.index, tt2.mean_land)
plt.plot(tt2.index, [res[0]*i*i + res[1]*i+res[2] for i in tt2.index])
#[-0.0006504146316646084, 0.043644924196173746, 8.985933608058609]


#全球地热数据和温度的关系  
fig, ax1 = plt.subplots()
ax1.plot([1990+i for i in range(len(low['MinMinTemp']))],low['MinMinTemp'])
ax1.set_xlabel('时间')
ax1.set_ylabel('平均最低温度')
ax1.legend(['年最低温度'])
ax2 = ax1.twinx()
ax2.plot([1990 + i for i in tt2.index], tt2.mean_land,color = 'r')
ax2.set_ylabel('地热数据')
ax2.legend(['land'])





################################################################################################
#########                              北美洲 三种模型预测                          ##################
###############################################################################################
#加拿大的地热数据 北美洲地热数据 
landtem = pd.read_csv('GlobalLandTemperaturesByState.csv')
landtem = landtem[landtem.Country =='Canada']
landtem['year'] = landtem['dt'].apply(lambda x: x.split('-')[0])
landtem1 = landtem.loc[landtem.year.astype(int) >= 1990]
#landtem1 = landtem1.loc[landtem1.State == 'Alberta'] 
#ab找出最低温:

tt = landtem1.groupby('year')[landtem1.columns[1]].agg({'MinTem':'min','MaxTem':'max',
                'MeanTem':'mean'})
fig, ax1 = plt.subplots()
ax1.plot([1990+i for i in range(len(low['MinMinTemp']))],low['MinMinTemp'])
ax1.set_xlabel('时间') 
ax1.set_ylabel('平均最低温度')
ax1.legend(['年最低温度'],loc = 'upper left')
ax2 = ax1.twinx()
ax2.plot(tt.index.astype(int), tt['MinTem'],color = 'r')
ax2.set_ylabel('地热数据')
ax2.legend(['land'])

res = polyfit([i - 1990 for i in tt.index.astype(int)],tt['MinTem'],2)['polynomial']
plt.plot([i for i in tt.index.astype(int)],tt['MinTem'])
plt.plot([i for i in tt.index.astype(int)], [res[0]*i*i + res[1]*i+res[2] for i in [i - 1990 for i in tt.index.astype(int)]])
plt.legend(['北美洲最低温度'])
plt.xlabel('时间')
plt.ylabel('温度')

#[-0.004744648829431388, 0.2968625752508359, -34.316425384615385]
def lanfunc(x):
    return  (res[0]+0.001)*x*x + res[1]*x+res[2]
lanfunc(45)
import random 
result = []

################################ 地热模型
for i in range(25,50):
    result.append(lanfunc(i)+random.uniform(-1,1))  
plt.plot([i +2020 for i in range(len(result))],result)
plt.title('陆面温度模型')
plt.xlabel('时间')
plt.ylabel('预测温度')


#二氧化碳浓度预测模型 


#吸热放热  二氧化碳的浓度 对 温度的影响 
#carbon = pd.read_csv('global.1751_2014.xlsx')

import pandas as pd
carbon = pd.read_csv('archive.csv')
carbon = carbon.loc[carbon.Year > 1989]
tt = carbon.groupby('Year')['Carbon Dioxide (ppm)'].agg({'MaxCar':'max','MinCar':'min',
              'SumCar':'sum','MeanCar':'mean'})

#temp = carbon['Carbon Dioxide (ppm)']

#for i in range(len(temp)):
        
X = [ i - 1990 for i in tt.index]

Y = tt.MeanCar

res = polyfit(X,Y,1)['polynomial']


########################   二氧化碳浓度模型
result2 = [ 0.56*(0.1464*i +random.uniform(-0.2,0.2)) for i in range(25)]



fig, ax1 = plt.subplots()
ax1.plot([1990+i for i in range(len(low['MinMinTemp']))],low['MinMinTemp'])
ax1.set_xlabel('时间') 
ax1.set_ylabel('平均最低温度')
ax1.legend(['年最低温度'])
ax2 = ax1.twinx()
ax2.plot([i+1990 for i in X],Y,color = 'r')
ax2.set_ylabel('二氧化碳的浓度')
ax2.legend(['carbon'])

#二氧化碳的浓度估值
plt.plot([2020+i for i in range(len(result2))],result2)
plt.title('全球吸放热与温度修正关系图')
plt.legend(['修正值'])
plt.xlabel('时间')
plt.ylabel('温度')
#0.06

#海洋表面预测模型：


#海洋温度具有周期性 
t = selectpoint(90 - 55,-138+180)
tt = t.groupby('year')['temp'].agg({'tempmean':'mean'})
plt.legend(['东太平洋海洋'])
plt.title('东太平洋SST')
plt.xlabel('时间')
plt.ylabel('SST')
plt.plot(tt.index[:-1],tt.values[:-1])

#海洋与温度的变化
fig, ax1 = plt.subplots()
ax1.plot([1990+i for i in range(len(bc['MinMinTemp']))],bc['MinMinTemp'])
ax1.set_xlabel('时间') 
ax1.set_ylabel('平均最低温度')
ax1.legend(['年最低温度'])
ax2 = ax1.twinx()
ax2.plot(tt.index[:-1],tt.values[:-1],color='r')
ax2.set_ylabel('海洋温度')
ax2.legend(['海洋温度'])


#线性模型和周期模型的叠加：
#1. 线性海洋模型:

result31_seamodel = [ 0.0152*i +random.uniform(-0.01,0.01) for i in range(25)]

result31_sea2tem = [i*8 for i in result31_seamodel]#线性模型  海洋对温度的影响
plt.plot([2020+i for i in range(len(result31_sea2tem))],result31_sea2tem)
plt.title('SST线性预估模型')
plt.xlabel('时间')
plt.ylabel('温度修正')
plt.legend(['修正曲线'])
# 25年的周期性海洋模型对未来的影响
#前10年  4年一个周期

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


seares2 = []
for i in range(len(result_32)):
    seares2.append(result31_seamodel[i] + result_32[i])


#plt.plot([2020 + i for i in range(len(seares2))],seares2)
plt.plot([2020 + i for i in range(len(seares2))],seares2)
plt.title('海洋周期图像')
plt.xlabel('时间')
plt.ylabel('温度')
plt.legend(['预测曲线'])


#海洋周期对温度的影响
temp = [0]
for i in range(len(result_32)-1):
    temp.extend(result_32[i+1] - result_32[i])
resuult3 = [i*9 +random.uniform(-1,1) for i in temp]    

seares = []
for i in range(len(resuult3)):
    seares.append(resuult3[i] + result31_sea2tem[i])
plt.plot([2020+i for i in range(len(seares))],seares)
plt.title('海洋周期对温度的影响')
plt.xlabel('时间')
plt.ylabel('温度')
plt.legend(['预测曲线'])

total = []
for i in range(25):
    total.append(result[i]+0.2*result2[i]+seares[i])
  
    
    
#plt.plot([1990+i for i in range(len(low['MinMinTemp']))],low['MinMinTemp'])
plt.plot([2020+i for i in range(len(total))],total)
plt.title('北美洲最低温度预测')
plt.xlabel('时间')
plt.ylabel('温度')
plt.legend(['预测曲线'])

