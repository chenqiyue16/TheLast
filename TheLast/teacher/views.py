from django.shortcuts import render, redirect
from .models import TeacherInfo
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from company.models import CompanyInfo

def index(request):
    user = request.session.get('username')
    if user:
        return render(request, 'teacher/index.html', {'name': user})
    else:
        return redirect('teacher/login/')

def login(request):
    return render(request, 'teacher/teacher_login.html')


def login_handle(request):
    username = request.POST.get('username')
    pwd = request.POST.get('password')
    u_check = request.POST.get('checkout', 0)
    print("uname::"+username)

    teacher = TeacherInfo.objects.filter(t_username=username)
    pwd = TeacherInfo.objects.filter(t_username=username, t_pwd=pwd)
    print(pwd)
    if teacher.exists():
        if pwd:
            red = HttpResponseRedirect('/teacher/index/')
            request.session['username'] = username
            return red
        else:
            context = {'error_name': 0, 'error_password': 1}
            return render(request, 'teacher/teacher_login.html', context)
    else:
        context = {'error_name': 1, 'error_password': 0}
        return render(request, 'teacher/teacher_login.html', context)


def teacher_shenhe(request):
    company = CompanyInfo.objects.filter(c_shenhe=0)
    context = {'companys': company}
    return render(request, 'teacher/teacher_shenhe.html', context)


def teacher_shenhe_handle(request):
    company_list = request.POST.getlist('company_list')
    shenhechenggong = 0
    if company_list:
        for id in company_list:
            CompanyInfo.objects.filter(id=id).update(c_shenhe=1)
            shenhechenggong = 1
    company = CompanyInfo.objects.filter(c_shenhe=0)
    context = {'companys': company, 'shenhechenggong': shenhechenggong}
    return render(request, 'teacher/teacher_shenhe.html', context)