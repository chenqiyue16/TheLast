# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20180304_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='qianyueinfo',
            name='q_com_kuaidi',
            field=models.CharField(null=True, max_length=18),
        ),
        migrations.AddField(
            model_name='qianyueinfo',
            name='q_stu_kuaidi',
            field=models.CharField(null=True, max_length=18),
        ),
    ]
