# -*- coding:utf-8 -*-
def time_(time_delta):
    result = ""
    if time_delta < 60:
        temp = int(((time_delta / 3600) * 3600) % 60)
        result = '%s秒前' % temp
    elif time_delta < 3600:
        temp = int(((time_delta / 3600) * 3600) / 60)
        result = '%s分钟前' % temp
    elif time_delta < 24 * 60 * 60:
        result = '%s小时%s分钟前' % (int(time_delta // 3600), int((((time_delta % 3600) / 3600) * 3600) / 60))
    elif time_delta < 24 * 60 * 60 * 30:
        result = '%s天前' % (int(time_delta / (24 * 60 * 60)),)
    elif time_delta < 24 * 60 * 60 * 30 * 12:
        result = '%s月前' % (int(time_delta / (24 * 60 * 60 * 30)),)
    else:
        result = '%s年前' % (int(time_delta / (24 * 60 * 60 * 30 * 12)),)

    return result
