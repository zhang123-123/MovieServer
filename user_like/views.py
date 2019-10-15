from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import LikeRecord
from user.models import PythonUser, Movie

# Create your views here.
@csrf_exempt
def userlike(request):
    result = {}
    is_like = request.POST.get("is_like")
    movie_id = request.POST.get("movie_id")
    print(is_like, movie_id)
    print(request.user.is_authenticated)
    print(request.user, type(request.user))
    print(request.user.id, type(request.user.id))
    if request.user.is_authenticated:
        # 点赞
        # 记录点赞状态
        movies = Movie.objects.filter(id=movie_id)
        movie = movies[0]
        likerecode = LikeRecord()
        likerecode.like_user = request.user
        likerecode.like_movie = movie

        if is_like == "true":
            is_like = True
            print("")
            movie.like_num += 1
            result["message"] = "点赞成功"
        # 取消点赞
        elif is_like == "false":
            is_like = False
            movie.like_num -= 1
            result["message"] = "取消点赞"
        likerecode.like_record = is_like
        likerecode.save()
        movie.save()
        result["code"] = "001"
        result["like_num"] = movie.like_num
    else:
        result["code"] = "002"
        result["message"] = "请先登录"
    print(result)
    return JsonResponse(result)

