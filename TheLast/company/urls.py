from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^index/$', views.company_index),
    url(r'^login/$', views.company_login),
    url(r'^login_handle/$', views.login_handle),

    url(r'^yaoyue/$', views.company_yaoyue),
    url(r'^addstudent/$', views.company_addstudent),
    url(r'^chaxunstudent/$', views.company_chaxunstudent),
    url(r'^test/$', views.test),
    url(r'^testpdf/$', views.testpdf),
    url(r'^shanchustudent/$', views.company_shanchustudent),
    url(r'^register1/$', views.company_register1),
    url(r'^checkUname/$', views.company_checkUname),
    url(r'^register2/$', views.company_register2),
    url(r'^registerhandle/$', views.company_registerhandle),
    url(r'^weishenhe/$', views.company_weishenhe),
    url(r'^weishenhe_xiugai/$', views.company_weishenhe_xiugai),
    url(r'^company_info/$', views.company_info),
    url(r'^yaoyue_handle/$', views.company_yaoyue_handle),
    url(r'^chaxun/(\d*)$', views.company_chaxun),
    url(r'^chaxun/(\d+)/$', views.company_chaxun),
    url(r'^chaxun_xiangxixinxi_(\d+)/$', views.company_chaxun_xiangxixinxi),
    url(r'^chaxun_sousuo/(\d*)$', views.company_chaxun_sousuo),
    url(r'^chaxun_sousuo/(\d+)/$', views.company_chaxun_sousuo),
    url(r'^quxiaoyaoyue/$', views.company_quxiaoyaoyue),
]