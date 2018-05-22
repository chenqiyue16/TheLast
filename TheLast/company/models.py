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

    def __str__(self):
        return self.c_danweimingcheng


class QianyueInfo(models.Model):

    q_youxiaotianshu = models.CharField(max_length=10)
    q_gongzuodidian = models.CharField(max_length=30)
    q_baodaodizhi = models.CharField(max_length=30)
    q_baodaoshijian = models.DateField()
    q_shiyongqixian = models.CharField(null=True,blank=True, max_length=20)
    q_zhuanzhengxinshui = models.CharField(null=True, blank=True, max_length=20)
    q_qita = models.CharField(null=True,blank=True,max_length=100)
    q_gangwei = models.CharField(max_length=25)
    q_zhiweileibie = models.CharField(max_length=20)
    q_danganjieshou = models.IntegerField(default=False)
    q_jieshoubumen = models.CharField(null=True, blank=True, max_length=20)
    q_jieshoudanweimingcheng = models.CharField(null=True, blank=True, max_length=20)
    q_jieshouxiangxidizhi = models.CharField(null=True, blank=True, max_length=50)
    q_jieshouyoubian = models.CharField(null=True, blank=True, max_length=8)
    q_jieshouren = models.CharField(null=True, blank=True, max_length=8)
    q_jieshoudianhua = models.CharField(null=True, blank=True, max_length=13)
    q_qianyuezhuangtai = models.IntegerField(default=0)
    q_com_kuaidi = models.CharField(max_length=18, null=True)
    q_stu_kuaidi = models.CharField(max_length=18, null=True)
    q_student = models.ForeignKey('student.StudentInfo', related_name="FAN1")
    q_company = models.ForeignKey(CompanyInfo, related_name="FAN2")




