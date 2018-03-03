# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_qianyueinfo_q_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qianyueinfo',
            name='q_company',
            field=models.ForeignKey(to='company.CompanyInfo', related_name='FAN2'),
        ),
        migrations.AlterField(
            model_name='qianyueinfo',
            name='q_student',
            field=models.ForeignKey(to='student.StudentInfo', related_name='FAN1'),
        ),
    ]
