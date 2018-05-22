from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CompanyInfo,QianyueInfo


class CompanyInfoAdmin(admin.ModelAdmin):
    list_filter = ['c_danweimingcheng']
    search_fields = ['c_danweimingcheng']
    list_display = ['c_username', 'c_password', 'c_danweimingcheng', 'c_zuzhijigoudaima', 'c_danweilishu', 'c_lianxiren',
                    'c_lianxidianhua', 'c_danweixingzhi', 'c_danweihangye', 'c_youxiang','c_tongxindizhi', 'c_pic', 'c_shenhe'
                    ]


class QianyueInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'q_youxiaotianshu', 'q_gongzuodidian', 'q_baodaodizhi', 'q_baodaoshijian', 'q_shiyongqixian', 'q_zhuanzhengxinshui', 'q_gangwei', 'q_zhiweileibie',
                    'q_danganjieshou', 'q_jieshoubumen', 'q_jieshoudanweimingcheng', 'q_jieshouxiangxidizhi', 'q_jieshouyoubian',
                    'q_qianyuezhuangtai', 'q_com_kuaidi', 'q_stu_kuaidi', 'q_student', 'q_company'
                    ]


admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(QianyueInfo, QianyueInfoAdmin)