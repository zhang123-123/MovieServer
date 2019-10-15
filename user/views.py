from django.db.models import Q
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from .models import PythonUser, Comment, Huifu

import time
import json
from tools.check_data import check_email, check_psw_strong, check_code, check_nickname, check_phone
from django.contrib.auth.hashers import make_password, check_password
from tools.img_path_name import gen_img_name
from tools.time_data import time_
from tools.orm2json import object_to_json
from tools.sent_phone_code import ZhenziSmsClient
import random

from django.core.mail import send_mail
from PythonServer import settings
import redis
from django.core.cache import cache

from django.contrib.auth import logout as sys_logout, login as sys_login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

"""
1.向谁发请求
url = a/
2.请求方式
post
3.携带哪些参数
email code pwd pwd1 nickname
4.返回结果
001 注册成功
002 注册失败 昵称已存在
003 注册成功 安全码不正确
004 注册成功 数据格式不正确

"""


# REDIS_DB = redis.Redis()

# Create your views here.
@csrf_exempt
def regist(request):
    result = {}
    if request.method == "POST":
        post_args = request.POST
        email = post_args.get("email", "邮箱错误")
        code = post_args.get("code")
        pwd = post_args.get("pwd")
        pwd1 = post_args.get("pwd1")
        nickname = post_args.get("nickname")
        if check_email(email):
            if pwd == pwd1:
                if check_psw_strong(pwd) == 3:
                    print(code, type(code))
                    print(cache.get(email), type(cache.get(email)))
                    # redis_code = cache.get(email).decode()
                    # cache.get(email) 返回的值是int类型
                    redis_code = str(cache.get(email))
                    print(redis_code, type(redis_code))
                    if check_code(code) and code == redis_code:
                        if check_nickname(nickname):
                            nicknames = PythonUser.objects.filter(nickname=nickname)
                            if nicknames:
                                result["code"] = "007"
                                result["message"] = "昵称已存在"
                                print("昵称已存在")
                            else:
                                # get :要么返回一个，要么报错
                                # PythonUser.objects.get()
                                users = PythonUser.objects.filter(username=email)
                                # print(users)
                                # for user in users:
                                #     print(user.pwd)
                                #     a = check_password(user.pwd)
                                #     print(a)
                                """
                                **__gt 表示大于
                                **__gte 表示大于等于
                                **__lt 表示小于
                                **__lte 表示大于等于
                                """
                                # PythonUser.objects.all() # 所有
                                if users:
                                    result["code"] = "006"
                                    result["message"] = "用户已存在"
                                    print("用户已存在")
                                else:

                                    new_pwd = make_password(pwd)
                                    # ORM插入数据
                                    user = PythonUser()
                                    user.username = email
                                    user.password = new_pwd
                                    user.nickname = nickname
                                    user.save()
                                    print("注册成功")
                                    result["code"] = "001"
                                    result["message"] = "注册成功"
                        else:
                            result["code"] = "001"
                            result["message"] = "昵称格式不正确"
                            print("昵称格式不正确")
                    else:
                        result["code"] = "005"
                        result["message"] = "安全码不正确或失效"
                        print("安全码不正确")
                else:
                    result["code"] = "004"
                    result["message"] = "密码强度不够"
                    print("密码强度不够")
            else:
                result["code"] = "003"
                result["message"] = "密码两次输入不一致"
                print("密码两次输入不一致")

        else:
            result["code"] = "002"
            result["message"] = "邮箱格式不正确"
            print("邮箱格式不正确")
        return JsonResponse(result)
    elif request.method == "GET":
        # render 渲染 加载网页
        return render(request, "regist.html")
    return HttpResponse("请求异常")

    # # 1.获取GET请求的参数
    # get_args = request.GET
    # # 2.获取POST请求的参数
    # post_args = request.POST
    # print(get_args, post_args)
    # # 具体的注册逻辑
    # # 要么返回网页，要么返回响应
    # return HttpResponse("欢迎注册")


