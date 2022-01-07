from typing import Sized
import urllib.request as request

import json

city = '基隆市'


def getweather(b):
    ur1 = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-4BA79C6C-79A5-4491-92B2-9F01DBB46A6F&format=JSON&locationName=&elementName=&sort=time'
    with request.urlopen(ur1) as response:
        data = json.load(response)

    cities = ['基隆市', '嘉義市', '臺北市', '嘉義縣', '新北市', '臺南市', '桃園縣', '高雄市', '新竹市', '屏東縣',
              '新竹縣', '臺東縣', '苗栗縣', '花蓮縣', '臺中市', '宜蘭縣', '彰化縣', '澎湖縣', '南投縣', '金門縣', '雲林縣', '連江縣']

    a = len(cities)
    for i in range(0, a):
        location = data['records']['location'][i]['locationName']
        if b == location:
            c = i
    print(c)

    for j in range(0, 3):
        mixtemp = data['records']['location'][c]['weatherElement'][2]['time'][j]['parameter']['parameterName']
        mixtemp_starttime = data['records']['location'][c]['weatherElement'][2]['time'][j]['startTime'][5:19]
        mixtemp_endtime = data['records']['location'][c]['weatherElement'][2]['time'][j]['endTime'][5:19]
        maxtemp = data['records']['location'][c]['weatherElement'][4]['time'][j]['parameter']['parameterName']
        temp_wx = data['records']['location'][c]['weatherElement'][0]['time'][j]['parameter']['parameterName']
        temp_pop = data['records']['location'][c]['weatherElement'][1]['time'][j]['parameter']['parameterName']

        mixtemp_com = mixtemp_starttime + '\n' + \
            mixtemp_endtime + '\n' + '溫度 ' + mixtemp + \
            ' ~ ' + maxtemp + '℃' + temp_wx + temp_pop
        temp_list = []

        if j == 0:
            temp_list1 = mixtemp_com
            temp_list.append(temp_list1)
        if j == 1:
            temp_list2 = mixtemp_com
            temp_list.append(temp_list2)
        if j == 2:
            temp_list3 = mixtemp_com
    temp_list.append(temp_list1)
    temp_list.append(temp_list2)
    temp_list.append(temp_list3)

    return temp_list


temp_list = getweather(city)
print(temp_list[0][42:45])
print(temp_list[0][45:48])
print(temp_list[0][30:41])
