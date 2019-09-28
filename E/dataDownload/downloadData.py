# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 00:00:38 2019

@author: Gupeng
"""


#= 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=1648&Year=1990&Month=8&Day=1&timeframe=2&submit=Download+Data'
import requests 
import re
import os
import pandas as pd
def findStationID(name = "LUTSELK'E A"):
    stationname = name
    stationname = stationname.replace(' ','+')
    stationname = stationname.replace("'", '%27')
    temp1 = 'http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?searchType=stnName&timeframe=1&txtStationName={}&searchMethod=contains&optLimit=yearRange&StartYear=1840&EndYear=2019&Year=1987&Month=7&Day=18&selRowPerPage=25'.format(stationname)
    temp1_data = requests.get(temp1) 
    temp1_data = temp1_data.content.decode('utf-8')
    iter2 = re.finditer('name="StationID" value="\d+"',temp1_data)
    stationidList = []
    for i in iter2:
        stationid = int(i.group().split('=')[2][1:-1])
        if stationid not in stationidList:
            stationidList.append(stationid)
    return stationidList

def download(stationId,year,path,filename ):
    tempurl = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={}&Year={}&Month=8&Day=1&timeframe=2&submit=Download+Data'.format(stationId,year)
    r = requests.get(tempurl,allow_redirects = False)
    if r.status_code == 200:
        with open(path + filename, "wb") as code:
            code.write(r.content)
    else:
        print('{}:{} is not exist'.format(stationId,year))        

#读取df_city程序 Cli_ID什么意思
with open('city.csv') as data_obj:
    line = data_obj.readline()
    data = [[],[],[]]
    count = 0
    flag = 0 
    while(line != ''):  
        if len(line) == 25:
            count +=1
            line = data_obj.readline()
            continue
        data[count].append(line.split(','))
        line = data_obj.readline()
    temp = data[2][1:]
    df_city = pd.DataFrame(temp,columns = data[2][0])
#    df_city.columns = [i[1:-1] for i in df_city.columns]
#    for i in df_city.columns :
#        df_city[i] = df_city[i].apply(lambda x: x[1:-1])

df_temp  = df_city.groupby(['Prov','Stn_Name','Lat','Long'])['D'].count().reset_index()
for i in df_temp['Prov'].value_counts().index[1:]:
    print(i)
    df_2 = df_temp.loc[df_temp['Prov'] == i]
    os.mkdir('Prov_{}'.format(i))
    path = os.getcwd()+'\\Prov_{}\\'.format(i)
    for stn in df_2['Stn_Name']:
        station = findStationID(stn)
        for stid in station:
            for year in [k for k in range(1990,2019,1)]:
                download(stid,year,path,'{}_{}_{}.csv'.format(stn,stid,year))
    

