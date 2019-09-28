

# 做一个统计模型  统计 极端天气出现的次数, 用于说明极端天气的出现和气候变化有关系  
#全球变暖  
# 统计次数，频率， 百分比  

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


# 统计极端天气
#统计偏差
findid = low.copy(deep = True)

findid['year'] = [1990 + i for i in low.index]




mintemp = findid['MinMinTemp'].values

mintemplist = [0]

for i in range(len(mintemp)-1):
    mintemplist.append(mintemp[i+1]-mintemp[i])
findid['det'] = mintemplist    
dis1 = findid.loc[findid.year <2004]

dis2 = findid.loc[(findid.year >=2004)&(findid.year<2018)]
result = []
result.append(len(dis1.loc[dis1.det <-2]))
result.append(len(dis2.loc[dis2.det <-2]))


#统计每个区域最低温度在三个阶段中出现负值大于多少的次数

def findcount(x):
    findid = x.copy(deep = True)
    findid['year'] = [1990 + i for i in low.index]
    mintemp = findid['MinMinTemp'].values
    mintemplist = [0]
    for i in range(len(mintemp)-1):
        mintemplist.append(mintemp[i+1]-mintemp[i])
    findid['det'] = mintemplist    
    dis1 = findid.loc[findid.year <2004]
    
    dis2 = findid.loc[(findid.year >=2004)&(findid.year<2018)]
    result = []
    result.append(len(dis1.loc[dis1.det <-2]))
    result.append(len(dis2.loc[dis2.det <-2]))  
    return result

result = []
for i in [bc,yt,nu,qc,sk,ab,ns,nb,mb,on,low]:
    result.append(findcount(i))
ttt = pd.DataFrame(result,columns = ['before','after'])
ttt['det'] = ttt.after - ttt.before #总共出现的次数 
sum1 = ttt.det.sum()
ttt['rate'] = ttt.det/ttt.after

ttt.rate.sum()
rate = len(ttt.loc[ttt.det > 0]) /len(ttt)

#计算两个区域内  降的均值的上升率：
def findrate(x):
    findid = x.copy(deep = True)
    findid['year'] = [1990 + i for i in low.index]
    mintemp = findid['MinMinTemp'].values
    mintemplist = [0]
    for i in range(len(mintemp)-1):
        mintemplist.append(mintemp[i+1]-mintemp[i])
    findid['det'] = mintemplist    
    dis1 = findid.loc[findid.year <2004]
    dis2 = findid.loc[(findid.year >=2004)&(findid.year<2018)]
    result = []
    result.append(dis1.loc[dis1.det <0].MinMinTemp.mean())
    result.append(dis2.loc[dis2.det <0].MinMinTemp.mean())  
    return result

#
result2 = []
for i in [bc,yt,nu,qc,sk,ab,ns,nb,mb,on,low]:
    result2.append(findrate(i))


