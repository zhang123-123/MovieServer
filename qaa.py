APPNET = 'https://openapi.alipaydev.com/gateway.do'
NOTIFY_URL = None
import time


def creat_ali():  # 创建ali对象
    import alipay
    APPID = "2016101200668491"
    ZFB_DNS = "https://openapi.alipaydev.com/gateway.do"

    APP_PRIVATE = """-----BEGIN RSA PRIVATE KEY-----
                    MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCBWkjIWeZMyYVBD9YNOYP6n0qPZrM3ZYt1cVzSG/ClARgJdJqsy1eGLHKe3ieeaoqJRu8PvRzYwgbBXa8IlsddT3y7+ERi9kohMWrafHCAT2aqxXdEaRq3KH0x2el8KnSBYq6Mv1K4WVZ60+D2IYAMtRUPCjm3opIGndZ5iEdkClhynMQ/wBc4xyexxQVPdhtF+GDEFQD92WzWGk1XM8/wgwjiGvUeZa42I1+6O59yVZywaQydFFoXnAXmSaLJ1j+GOAEu6c098e8a/r1Q0WXI9WhiKgAR/is39IOPhseuyHi2ueux64DjSmpxRvRjupyBNXxkQ+V6SSBtw6uMK9/RAgMBAAECggEAJzjZGOcpjd8NKM1Een4WJshmM1VQwltoDhRxsMQIFABg6X0R6ZM+1tBjcQirur1ThIydsIgHVzJ+GePuTwxpJ0IS8Gw3UEqd77KsU9OnyUBKQT3fDD9SencsfxE0WxIEgbcKdmMNEhkEv/m/HOLLkQ7Xc9gF6EjDPn5dqjxIaWzLQqgcqKmxMOznUv5XQAp5nLRrgWgJgS3tdxPt2ojRnKsHEmfgu6jskL+X7jn4R5Br9LXjXAXS7q7tZtHI80oZzE+nGyAhdkKJgvyalpE5MnmjkbwJVasTM6Ly1CSFDpETu75ZnAHiEQIXmnMp2KJlWzlYWjRwkQtRIpU23vK2AQKBgQC6Db/LOQfxzhET5pJpYoYGdkbr1aRmGJquoi9EYTjzaMisyg+VmwzIuFrN6JuugGG3GCUG7If8sOdCiP7img4qjVHt+TE+1mQR3nHUQUeh79awNpkr7Usgbdbr9mf/pxsL5Z80mA6jLkaTMKV+WpnljsLnUEtllTNLLFViQfcd5QKBgQCx+34qsORVt9MIqiVJFiOxXo8inWOvY4AZp702iHHXgzyUMP+VeIEwmai3J41OgOMn5ieuEHtFOikQlcd0roFrqnOih6nCeGeHa3eBV4cWqQ7FNx0NoO6z0uZE2l2HeZUSyKBq6N1Nl7FIQBRrk+T3SXJUhFjTGKsJBL/+ajy7fQKBgFa268o7BYHkyj7dOyYU/mRqoflu9JWFKCr2elNDgPipwMYP0x2mS1oN2nyXyl+VhHWCslc8zNCwXsi68xkINkwM27+vYg1ofPF7HNCRsGJAV25/s/ouOdKefwoxKR2Vc9yipAYuTLwvaENX6/otHgdI93w6BzoMRQDnY9BM8HElAoGAeNqRqEFnOoFRDiAio0ciQ202+kUvDEgfEsygoafyzWkyuFmxIvipmKuuMXfs7rJ8DHqu1PYiDjbY7YcW4bcg8E/UpzdBYWjKu9yQUEZz10JCYk3zL27oxzhc3cH9ImG/hPqwWwf2RZrMaYgBla7eGcBInvUjL2wfr0cHa6UNyi0CgYBCOYdMFk72i0GCpVwMLp4/I8N97BLhDtRf0N55i/nUCZwGOQijyfFKoP0GlgfO0eSVzUNZl25sYcwTyzOZLhOpmEAX/Z1yyd4DaUUXu/vx5If5Gtr1TFiCmjDion78BRqoXg5RCHQs6uWpq2D0YhoO/2qKsrvoYqw5twsx40u/8w==
                    -----END RSA PRIVATE KEY-----"""
    APP_PUBLIC = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgVpIyFnmTMmFQQ/WDTmD+p9Kj2azN2WLdXFc0hvwpQEYCXSarMtXhixynt4nnmqKiUbvD70c2MIGwV2vCJbHXU98u/hEYvZKITFq2nxwgE9mqsV3RGkatyh9MdnpfCp0gWKujL9SuFlWetPg9iGADLUVDwo5t6KSBp3WeYhHZApYcpzEP8AXOMcnscUFT3YbRfhgxBUA/dls1hpNVzPP8IMI4hr1HmWuNiNfujufclWcsGkMnRRaF5wF5kmiydY/hjgBLunNPfHvGv69UNFlyPVoYioAEf4rN/SDj4bHrsh4trnrseuA40pqcUb0Y7qcgTV8ZEPlekkgbcOrjCvf0QIDAQAB"
    ALI_PUBLIC = """-----BEGIN PUBLIC KEY-----
                    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl7OwhGmH/J2aSP3j4Pbk/NxvNhBfAIBDCEujBN9vdnCu3kKA5SNkomvHvdHXM66/3LQhKzigMg9r/y6CrgQJPR8Q+wHrRiGXbLmIqJw2pMVfXgms1gr1Mz9aR3GbuIzTMOLcHALWPQ47cNtgPUg1UfRE0NyJMpZ3+crg9Dzt5fJ7BJK+7m9FDX8v7R0axahEkkO0IYaxqHOvZ5v0pygls3z2ZM0gVon63cu1K8PxD2KsNHwK8dUkw6uDY2VqkyYybQGRlT4VWQkDYdPNqzMDmjV7Y4DjX+b/JV+Wu7mYY6llosNT30yQhKhcb1C5MEPulvbeOrjdxP59+niERAV/4QIDAQAB
                    -----END PUBLIC KEY-----"""
    ali = alipay.AliPay(
        appid=APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE,
        alipay_public_key_string=ALI_PUBLIC,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认False
    )
    return ali


