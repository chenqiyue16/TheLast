from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
import json
import pdfkit
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def company_login(request):

    return render(request, 'company/company_login.html')


def company_index(request):
    name = request.POST.get('username')
    pwd = request.POST.get('password')
    print(name+':'+pwd)
    context = {'name': 5, 'pwd': pwd}
    return render(request, 'company/index.html', context)


def company_welcome(request):
    return render(request, 'company/welcome.html')


def company_yaoyue(request):
    students = Linshi.objects.all()
    context = {'students': students}
    return render(request,'company/company_yaoyue.html', context)


def test(request):
    return render(request, 'company/test.html')


def testpdf(request):
    print("test")
    pdfkit.from_url('https://www.liuxue86.com/a/2545752.html', 'out1.pdf')
    return redirect('/company/test/')


def company_shanchustudent(request):
    student_list = request.REQUEST.getlist('student_list')
    print(student_list)
    for ls in student_list:
        student = Linshi.objects.get(u_id=ls)
        student.delete()


    return redirect('/company/yaoyue/')

@csrf_exempt
def company_addstudent(request):
    studentid = request.POST.get('studentid', None)

    print(studentid)
    students = UserInfo.objects.filter(u_id=studentid)

    student = Linshi()

    student.u_id = students[0].u_id
    student.u_pwd = students[0].u_pwd
    student.u_name = students[0].u_name
    student.u_xueyuan = students[0].u_xueyuan
    student.u_nianji = students[0].u_nianji
    student.u_xueli = students[0].u_xueli
    student.u_zhuanye = students[0].u_zhuanye
    print('u_name')
    print(student.u_name)
    student.save()
    return HttpResponse(json.dumps({"u_id": student.u_id, "u_name": student.u_name, "u_xueyuan": student.u_xueyuan
                                    , "u_nianji": student.u_nianji, "u_xueli": student.u_xueli, "u_zhuanye": student.u_zhuanye}))