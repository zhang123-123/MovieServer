from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, render_to_response, redirect, reverse
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from tools.img_path_name import gen_img_name
from user.models import Movie
from error import views as error_views
import math


# Create your views here.


def movie_index(request):
    # result = {"code": "001",
    #           "message": "成功",
    #           "data": [{"cate_name": "综合电影", "movie_info": [{
    #               "movie_name": "2019年国产动作片《九龙不败》HD高清国语中字",
    #               "img": "",
    #               "movie_down_url": ""
    #           }, {}, {}, {}]},
    #                    {"cate_name": "经典电影", "movie_info": [{
    #                        "movie_name": "2019年国产动作片《九龙不败》HD高清国语中字",
    #                        "img": "",
    #                        "movie_down_url": ""
    #                    }, {}, {}, {}]},
    #                    {"cate_name": "国内电影", "movie_info": [{
    #                        "movie_name": "2019年国产动作片《九龙不败》HD高清国语中字",
    #                        "img": "",
    #                        "movie_down_url": ""
    #                    }, {}, {}, {}]},
    #                    {"cate_name": "欧美电影", "movie_info": [{
    #                        "movie_name": "2019年国产动作片《九龙不败》HD高清国语中字",
    #                        "img": "",
    #                        "movie_down_url": ""
    #                    }, {}, {}, {}]}
    #                    ]
    #           }
    result = {}
    movies = Movie.objects.raw('SELECT * FROM user_movie')
    print(movies)
    cates = []
    for movie in movies:
        # print(movie.cate_name)
        if movie.cate_name not in cates:
            cates.append(movie.cate_name)
    if cates:
        result["code"] = "001"
        result["message"] = "查询成功"
        result["data"] = {}
    for cate in cates:
        movie_infos = Movie.objects.raw(
            f"SELECT * FROM user_movie where cate_name='{cate}' order by down desc limit 4 ")

        # if movie_infos:
        #     result["code"] = "002"
        #     result["message"] = "查询成功"
        #     result["data"] = []
        #     a = {}
        #     movie_info11 = []
        #     b = {}
        #     for movie_info in movie_infos:
        #         a["movie_name"] = movie_info.movie_name
        #         a["img"] = movie_info.img
        #         a["movie_down_url"] = movie_info.movie_down_url
        #         movie_info11.append(a)
        #         if cate not in b.values():
        #             b["cate_name"] = cate
        #             b["movie_info"] = [a]
        #         else:
        #             b["movie_info"].append(a)
        #         result["data"].append(b)
        if movie_infos:
            result["data"][cate] = []
            for info in movie_infos:
                a = {}
                a['id'] = info.id
                a['cate_title'] = info.cate_name
                a['movie_name'] = info.movie_name
                a['movie_down_url'] = info.movie_down_url
                a['look'] = info.look
                a['mark'] = info.mark
                a['down'] = info.down
                a['movie_img'] = info.movie_img
                result['data'][cate].append(a)

        else:
            result["code"] = "002"
            result["message"] = "查询失败"
    return JsonResponse(result)


def movie_list(request):
    cate_name = request.GET.get("cate_name")
    page = request.GET.get("page", "1")
    page = int(page)
    if cate_name:
        movies = Movie.objects.filter(cate_name=cate_name)
        print(len(movies))
        print(len(movies) / 16)
        all_page = math.ceil(len(movies) / 16)
        print(all_page)
        if page > all_page:
            return render(request, "404.html")
    else:
        return render(request, "404.html")
    return render(request, "list.html", {
        "movies": movies[(page - 1) * 16:page * 16],
        "all_page": all_page * 10,
        "page": page,
        "cate_name": cate_name
    })


def movie_detail(request):
    """
    print(cate_name, movie_name, movie_img, movie_down_url, trans_name, movie_title, movie_age, movie_place, movie_cate, movie_language, movie_subtitle, movie_release_time,
              movie_imdb, movie_douban, movie_file_format, movie_video_size, movie_file_size, movie_length,
              movie_director, movie_screenwriter, movie_starring, movie_label, movie_introduction)
    """
    movie_id = request.GET.get("movie_id")
    if movie_id:
        movies = Movie.objects.filter(id=movie_id)
        if movies:
            movie = movies[0]
            return render(request, "movie_detail.html", {"movie": movie})
    return render(request, "movie_detail.html")


def movie_down_url(request):
    result = {}
    # movie_name = request.GET.get("movie_name")
    movie_id = request.GET.get("movie_id")
    print("11111111111")
    print(movie_id)
    if request.user.is_authenticated:

        if request.user.vip >= 1:
            if movie_id:
                movies = Movie.objects.filter(id=movie_id)
                if movies:
                    movie = movies[0]
                    result["code"] = "001"
                    result["message"] = "查询成功"
                    result["datas"] = {}
                    result["datas"]["movie_down_url"] = movie.movie_down_url
                    result["datas"]["id"] = movie.id
                    result["datas"]["movie_img"] = movie.movie_img
                    result["datas"]["movie_name"] = movie.movie_name
                    result["datas"]["look"] = movie.look
                    result["datas"]["mark"] = movie.mark
                    result["datas"]["mark"] = movie.down
                else:
                    result["code"] = "003"
                    result["message"] = "id不存在"
            else:
                result["code"] = "002"
                result["message"] = "id输入不正确"
        else:
            result["code"] = "005"
            result["message"] = "等级不够"
    else:
        result["code"] = "004"
        result["message"] = "未登录"
        result["login_url"] = reverse("login")
        print(reverse("login"))
    print(result)
    return JsonResponse(result)


@csrf_exempt
def rich_upload(request):
    if request.method == 'POST':
        """
        {
  "code": 0 //0表示成功，其它失败
  ,"msg": "" //提示信息 //一般上传失败后返回
  ,"data": {
    "src": "图片路径"
    ,"title": "图片名称" //可选
  }
}
        """
        file_content = request.FILES['file'].read()
        # print(file_content)
        ext = request.FILES['file'].name.split(".")[-1]
        new_img_name = request.FILES['file'].name
        # new_img_name = gen_img_name(request.user.username) + "." + ext
        with open(f"static/rich_upload/{new_img_name}", "wb") as f:
            f.write(file_content)
        print(file_content, "1111111", type(file_content))
        # print(a)
        result = {
            'code': 0,
            'msg': '上传成功',
            "data": {
                "src": f"/static/rich_upload/{new_img_name}",
                "title": new_img_name
            }
        }

        return JsonResponse(result)
    elif request.method == 'GET':
        return render(request, 'upload.html')
