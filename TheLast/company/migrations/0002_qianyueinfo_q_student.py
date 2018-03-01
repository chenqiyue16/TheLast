# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qianyueinfo',
            name='q_student',
            field=models.ForeignKey(to='student.StudentInfo'),
        ),
    ]
