"""PythonServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from user import views
from movies import views as movie_views
from error import views as error_views
from vip import views as vip_views
from website import views as site_views
from user_like import views as user_like_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("regist/", views.regist, name="regist"),
    path("login/", views.login, name="login"),
    path("forgetpwd/", views.forgetpwd, name="forgetpwd"),
    path("index/", views.index, name="index"),
    path("", views.index, name="index"),  # 首页路由配置
    path("code/", views.get_code, name="code"),
    path("get_v_code/", views.get_v_code, name="get_v_code"),
    path("logout/", views.logout, name="logout"),
    path("update_info/", views.update_info, name="update_info"),
    path("upload/", views.upload, name="upload"),
    path("up_phone/", views.up_phone, name="up_phone"),
    path("sent_phone_code/", views.send_phone_code, name="sent_phone_code"),
    path("update_pwd/", views.update_pwd, name="update_pwd"),
    path("user_pl/", views.user_pl, name="user_pl"),
    path("delete_pl/", views.delete_pl, name="delete_pl"),
    path("add_hf/", views.add_hf, name="add_hf"),
    path("delete_hf/", views.delete_hf, name="delete_hf"),
    # path("up_vip/", views.up_vip, name="up_vip"),


    # url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    path("movie_index/", movie_views.movie_index, name="movie_index"),
    path("movie_list/", movie_views.movie_list, name="movie_list"),
    path("rich_upload/", movie_views.rich_upload, name="rich_upload"),
    path("movie_ss/", movie_views.movie_ss, name="movie_ss"),
    path("movie_type_ss/", movie_views.movie_type_ss, name="movie_type_ss"),

    path("page_not_found/", error_views.page_not_found, name="page_not_found"),
    path("movie_detail/", movie_views.movie_detail, name="movie_detail"),
    path("movie_down_url/", movie_views.movie_down_url, name="movie_down_url"),


    path("recharge_vip/", vip_views.recharge_vip, name="recharge_vip"),
    path("zhifu/", vip_views.zhifu, name="zhifu"),


    # path('', site_views.index),
    path("qq_login/", site_views.qq_login, name="qq_login"),



    path("user-like/", user_like_views.userlike, name="user-like")



]

handler404 = error_views.page_not_found  # 改动2
handler500 = error_views.server_Error  # 改动2
