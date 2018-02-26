from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^login/$', views.company_login),
    url(r'^index/$', views.company_index),
    url(r'^welcome/$', views.company_welcome),
    url(r'^yaoyue/$', views.company_yaoyue),
    url(r'^addstudent/$', views.company_addstudent),
    url(r'^test/$', views.test),
    url(r'^testpdf/$', views.testpdf),
    url(r'^shanchustudent/$', views.company_shanchustudent)
]