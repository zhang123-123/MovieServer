from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tools.zfb_pay import AliPay
from user.models import Pay
import time

# Create your views here.
@login_required
def recharge_vip(request):
    result = ""
    if request.method == "GET":
        out_trade_no = request.GET.get("out_trade_no")
        if out_trade_no:
            pays = Pay.objects.filter(trade_no=out_trade_no)
            if pays:
                pay = pays[0]
                ali = AliPay(out_trade_no)
                is_ok = ali.check_pay_state(3)
                if is_ok:
                    request.user.all_price += pay.pay_price
                    request.user.save()
                    result = "支付成功"
                    pay.pay_status = 1
                    if request.user.all_price < 10.0:
                        vip = 0
                    elif request.user.all_price < 50.0:
                        vip = 1
                    elif request.user.all_price < 100.0:
                        vip = 2
                    else:
                        vip = 3
                    request.user.vip = vip
                    request.user.save()
                else:
                    result = "支付失败"
                    pay.pay_status = -1
                pay.save()
            else:
                result = "订单号不存在"
        else:
            result = "尚未支付"
    return render(request, "vip.html", {"result": result})


@csrf_exempt
def zhifu(request):
    result = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            price = request.POST.get("price")
            trade_no = str(int(time.time()))
            ali = AliPay(trade_no, int(price))
            pay_url = ali.create_url()
            result["code"] = "001"
            result["message"] = "生成支付页成功"
            result["pay_url"] = pay_url
            pay = Pay()
            pay.trade_no = trade_no
            pay.out_trade_no = ""
            pay.user_id = request.user.id
            pay.pay_price = float(price)
            pay.pay_status = 0
            pay.save()
        else:
            result["code"] = "002"
            result["message"] = "未登录，请先登录"
    return JsonResponse(result)


"""out_trade_no=1568959656
&method=alipay.trade.page.pay.return
&total_amount=10.00
&sign=Y%2FkC1YgptqKn8W4VXGScrm8gXf9hxLx6BRYGtgqMAdOnaw2u0JuEOpiPnQHIspUQhjpZLDW6cAdvdg8X851SOZIiZNurV1S6rQEFqKjJh2JO4%2BPBpRX3qPNMtcgv6DDajqxAboPgyt5JEUBhEc%2Bwd9Y%2FDJMH3iLctD2jiIjUbnb5FK14Ny%2BzTJs5QP8NWnGZEF2YHYoVkbAOr9YVFXivu1GzpbpQ70StKl%2FtcTOHERoerQe%2B%2FE2s93ZZpF59%2FumJdvGeqaVRBrzMWRHZss49Y3uDnrxVfcv960%2BJVM2LJzbWEP%2Bo9%2FVesp6YzxAjjPu4ZNzz50dpXwsYXm%2Bx%2F4wloQ%3D%3D
&trade_no=2019092022001468391000018669
&auth_app_id=2016101200668491
&version=1.0
&app_id=2016101200668491
&sign_type=RSA2
&seller_id=2088102179229447
&timestamp=2019-09-20+14%3A07%3A58"""

