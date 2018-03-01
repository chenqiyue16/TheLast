# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinshiInfo',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=20)),
                ('u_identyid', models.CharField(max_length=18)),
                ('u_xueyuan', models.CharField(max_length=20)),
                ('u_zhuanye', models.CharField(max_length=20)),
                ('u_nianji', models.CharField(max_length=10)),
                ('u_xueli', models.CharField(max_length=10)),
                ('u_status', models.CharField(max_length=5)),
                ('u_company', models.ForeignKey(to='company.CompanyInfo')),
            ],
        ),
        migrations.CreateModel(
            name='QianyueStudent',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=20)),
                ('u_identyid', models.CharField(max_length=18)),
                ('u_xueyuan', models.CharField(max_length=20)),
                ('u_zhuanye', models.CharField(max_length=20)),
                ('u_nianji', models.CharField(max_length=10)),
                ('u_xueli', models.CharField(max_length=10)),
                ('u_status', models.CharField(max_length=5)),
                ('u_company', models.ForeignKey(to='company.CompanyInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=20)),
                ('u_pwd', models.CharField(max_length=40)),
                ('u_identyid', models.CharField(max_length=18)),
                ('u_xueyuan', models.CharField(max_length=20)),
                ('u_zhuanye', models.CharField(max_length=20)),
                ('u_nianji', models.CharField(max_length=10)),
                ('u_xueli', models.CharField(max_length=10)),
                ('u_status', models.CharField(max_length=5)),
            ],
        ),
    ]
