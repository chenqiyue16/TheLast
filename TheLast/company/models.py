from django.db import models

# Create your models here


class UserInfo(models.Model):
    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_id = models.CharField(max_length=30)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)


class Linshi(models.Model):
    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_id = models.CharField(max_length=30)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)

