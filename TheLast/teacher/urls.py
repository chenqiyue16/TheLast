from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^shenhe/$', views.teacher_shenhe),
    url(r'^shenhe_handle/$', views.teacher_shenhe_handle),
    url(r'^chartstest/$', views.teacher_chartstest),
    ]