from django.db import models

# Create your models here.


class TeacherInfo(models.Model):
    t_username = models.CharField(max_length=20)
    t_pwd = models.CharField(max_length=40)
