from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# PythonUser是表名
# 属性表示列名
# python manage.py makemigrations  将类转换成sql相关语句
# python manage.py migrate  生成表
# class PythonUser(models.Model):
class PythonUser(AbstractUser):
    # email = models.CharField(max_length=100, null=True, blank=True)
    # pwd = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    # join_time = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True 自动添加当前时间
    age = models.IntegerField(default=0)
    img = models.ImageField(upload_to="upload/", default="static/upload/a.jpg", max_length=100)
    # upload_to  图像上传地址
    # 等级
    vip = models.IntegerField(default=0, null=True, blank=True)
    login_type = models.CharField(max_length=50, null=True, blank=True)
    all_price = models.FloatField(default=0)


class Movie(models.Model):
    cate_name = models.CharField(max_length=100, null=True, blank=True)
    movie_name = models.CharField(max_length=100, null=True, blank=True)
    movie_img = models.CharField(max_length=255, null=True, blank=True)
    movie_down_url = models.CharField(max_length=255, null=True, blank=True)
    trans_name = models.CharField(max_length=255, null=True, blank=True)
    movie_title = models.CharField(max_length=255, null=True, blank=True)
    movie_age = models.CharField(max_length=255, null=True, blank=True)
    movie_place = models.CharField(max_length=255, null=True, blank=True)
    movie_cate = models.CharField(max_length=255, null=True, blank=True)
    movie_language = models.CharField(max_length=255, null=True, blank=True)
    movie_subtitle = models.CharField(max_length=255, null=True, blank=True)
    movie_release_time = models.CharField(max_length=255, null=True, blank=True)
    movie_imdb = models.CharField(max_length=255, null=True, blank=True)
    movie_douban = models.CharField(max_length=255, null=True, blank=True)
    movie_file_format = models.CharField(max_length=255, null=True, blank=True)
    movie_video_size = models.CharField(max_length=255, null=True, blank=True)
    movie_file_size = models.CharField(max_length=255, null=True, blank=True)
    movie_length = models.CharField(max_length=255, null=True, blank=True)
    movie_director = models.TextField(null=True, blank=True)
    movie_screenwriter = models.TextField(null=True, blank=True)

    movie_starring = models.TextField(null=True, blank=True)
    movie_label = models.CharField(max_length=255, null=True, blank=True)
    movie_introduction = models.TextField(max_length=255, null=True, blank=True)

    # 浏览量
    look = models.IntegerField(default=0, null=True, blank=True)
    # 点击量
    mark = models.IntegerField(default=0, null=True, blank=True)
    # 下载量
    down = models.IntegerField(default=0, null=True, blank=True)
    # 点赞量
    like_num = models.IntegerField(default=0, null=True, blank=True)



class Mark(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    movie_date = models.DateTimeField(auto_now_add=True)


# 评论
class Comment(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    movie_date = models.DateTimeField(auto_now=True)
    user_comment_content = models.CharField(max_length=255)


class Huifu(models.Model):
    comment_user_id = models.IntegerField()
    movie_id = models.IntegerField()
    hf_date = models.DateTimeField(auto_now_add=True)
    hf_content = models.TextField(default="")
    comment_id = models.IntegerField(default=0)
    hf_user_id = models.IntegerField()

class Pay(models.Model):
    out_trade_no = models.CharField(max_length=50)  # 支付后
    trade_no = models.CharField(max_length=50)  # 支付前
    user_id = models.IntegerField()
    pay_date = models.DateTimeField(auto_now_add=True)
    pay_price = models.FloatField(default=0)
    pay_status = models.IntegerField()
    # -1 支付失败  0 尚未支付  1 支付成功


