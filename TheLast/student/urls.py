from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^login/$', views.student_login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^chakanyaoyue_(\d*)$', views.student_chakanyaoyue),
    url(r'^chakanyaoyue_(\d+)/$', views.student_chakanyaoyue),
    url(r'^chakanxiangxixinxi_(\d*)$', views.student_chakanxiangxixinxi),
    url(r'^chakanxiangxixinxi_(\d+)/$', views.student_chakanxiangxixinxi),
    url(r'^jieshouyaoyue/$', views.student_jieshouyaoyue),
    url(r'^qianyuexinxi/$', views.student_qianyuexinxi),
    url(r'^wuliuxinxiluru/$', views.student_wuliuxinxiluru),
    url(r'^wuliuxinxichakan/$', views.student_wuliuxinxichakan),
    url(r'^wuliuxinxibaocun/$', views.student_wuliuxinxibaocun),
    url(r'^shujutongji/$', views.student_shujutongji),
    url(r'^xiugaimima/$', views.student_xiugaimima),
    url(r'^xiugaimima_handle/$', views.student_xiugaimima_handle),
    url(r'^xiugaimima_check/$', views.student_xiugaimima_check),
    url(r'^tuichu/$', views.student_tuichu),
    ]