from django.db import models

class User(models.Model):
    nickname = models.CharField('昵称', max_length=150)
    openid = models.CharField('ID', max_length=128, primary_key=True)
    head = models.URLField('头像')
    gender = models.CharField('性别', max_length=2, default='保密')
