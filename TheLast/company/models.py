from django.db import models

# Create your models here


class CompanyInfo(models.Model):
    c_username = models.CharField(max_length=30)
    c_password = models.CharField(max_length=40)
    c_danweimingcheng = models.CharField(max_length=30)
    c_zuzhijigoudaima = models.IntegerField()
    c_danweilishu = models.CharField(max_length=20)
    c_lianxiren = models.CharField(max_length=8)
    c_youxiang = models.CharField(max_length=28)
    c_lianxidianhua = models.CharField(max_length=11)
    c_danweixingzhi = models.CharField(max_length=40)
    c_danweihangye = models.CharField(max_length=40)
    c_tongxindizhi = models.CharField(max_length=50)
    c_pic = models.ImageField(upload_to='zhizhao')
    c_shenhe = models.IntegerField(default=0)


class QianyueInfo(models.Model):

    q_youxiaotianshu = models.CharField(max_length=10)
    q_gongzuodidian = models.CharField(max_length=30)
    q_baodaodizhi = models.CharField(max_length=30)
    q_baodaoshijian = models.DateField()
    q_shiyongqixian = models.CharField(null=True,blank=True, max_length=20)
    q_zhuanzhengxinshui = models.CharField(null=True, blank=True, max_length=20)
    q_qita = models.CharField(null=True,blank=True,max_length=100)
    q_zhiweileibie = models.CharField(max_length=20)
    q_danganjieshou = models.BooleanField(default=False)
    q_jieshoubumen = models.CharField(max_length=20)
    q_jieshoudanweimingcheng = models.CharField(max_length=20)
    q_jieshouxiangxidizhi = models.CharField(max_length=50)
    q_jieshouyoubian = models.IntegerField()
    q_jieshouren = models.CharField(max_length=8)
    q_jieshoudianhua = models.CharField(max_length=13)
    q_student = models.ForeignKey('student.StudentInfo')
    q_company = models.ForeignKey(CompanyInfo)

