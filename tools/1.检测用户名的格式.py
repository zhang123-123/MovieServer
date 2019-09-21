import re


def check_username(name):
    phone_pattern = re.compile("^1[345678]\d{9}$")
    is_phone = phone_pattern.match(name)
    if is_phone:
        print("是手机号")
        return True
    else:
        email_pattern = re.compile("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$")
        is_email = email_pattern.match(name)
        if is_email():
            print("是邮箱")
            return True
    return False


check_username("23")