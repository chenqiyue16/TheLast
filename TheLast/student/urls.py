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
    url(r'^qianyuexinxi/$', views.student_qianyuexinxi)
    ]