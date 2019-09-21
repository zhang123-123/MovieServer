import re

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


check_psw_strong("231313131.l")