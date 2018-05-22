from django.db import models

# Create your models here.


class StudentInfo(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_identyid = models.CharField(max_length=18)
    u_sex = models.CharField(max_length=4, null=True)
    u_minzu = models.CharField(max_length=10, null=True)
    u_shouji = models.CharField(max_length=11, null=True)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)

    def __str__(self):
        return self.u_name


class LinshiInfo(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=20)
    u_identyid = models.CharField(max_length=18)
    u_sex = models.CharField(max_length=4, null=True)
    u_minzu = models.CharField(max_length=10, null=True)
    u_shouji = models.CharField(max_length=11, null=True)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)
    u_company = models.ForeignKey('company.CompanyInfo')

    def __str__(self):
        return self.u_name


class QianyueStudent(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=20)
    u_identyid = models.CharField(max_length=18)
    u_sex = models.CharField(max_length=4, null=True)
    u_minzu = models.CharField(max_length=10, null=True)
    u_shouji = models.CharField(max_length=11, null=True)
    u_xueyuan = models.CharField(max_length=20)
    u_zhuanye = models.CharField(max_length=20)
    u_nianji = models.CharField(max_length=10)
    u_xueli = models.CharField(max_length=10)
    u_status = models.CharField(max_length=5)
    u_date = models.DateField(null=True, auto_now=True)
    u_company = models.ForeignKey('company.CompanyInfo')

    def __str__(self):
        return self.u_name

