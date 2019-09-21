# -*- coding:utf-8 -*-
import datetime
import time
now_time = time.time()
print(now_time)
time_delta = now_time - (time.time() - 360000000)
print(time_delta, type(time_delta))
a = "2019-09-19 01:32:06.461533"
t = "2017-11-24 17:30:00"
#将其转换为时间数组
timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
#转换为时间戳:
timeStamp = int(time.mktime(timeStruct))
print(timeStamp)
item = {}
if time_delta < 60:
    temp = int(((time_delta / 3600) * 3600) % 60)
    result = '%s秒前' % temp
    print(result)
elif time_delta < 3600:
    temp = int(((time_delta / 3600) * 3600) / 60)
    result = '%s分钟前' % temp
    print(result)
elif time_delta < 24 * 60 * 60:
    result = '%s小时%s分钟前' % (int(time_delta // 3600), int((((time_delta % 3600) / 3600) * 3600) / 60))
    print(result)
elif time_delta < 24 * 60 * 60 * 30:
    result = '%s天前' % (int(time_delta / (24 * 60 * 60)),)
    print(result)
elif time_delta < 24 * 60 * 60 * 30 * 12:
    result = '%s月前' % (int(time_delta / (24 * 60 * 60 * 30)),)
    print(result)
else:
    result = '%s年前' % (int(time_delta / (24 * 60 * 60 * 30 * 12)),)
    print(result)
print(item)