@csrf_exempt
def login(request):
    result = {}
    if request.method == "POST":
        post_args = request.POST
        email = post_args.get("email", "邮箱错误")
        pwd = post_args.get("pwd")
        vercode = post_args.get("vercode")
        remember = post_args.get("remember")
        save_code = request.session["v_code"]
        if check_email(email):
            users = PythonUser.objects.filter(username=email)
            vercode = vercode.upper()
            if users:
                if vercode != save_code:
                    result["code"] = "004"
                    result["message"] = "验证码输入不正确"
                else:
                    for user_ in users:
                        # print(check_password(pwd, user.pwd))
                        if check_password(pwd, user_.password):
                            result["code"] = "001"
                            result["message"] = "登入成功"
                            request.session['username'] = user_.email
                            user = authenticate(username=email, password=pwd)
                            sys_login(request, user)
                            # context = {}
                            # context['email'] = email
                            # request.session['msg'] = context
                        else:
                            result["code"] = "005"
                            result["message"] = "密码输入不正确"
            else:
                result["code"] = "003"
                result["message"] = "邮箱不存在"
        else:
            result["code"] = "002"
            result["message"] = "邮箱格式不正确"
        return JsonResponse(result)
    elif request.method == "GET":
        # render 渲染 加载网页
        return render(request, "login.html")
    return HttpResponse("请求异常")


@csrf_exempt
def forgetpwd(request):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        return render(request, "forgetpwd.html")
    return HttpResponse("请求异常")


def index(request):
    return render(request, "index.html")


def get_code(request):
    result = {}
    email = request.GET.get("email")
    if check_email(email):
        if cache.get(email):
            result["code"] = "003"
            result["message"] = "已发送，请查看邮箱安全码"
        else:
            code = random.randint(100000, 999999)
            # subject = "邮箱安全码"
            content = f"正在进行邮箱验证，本次请求的验证码为：{code}(为了保障您帐号的安全性，请在1小时内完成验证。)"
            # receive_email = [email]
            # send_email(subject, content, [], receive_email)
            msg = content
            send_mail(
                subject='请注意这是Django邮件测试',
                message=msg,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]  # 这里注意替换成自己的目的邮箱，不然就发到我的邮箱来了：）
            )
            result["code"] = "001"
            result["message"] = "发送邮件成功"
            cache.set(email, code, 600)
    else:
        result["code"] = "002"
        result["message"] = "邮件格式不正确"
    return JsonResponse(result)


# 因为页面控制每次点击图片在连接后加？ 或减去？，url一直都是这两个，Django会自动将这两个url的执行加入缓存，所以每次会获得一样的验证图片
# 该语法糖 告诉系统不要对该方法进行缓存操作
@never_cache
def get_v_code(request):
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 定义生成一个随机颜色代码的内部函数
    def get_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        "RGB",  # 图片格式
        (166, 37),  # 图片大小
        color=get_color()
    )

    # 在图片中加文字

    # 生成一个画笔对象
    draw_obj = ImageDraw.Draw(img_obj)

    # 加载字体文件
    font_obj = ImageFont.truetype("static/font/msyh.ttf", size=28)

    # 循环5次，每次往图片上写入一个随机字符
    tmp_list = []
    for i in range(5):
        n = str(random.randint(0, 9))
        l = chr(random.randint(97, 122))
        u = chr(random.randint(65, 90))

        r = random.choice([n, l, u])
        tmp_list.append(r)
        draw_obj.text(
            (i * 30 + 10, 0),  # 位置
            r,  # 内容
            get_color(),  # 颜色
            font=font_obj,
        )
    # 得到随机验证码
    v_code = "".join(tmp_list)
    request.session["v_code"] = v_code.upper()

    # 第一种，将图片保存到文件（硬盘），然后再返回到页面
    # with open(‘vv.png‘, ‘wb‘)as f:
    #     img_obj.save(f, ‘png‘)
    # with open(‘vv.png‘, ‘rb‘)as f:
    #     return HttpResponse(f.read(), content_type=‘imge/png‘)

    # 第二种，直接将图片放在内存中，返回回去
    from io import BytesIO
    tmp = BytesIO()  # 生成一个IO对象
    img_obj.save(tmp, "png")

    data = tmp.getvalue()
    return HttpResponse(data, content_type="imge/png")


@login_required
def logout(request):
    # sys_logout()这个方法，会将存储在用户session的数据全部清空
    sys_logout(request)
    # 重定向 从一个网页返回另一个网页
    # 使用系统的退出功能，实现退出，并重定向回首页
    index_url = reverse("index")
    return redirect(index_url)


def update_info(request):
    return render(request, "update_info.html")


