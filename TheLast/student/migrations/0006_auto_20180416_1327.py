# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20180407_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='linshiinfo',
            name='u_shouji',
            field=models.CharField(null=True, max_length=11),
        ),
        migrations.AddField(
            model_name='qianyuestudent',
            name='u_shouji',
            field=models.CharField(null=True, max_length=11),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='u_shouji',
            field=models.CharField(null=True, max_length=11),
        ),
    ]
