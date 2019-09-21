# -*- coding:utf-8 -*-

"""
1.创建django项目，django-admin startproject 项目名
2.创建app         django-admin startapp app名
3.将创建的app在settings中的INSTALLED_APPS配置和加载
4.在app的views.py中自定义函数写逻辑
5.在urls.py中设置路由和相关函数映射
6.运行项目，访问相关路由
    http://127.0.0.1:8000/a/
"""

"""
django获取get/poat参数的正确写法
name = request.GET.get("参数名", "默认值")
name = request.POST.get("参数名", "默认值")

django 返回前端大量数据用json/xml格式
HttpResponse(普通文本) 前台收到的是字符串
JsonResponse(字典)     前台收到的是对象

通过设置ensure_ascii=False,可以解决json字符串的汉子编码
json.dumps(result, ensure_ascii=False)

django中的模板如何加载静态文件
1. 项目根目录下创建static文件夹
2. 在settings最后添加配置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # 'var/www/static/', 在linux系统下存放的地址
]
3. 在模板文件最上方添加一句
{% load static %}
4. 所有资源的路径采用以下方式实现
{% static '资源的相对路径' %}


模板文件中的界面跳转需要通过
{% url '路由别名' %}  动态生成


django的模板继承
作用：将公共代码放入同一个文件，减少子页面的代码量
难点：base.html需要好好设计
1. 创建一个base.html
2. 把公共代码都放进去
3. 不同的部分用 {% block  名字 %} {% endblock %}
4. 子页面
{% extends 'base.html' %}
5. 针对不同部分单独重写即可
{% block middle %}
子页面的代码
{% endblock %}


django操作数据库的方式称为ORM=对象关系映射
目标：不用sql语句，使用面向对象的方式操作数据库
缺点：不支持复杂的sql功能


django使用orm动态生成表
1. 在app的models.py中创建模型类
2. 完成后执行两句命令
python manage.py makemigrations
python manage.py migrate
3. 若后期修改了类中的代码，则需再执行第2步

"""