@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        file_content = ContentFile(request.FILES['file'].read())
        # print(file_content)
        ext = request.FILES['file'].name.split(".")[-1]
        new_img_name = gen_img_name(request.user.username) + "." + ext
        request.user.img.save(new_img_name, file_content)
        # print(a)
        result = {
            'code': '001',
            'message': '上传成功'
        }
        return JsonResponse(result)
    elif request.method == 'GET':
        return render(request, 'upload.html')


# 上传手机号
@csrf_exempt
def up_phone(request):
    result = {}
    if request.method == "POST":
        phone = request.POST.get("phone")
        phone_code = request.POST.get("code")
        if check_phone(phone):
            # 判断手机验证码
            if phone_code == str(cache.get(phone)):
                PythonUser.objects.filter(username=request.user.username).update(phone=phone)
                result["code"] = "001"
                result["message"] = "上传手机号成功"
            else:
                result["code"] = "003"
                result["message"] = "验证码不正确或失效"
        else:
            result["code"] = "002"
            result["message"] = "手机号格式不正确"
        return JsonResponse(result)
    elif request.method == "GET":
        return render(request, 'up_phone.html')
    else:
        return HttpResponse("请求失败")


# 发送手机验证码
@csrf_exempt
def send_phone_code(request):
    result_ = {}
    if request.method == "POST":
        phone = request.POST.get("phone")
        if cache.get(phone):
            result_["code"] = "003"
            result_["message"] = "已发送，请查看手机验证码码"
        else:
            # client = ZhenziSmsClient("http://sms_developer.zhenzikj.com", 102703, "cc337e73-a258-4dbe-8dda-ff228a4354f8")
            code = random.randint(100000, 999999)
            # subject = "邮箱安全码"
            content = f"正在进行手机验证，本次请求的验证码为：{code}(为了保障您帐号的安全性，请在1小时内完成验证。)"
            print(content)
            # result = client.send(phone, content)
            # result_obj = json.loads(result)
            # if result_obj["code"] == 0:
            result_["code"] = "001"
            result_["message"] = "发送成功"
            # else:
            #     result_["code"] = "002"
            #     result_["message"] = "发送失败"
            cache.set(phone, code, 600)
        return JsonResponse(result_)
    elif request.method == "GET":
        return render(request, 'up_phone.html')
    else:
        return HttpResponse("请求失败")


# 修改密码
@csrf_exempt
def update_pwd(request):
    result = {}
    if request.method == "POST":
        pwd = request.POST.get("pwd")
        new_pwd = request.POST.get("new_pwd")
        if check_password(pwd, request.user.password):
            check_pwd = make_password(new_pwd)
            PythonUser.objects.filter(username=request.user.username).update(password=check_pwd)
            result["code"] = "001"
            result["message"] = "修改密码成功"
        else:
            result["code"] = "002"
            result["message"] = "原密码输入错误！请重新输入"
        return JsonResponse(result)
    elif request.method == "GET":
        return render(request, "update_pwd.html")
    else:
        return HttpResponse("请求失败")


