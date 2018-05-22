# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_qianyuestudent_u_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='linshiinfo',
            name='u_minzu',
            field=models.CharField(null=True, max_length=10),
        ),
        migrations.AddField(
            model_name='linshiinfo',
            name='u_sex',
            field=models.CharField(null=True, max_length=4),
        ),
        migrations.AddField(
            model_name='qianyuestudent',
            name='u_minzu',
            field=models.CharField(null=True, max_length=10),
        ),
        migrations.AddField(
            model_name='qianyuestudent',
            name='u_sex',
            field=models.CharField(null=True, max_length=4),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='u_minzu',
            field=models.CharField(null=True, max_length=10),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='u_sex',
            field=models.CharField(null=True, max_length=4),
        ),
    ]
