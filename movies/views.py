from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.base import ContentFile
from django.db.models import Q

from django.shortcuts import render, render_to_response, redirect, reverse
from django.http import JsonResponse, Http404
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from tools.img_path_name import gen_img_name
from tools.orm2json import object_to_json
from user.models import Movie
from user_like.models import LikeRecord
from error import views as error_views
import math
from django.core.cache import cache
from haystack.views import SearchView

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
                a["like_num"] = info.like_num
                record = False
                if request.user.is_authenticated:
                    likerecords = LikeRecord.objects.raw(
                        f"SELECT * FROM user_like_likerecord where like_movie_id={info.id} and like_user_id={request.user.id} order by id desc limit 1 ")
                    # likerecords = LikeRecord.objects.filter(like_movie=info.id, like_user=request.user.id)
                    # record = likerecords[0].like_record
                    for likerecord in likerecords:
                        record = likerecord.like_record
                a["record"] = record
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
        if cache.get(cate_name):
            movies = cache.get(cate_name)
            # print("缓存中获取")
        else:
            movies = Movie.objects.filter(cate_name=cate_name)
            movies = object_to_json(movies)
            for movie in movies:
                record = False
                # print("2222", info.id, request.user.id)
                if request.user.is_authenticated:
                    likerecords = LikeRecord.objects.raw(
                        f"SELECT * FROM user_like_likerecord where like_movie_id={movie['id']} and like_user_id={request.user.id} order by id desc limit 1 ")
                    # likerecords = LikeRecord.objects.filter(like_movie=info.id, like_user=request.user.id)
                    # record = likerecords[0].like_record
                    for likerecord in likerecords:
                        # print("11111", likerecord.like_record)
                        record = likerecord.like_record
                movie["record"] = f"{record}"
            # cache.set(cate_name, movies, 3600)
            # print("sql语句查询获取")
        # print(len(movies))
        # print(len(movies) / 16)
        all_page = math.ceil(len(movies) / 16)
        # print(all_page)
        if page > all_page:
            return render(request, "404.html")
    else:
        return render(request, "404.html")
    return render(request, "list.html", {
        "movies": movies[(page - 1) * 16:page * 16],
        "movies1": mark_safe(movies[(page - 1) * 16:page * 16]),
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


def movie_ss(request):
    ss_text = request.GET.get("ss_text")
    if ss_text:
        if cache.get(ss_text):
            movie_infos = cache.get(ss_text)
        else:
            # print(ss_text)
            # movie_infos = Movie.objects.raw(f"""SELECT * FROM user_movie where movie_name like '%{ss_text}%'""")
            movie_infos = Movie.objects.filter(movie_name__contains=ss_text)
            # print(movie_infos)
            cache.set(ss_text, movie_infos, 3600)
        if movie_infos:
            page = request.GET.get("page", "1")
            page = int(page)
            print(page)
            all_page = math.ceil(len(movie_infos) / 16)
            # result = {
            #             #     "movies": movie_infos[(page - 1) * 16:page * 16],
            #             #     "all_page": all_page * 10,
            #             #     "page": page,
            #             #     "ss_text": ss_text
            #             # }
            # print(result)
            return render(request, "list.html", {
                "movies": movie_infos[(page - 1) * 16:page * 16],
                "all_page": all_page * 10,
                "page": page,
                "ss_text": ss_text
            })
        else:
            return render(request, "404.html")
    else:
        return render(request, "404.html")


def movie_type_ss(request):
    movie_cate = request.GET.get("movie_cate")
    if movie_cate:

        # movie_infos = Movie.objects.raw(f"""SELECT * FROM user_movie where movie_name like '%{ss_text}%'""")
        if cache.get(movie_cate):
            movie_infos = cache.get(movie_cate)
            # print("缓存中获取")
        else:
            if movie_cate == "其他":
                # movie_infos = Movie.objects.raw(f"""SELECT * FROM user_movie where movie_cate not like '%动作%' and movie_cate not like '%犯罪%' and movie_cate not like '%剧情%' and movie_cate not like '%惊悚%' and movie_cate not like '%喜剧%' and movie_cate not like '%悬疑%' and movie_cate not like '%爱情%'""")
                # # movie_infos = Movie.objects.exclude(movie_cate__contains=["动作", "犯罪", "剧情", "惊悚", "喜剧", "悬疑", "爱情"])
                # movie_infos = serializers.serialize("json", movie_infos)
                movie_infos = Movie.objects.filter(
                    ~Q(movie_cate__contains="动作") & ~Q(movie_cate__contains="犯罪") & ~Q(movie_cate__contains="剧情") & ~Q(
                        movie_cate__contains="惊悚") & ~Q(movie_cate__contains="喜剧") & ~Q(movie_cate__contains="悬疑") & ~Q(
                        movie_cate__contains="爱情"))
                print(movie_infos)
            else:
                movie_infos = Movie.objects.filter(movie_cate__contains=movie_cate)
                print(movie_infos)
            cache.set(movie_cate, movie_infos, 3600)
            # print("sql语句查询获取")
        if movie_infos:
            page = request.GET.get("page", "1")
            page = int(page)
            # print(page)
            all_page = math.ceil(len(movie_infos) / 16)
            # result = {
            #     "movies": movie_infos[(page - 1) * 16:page * 16],
            #     "all_page": all_page * 10,
            #     "page": page,
            #     "movie_cate": movie_cate
            # }
            # print(result)
            # index_url = reverse("index")
            # return redirect(index_url)
            # result["code"] = 001
        else:
            return render(request, "404.html")
    else:
        return render(request, "404.html")
    return render(request, "list.html", {
        "movies": movie_infos[(page - 1) * 16:page * 16],
        "all_page": all_page * 10,
        "page": page,
        "movie_cate": movie_cate
    })



#搜索引擎 全站搜索
class MySearchIndex(SearchView):

    template = 'list.html'
    #我们通过重写extra_context 来定义我们自己的变量，
    #通过看源码，extra_context 默认返回的是空，然后再get_context方法里面，把extra_context
    #返回的内容加到我们self.context字典里
    def extra_context(self):
        context = super(MySearchIndex, self).extra_context()
        search_song = Movie.objects.select_related('movie_name').all()[:self.results_per_page]
        context['search_song']= search_song
        return context

    def create_response(self):
        ss_text = self.request.GET.get("ss_text")
        page = self.request.GET.get("page", "1")
        print(ss_text, page)
        if not ss_text:
            print(self.request.GET.get("ss_text"))
            movie_infos =Movie.objects.filter(movie_name=ss_text)[:self.results_per_page]
            all_page = math.ceil(len(movie_infos) / 16)
            # song_info = Song.objects.all()
            # paginator = Paginator(song_info, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            return render(self.request, "list.html", {
                "movies": movie_infos[(page - 1) * 16:page * 16],
                "all_page": all_page * 10,
                "page": page,
                "ss_text": ss_text
            })




