from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentInfo, LinshiInfo, QianyueStudent


class StudentInfoadmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['u_id', 'u_name', 'u_pwd', 'u_identyid', 'u_sex', 'u_minzu',
                    'u_shouji', 'u_xueyuan', 'u_zhuanye', 'u_nianji','u_xueli', 'u_status'
                    ]


class LinshiInfoInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['u_id', 'u_name', 'u_identyid', 'u_sex', 'u_minzu',
                    'u_shouji', 'u_xueyuan', 'u_zhuanye', 'u_nianji','u_xueli', 'u_status', 'u_company'
                    ]


class QianyueStudentAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['u_id', 'u_name', 'u_identyid', 'u_sex', 'u_minzu',
                    'u_shouji', 'u_xueyuan', 'u_zhuanye', 'u_nianji', 'u_xueli', 'u_status', 'u_company', 'u_date'
                    ]


admin.site.register(StudentInfo, StudentInfoadmin)
admin.site.register(LinshiInfo, LinshiInfoInfoAdmin)
admin.site.register(QianyueStudent, QianyueStudentAdmin)