# 发表评论
@csrf_exempt
def user_pl(request):
    result = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            pl_content = request.POST.get("pl_content")
            user_id = request.user.id
            movie_id = request.POST.get("movie_id")
            if request.user.vip >= 2:
                if pl_content:
                    comment = Comment()
                    comment.user_id = user_id
                    comment.movie_id = movie_id
                    comment.user_comment_content = pl_content
                    comment.save()
                    result["code"] = "001"
                    result["message"] = "评论成功"
                else:
                    result["code"] = "004"
                    result["message"] = "评论内容不能为空"
            else:
                result["code"] = "003"
                result["message"] = "等级不够"
        else:
            result["code"] = "002"
            result["message"] = "未登录"
            result["login_url"] = reverse("login")
    elif request.method == "GET":
        """
        result = {
            "code": "",
            "message": "查询成功"，
            "dates":[{
            "username":"",
            "user_img":""
            "user_hf":[{}]
            }]
        }
        """
        movie_id = request.GET.get("movie_id")
        movie_comments = Comment.objects.raw(
            """SELECT * FROM user_comment left join user_pythonuser on user_comment.user_id = user_pythonuser.id where movie_id=%s order by movie_date """,
            (movie_id,))

        if movie_comments:
            result["code"] = "001"
            result["message"] = "查询成功"
            result["datas"] = []
            print(movie_comments)
            i = 1
            for movie_comment in movie_comments:
                dict1 = {}
                # print(movie_comment.user_comment_content)
                # print(movie_comment.phone, movie_comment.id, movie_comment.user_id)
                dict1["user_name"] = movie_comment.username
                dict1["user_id"] = movie_comment.user_id
                dict1["user_img"] = movie_comment.img
                dict1["logn_type"] = movie_comment.login_type
                dict1["comment_content"] = movie_comment.user_comment_content
                dict1["comment_id"] = movie_comment.id

                dict1["lou"] = i

                # date = time.time()
                # timeArray = time.localtime(date)
                # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                # print(otherStyleTime)
                # date_time = otherStyleTime - movie_comment.movie_date
                # print(movie_comment.movie_date, type(movie_comment.movie_date))
                # print(str(movie_comment.movie_date))
                t = str(movie_comment.movie_date).split(".")[0]
                timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
                # 转换为时间戳:
                timeStamp = int(time.mktime(timeStruct))
                dict1["movie_date"] = time_(time.time() - timeStamp)
                # hf_s = Huifu.objects.filter(
                #     Q(movie_id=movie_id) & Q(comment_id=dict1["comment_id"]))
                print(dict1)
                hf_s = Huifu.objects.raw(
                    """SELECT * FROM user_huifu left join user_pythonuser on user_huifu.hf_user_id = user_pythonuser.id where movie_id=%s and comment_id=%s order by hf_date """,
                    (movie_id, dict1["comment_id"]))
                print(hf_s)
                # hf_obj = object_to_json(hf_s)
                # dict1["hf_info"] = hf_obj
                dict1["hf_info"] = []
                j = 1
                for hf_ in hf_s:
                    dict2 = {}
                    dict2["user_name"] = hf_.username
                    dict2["user_id"] = hf_.hf_user_id
                    dict2["user_img"] = hf_.img
                    dict2["logn_type"] = hf_.login_type
                    dict2["hf_content"] = hf_.hf_content
                    dict2["hf_id"] = hf_.id
                    t = str(hf_.hf_date).split(".")[0]
                    timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
                    # 转换为时间戳:
                    timeStamp = int(time.mktime(timeStruct))
                    print(dict2)
                    dict2["movie_date"] = time_(time.time() - timeStamp)
                    dict2["lou"] = j
                    dict1["hf_info"].append(dict2)
                    j += 1
                result["datas"].append(dict1)
                i += 1

        else:
            result["code"] = "002"
            result["message"] = "查询失败"
    else:
        pass
    # print(result)
    # print(json.dumps(result))
    return JsonResponse(result)


# 删除评论
def delete_pl(request):
    result = {}
    # DELETE = QueryDict(request.body)
    # print(DELETE)
    # id = DELETE.get('id')
    id = request.GET.get("id")
    print(id)
    comments = Comment.objects.filter(id=id)
    if comments:
        comments.delete()
        result["code"] = "001"
        result["message"] = "删除成功"
    else:
        result["code"] = "002"
        result["message"] = "id不存在"

    return JsonResponse(result)


# 回复
@csrf_exempt
def add_hf(request):
    result = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_user_id = request.POST.get("comment_user_id")
            movie_id = request.POST.get("movie_id")
            hf_content = request.POST.get("hf_content")
            comment_id = request.POST.get("comment_id")
            if request.user.vip >= 2:
                if hf_content:
                    hf = Huifu()
                    hf.comment_id = comment_id
                    hf.hf_content = hf_content
                    hf.comment_user_id = comment_user_id
                    hf.movie_id = movie_id
                    hf.hf_user_id = request.user.id
                    hf.save()
                    result["code"] = "001"
                    result["message"] = "回复成功"
                else:
                    result["code"] = "004"
                    result["message"] = "回复内容不能为空"
            else:
                result["code"] = "003"
                result["message"] = "等级不够"
        else:
            result["code"] = "002"
            result["message"] = "未登录"
            result["login_url"] = reverse("login")
    return JsonResponse(result)


# 删除回复
def delete_hf(request):
    result = {}
    # DELETE = QueryDict(request.body)
    # print(DELETE)
    # id = DELETE.get('id')
    id = request.GET.get("id")
    movie_id = request.GET.get("movie_id")
    print(id)
    hfs = Huifu.objects.filter(id=id)
    if hfs:
        hfs.delete()
        result["code"] = "001"
        result["message"] = "删除成功"
    else:
        result["code"] = "002"
        result["message"] = "id不存在"

    return JsonResponse(result)


"""
def up_vip(request):
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
"""
