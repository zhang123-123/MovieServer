# -*- coding:utf-8 -*-
import time
from hashlib import md5
# 图像名 = MD5(用户名 + 时间戳)
def gen_img_name(username):
    img_name = username + str(time.time())
    new_md5 = md5()
    new_md5.update(img_name.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


if __name__ == '__main__':
    a = gen_img_name("zhangsan")
    print(a)
