from django.db import models
from user.models import PythonUser, Movie


# Create your models here.

class LikeRecord(models.Model):
    like_user = models.ForeignKey("user.PythonUser", on_delete=models.DO_NOTHING)
    like_movie = models.ForeignKey("user.Movie", on_delete=models.DO_NOTHING)
    like_time = models.DateTimeField(auto_now_add=True)
    like_record = models.BooleanField(default=False)


# class MovieLikeCount(models.Model):
#     movie = models.ForeignKey("user.Movie", on_delete=models.CASCADE)
#     like_num = models.IntegerField(default=0)