def create_paypage_url(trade_no, price, subject):  # 生成网页支付地址

    order_string = creat_ali().api_alipay_trade_page_pay(
        out_trade_no=trade_no,
        total_amount=price,
        subject=subject,
        notify_url=NOTIFY_URL  # 可选, 不填则使用默认notify url
    )
    pay_url = APPNET + '?' + order_string
    return pay_url


def check_pay_state(trade_no, timeout, qr_code=None):
    import time, os
    ok = False
    while True:
        time.sleep(1)
        timeout = timeout - 1

        result = creat_ali().api_alipay_trade_query(trade_no)
        # print(result)
        print(f"等待支付还剩{timeout}秒")
        if result.get('trade_status') == 'TRADE_SUCCESS':
            print("支付成功")
            if qr_code:
                os.remove(qr_code)
            ok = True
            break
    return ok


def create_qr_code(trade_no, price, subject, dir):
    pay = creat_ali().api_alipay_trade_precreate(subject, trade_no, price)
    qr_code = pay.get('qr_code')
    import qrcode, os
    qr = qrcode.QRCode(
        version=1,  # 设置容错率为最高
        error_correction=qrcode.ERROR_CORRECT_H,  # 用于控制二维码的错误纠正程度
        box_size=8,  # 控制二维码中每个格子的像素数，默认为10
        border=1,  # 二维码四周留白，包含的格子数，默认为4
    )
    qr.add_data(qr_code)  # QRCode.add_data(data)函数添加数据
    img = qr.make_image()
    path = os.path.join(dir, trade_no + '.jpg')
    img.save(path)
    return path


def cancel_trade(trade_no, timeout):
    import time
    ok = False
    while True:
        time.sleep(1)
        timeout = timeout - 1
        if timeout == 0:
            print("订单取消")
            qx = creat_ali().api_alipay_trade_cancel(trade_no)
            print(qx)
            ok = True
            break
    return ok


if __name__ == '__main__':
    trade_no = str(int(time.time()))
    price = 0.01
    subject = "vip充值"
    url=create_paypage_url(trade_no, price, subject)
    print(url)
    # qrcode = create_qr_code(trade_no, price, subject, '')
    # print(qrcode)
    check = check_pay_state(trade_no, 60)
