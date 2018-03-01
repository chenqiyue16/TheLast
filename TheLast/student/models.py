from django.db import models

# Create your models here.


class StudentInfo(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_identyid = models.CharField(max_length=18)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)


class LinshiInfo(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=20)
    u_identyid = models.CharField(max_length=18)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)
    u_company = models.ForeignKey('company.CompanyInfo')


class QianyueStudent(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=20)
    u_identyid = models.CharField(max_length=18)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)
    u_company = models.ForeignKey('company.CompanyInfo')