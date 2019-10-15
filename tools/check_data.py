# -*- coding:utf-8 -*-
import re

def check_phone(phone):
    phone_pattern = re.compile("^1[345678]\d{9}$")
    is_phone = phone_pattern.match(phone)
    if is_phone:
        print("是手机号")
        return True
    return False


def check_email(name):
    email_pattern = re.compile("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$")
    is_email = email_pattern.match(name)
    if is_email:
        print("是邮箱")
        return True
    return False


# 强度=数字+字母+符号（6-12）
# 1弱 2中 3强 4密码长度不对
def check_psw_strong(password):
    if 6 <= len(password) <= 12:
        weak = re.compile(r'^((\d+)|([A-Za-z]+)|(\W+))$')
        level_weak = weak.match(password)
        level_middle = re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+', password)
        level_strong = re.match(r'(\w+|\W+)+', password)
        if level_weak:
            return 1
        else:
            if level_middle and len(level_middle.group()) == len(password):
                return 2
            else:
                if level_strong and len(level_strong.group()) == len(password):
                    return 3
    else:
        return 4


# 检测安全码是否为六位
def check_code(code):
    pattern = re.compile("\d{6}")
    result = pattern.match(code)
    if result:
        return True
    return False


# 检测昵称是否全为中文  是否已存在
def check_nickname(name):
    pattern = re.compile("[\u4e00-\u9fa5]{3,10}")
    result = pattern.match(name)
    if result:
        return True
    return False




