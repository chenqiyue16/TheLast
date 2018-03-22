# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20180313_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='qianyuestudent',
            name='u_date',
            field=models.DateField(null=True, auto_now=True),
        ),
    ]
