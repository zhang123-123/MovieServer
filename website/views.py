from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from urllib import request as req
import re
import json
from .models import User
from urllib import parse
import random


def index(request):
    try:
        openid = request.session['openid']  # 读取Session
        userinfo = User.objects.get(openid=openid)  # 根据Session获取用户信息
        return render(request, 'index.html', {'userinfo': userinfo})
    except:  # 如果发生异常
        return render(request, 'index.html')


def qq_login(request):
    state = str(random.randrange(100000, 999999))  # 定义一个随机状态码，防止跨域伪造攻击。
    request.session['state'] = state  # 将随机状态码存入Session，用于授权信息返回时验证。
    client_id = '1*******9'  # QQ互联中网站应用的APP ID。
    callback = parse.urlencode({'redirect_uri': 'http://127.0.0.1:8888/login'})
    # 对回调地址进行编码，用户同意授权后将调用此链接。
    login_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=%s&%s&state=%s' % (
        client_id, callback, state)  # 组织QQ第三方登录链接
    return HttpResponseRedirect(login_url)  # 重定向到QQ第三方登录授权页面


def login_qq(request):
    if request.session['state'] == request.GET['state']:  # 验证状态码，防止跨域伪造攻击。
        code = request.GET['code']  # 获取用户授权码
        client_id = '1*******9'  # QQ互联中网站应用的APP ID。
        client_secret = '83b76c870************9ec664b8891'  # QQ互联中网站应用的APP Key。
        callback = parse.urlencode({'redirect_uri': 'http://127.0.0.1:8888/login'})
        # 对回调地址进行编码，用户同意授权后将调用此链接。
        login_url = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&%s' % (
            code, client_id, client_secret, callback)  # 组织获取访问令牌的链接
        response = req.urlopen(login_url).read().decode()  # 打开获取访问令牌的链接
        # ...接下一段代码...
        access_token = re.split('&', response)[0]  # 获取访问令牌
        res = req.urlopen('https://graph.qq.com/oauth2.0/me?' + access_token).read().decode()  # 打开获取openid的链接
        # ...接下一段代码...
        openid = json.loads(parse_jsonp(res))['openid']  # 从返回数据中获取openid
        userinfo = req.urlopen('https://graph.qq.com/user/get_user_info?oauth_consumer_key=%s&openid=%s&%s' % (
            client_id, openid, access_token)).read().decode()  # 打开获取用户信息的链接
        userinfo = json.loads(userinfo)  # 将返回的用户信息数据（JSON格式）读取为字典。
        user = User.objects.get(openid=openid)  # 查询是否已存在用户
        if not user:  # 如果不存在用户
            user = User()  # 创建新用户
            user.openid = openid  # 写入用户信息
        user.nickname = userinfo['nickname']  # 写入用户信息
        user.gender = userinfo['gender']  # 写入用户信息
        user.head = userinfo['figureurl_qq_1']  # 写入用户信息
        user.save()  # 保存或更新用户
        request.session['openid'] = openid  # 将已登录的用户openid写入Session
        return render(request, 'index.html', {'userinfo': user})

    else:
        return HttpResponse('授权失败！')


def parse_jsonp(jsonp_str):
    try:
        return re.search('^[^(]*?\((.*)\)[^)]*$', jsonp_str).group(1)
    except:
        raise ValueError('无效数据！')
