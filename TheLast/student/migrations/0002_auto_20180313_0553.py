# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qianyuestudent',
            name='u_com_kuaidi',
            field=models.CharField(null=True, max_length=18),
        ),
        migrations.AddField(
            model_name='qianyuestudent',
            name='u_stu_kuaidi',
            field=models.CharField(null=True, max_length=18),
        ),
    ]
