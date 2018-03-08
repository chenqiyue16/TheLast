# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20180303_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qianyueinfo',
            name='q_danganjieshou',
            field=models.IntegerField(default=False),
        ),
    ]
