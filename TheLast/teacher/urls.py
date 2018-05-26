from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^shenhe_(\d*)$', views.teacher_shenhe),
    url(r'^shenhe_(\d+)/$', views.teacher_shenhe),
    url(r'^shenhe_handle/$', views.teacher_shenhe_handle),
    url(r'^refuse_handle/$', views.teacher_refuse_handle),
    url(r'^chartstest/$', views.teacher_chartstest),
    url(r'^chaxun/(\d*)$', views.teacher_chaxun),
    url(r'^chaxun/(\d+)/$', views.teacher_chaxun),
    url(r'^chaxun_sousuo/(\d*)$', views.teacher_chaxun_sousuo),
    url(r'^chaxun_sousuo/(\d+)/$', views.teacher_chaxun_sousuo),
    ]