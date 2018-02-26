# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Linshi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=20)),
                ('u_pwd', models.CharField(max_length=40)),
                ('u_id', models.CharField(max_length=30)),
                ('u_xueyuan', models.CharField(max_length=20)),
                ('u_zhuanye', models.CharField(max_length=20)),
                ('u_nianji', models.CharField(max_length=10)),
                ('u_xueli', models.CharField(max_length=10)),
                ('u_status', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='u_status',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]
