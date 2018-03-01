# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('c_username', models.CharField(max_length=30)),
                ('c_password', models.CharField(max_length=40)),
                ('c_danweimingcheng', models.CharField(max_length=30)),
                ('c_zuzhijigoudaima', models.IntegerField()),
                ('c_danweilishu', models.CharField(max_length=20)),
                ('c_lianxiren', models.CharField(max_length=8)),
                ('c_youxiang', models.CharField(max_length=28)),
                ('c_lianxidianhua', models.CharField(max_length=11)),
                ('c_danweixingzhi', models.CharField(max_length=40)),
                ('c_danweihangye', models.CharField(max_length=40)),
                ('c_tongxindizhi', models.CharField(max_length=50)),
                ('c_pic', models.ImageField(upload_to='zhizhao')),
                ('c_shenhe', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QianyueInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('q_youxiaotianshu', models.CharField(max_length=10)),
                ('q_gongzuodidian', models.CharField(max_length=30)),
                ('q_baodaodizhi', models.CharField(max_length=30)),
                ('q_baodaoshijian', models.DateField()),
                ('q_shiyongqixian', models.CharField(blank=True, max_length=20, null=True)),
                ('q_zhuanzhengxinshui', models.CharField(blank=True, max_length=20, null=True)),
                ('q_qita', models.CharField(blank=True, max_length=100, null=True)),
                ('q_gangwei', models.CharField(max_length=25)),
                ('q_zhiweileibie', models.CharField(max_length=20)),
                ('q_danganjieshou', models.BooleanField(default=False)),
                ('q_jieshoubumen', models.CharField(blank=True, max_length=20, null=True)),
                ('q_jieshoudanweimingcheng', models.CharField(blank=True, max_length=20, null=True)),
                ('q_jieshouxiangxidizhi', models.CharField(blank=True, max_length=50, null=True)),
                ('q_jieshouyoubian', models.CharField(blank=True, max_length=8, null=True)),
                ('q_jieshouren', models.CharField(blank=True, max_length=8, null=True)),
                ('q_jieshoudianhua', models.CharField(blank=True, max_length=13, null=True)),
                ('q_qianyuezhuangtai', models.IntegerField(default=0)),
                ('q_company', models.ForeignKey(to='company.CompanyInfo')),
            ],
        ),
    ]
