# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20180313_0553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qianyuestudent',
            name='u_com_kuaidi',
        ),
        migrations.RemoveField(
            model_name='qianyuestudent',
            name='u_stu_kuaidi',
        ),
    ]
