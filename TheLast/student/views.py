from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import *
from company.models import CompanyInfo,QianyueInfo
from django.core.paginator import Paginator


def index(request):
    student_id = request.session.get('student_id')
    if student_id:
        u_student = StudentInfo.objects.filter(u_id=student_id)
        u_status = u_student[0].u_status
        context = {'u_status': u_status}
        return render(request, 'student/index.html', context)
    else:
        return redirect('/student/login/')


def student_login(request):
    return render(request, 'student/student_login.html')


def login_handle(request):
    u_id = request.POST.get('username')
    u_pwd = request.POST.get('password')
    u_check = request.POST.get('checkout', 0)
    print("uname::"+u_id)

    student = StudentInfo.objects.filter(u_id=u_id)
    pwd = StudentInfo.objects.filter(u_id=u_id, u_pwd=u_pwd)
    print(pwd)
    if student.exists():
        if pwd:
            # url = request.COOKIES.get('url', '/')
            u_status = student[0].u_status
            if u_status == '未签约':
                red = HttpResponseRedirect('/student/index/')
            else:
                red = HttpResponseRedirect('/student/weishenhe/')
            if u_check == 1:
                red.set_cookie('student_id', u_id)
            else:
                red.set_cookie('student_id', '', max_age=-1)

            request.session['student_id'] = u_id
            request.session['student_name'] = student[0].u_name
            request.session['student_status'] = student[0].u_status
            return red
        else:
            context = {'error_name': 0, 'error_password': 1}
            return render(request, 'student/student_login.html', context)
    else:
        context = {'error_name': 1, 'error_password': 0}
        return render(request, 'student/student_login.html', context)


def student_chakanyaoyue(request, pIndex):
    student_id = request.session.get('student_id')
    print(student_id)
    if student_id:
        students = StudentInfo.objects.filter(u_status='未签约', u_id=student_id)
        if students:
            yaoyues = QianyueInfo.objects.filter(q_student_id=student_id, q_qianyuezhuangtai=0, q_student_id__u_status='未签约').values('q_company_id', 'q_company_id__c_zuzhijigoudaima', 'q_company_id__c_danweimingcheng',
                                                                             'q_company_id__c_lianxiren', 'q_company_id__c_lianxidianhua',
                                                                             'q_company_id__c_danweilishu', 'q_company_id__c_danweixingzhi',
                                                                             'q_company_id__c_danweihangye')
            if yaoyues:
                p = Paginator(yaoyues, 1)
                if pIndex == '':
                    pIndex = 1
                pIndex = int(pIndex)
                list2 = p.page(pIndex)
                plist = p.page_range
                context = {'plist': plist, 'yaoyues': list2, 'pindex': pIndex}
                return render(request, 'student/student_chakanyaoyue.html', context)
            else:

                return render(request, 'student/student_chakanyaoyue.html')
        else:
            return HttpResponse('hello')
    else:
        return redirect('/company/login/')


def student_chakanxiangxixinxi(request, id):
    student_id = request.session.get('student_id')
    print(student_id)
    print(id)
    if student_id:
        qianyues = QianyueInfo.objects.filter(q_student_id=student_id, q_company_id=id).values('q_company_id__c_danweimingcheng', 'q_gangwei',
                                                                             'q_zhiweileibie', 'q_gongzuodidian',
                                                                             'q_baodaodizhi', 'q_baodaoshijian',
                                                                             'q_shiyongqixian', 'q_zhuanzhengxinshui',
                                                                              'q_danganjieshou', 'q_jieshoubumen',
                                                                              'q_jieshoudanweimingcheng', 'q_jieshouxiangxidizhi',
                                                                              'q_jieshouren', 'q_jieshoudianhua', 'q_jieshouyoubian',
                                                                              'q_qita')
        context = {'qianyue':qianyues[0]}
        return render(request, 'student/student_chakanxiangxixinxi.html', context)
    else:
        return redirect('/student/login/')


def student_jieshouyaoyue(request):
    student_id = request.session.get('student_id')
    if student_id:
        company_id = request.POST.get('yaoyue_list')
        print(company_id)
        c_id = company_id
        StudentInfo.objects.filter(u_id=student_id).update(u_status='已签约')
        QianyueInfo.objects.filter(q_student_id=student_id).update(q_qianyuezhuangtai=-1)
        QianyueInfo.objects.filter(q_company_id=c_id, q_student_id=student_id).update(q_qianyuezhuangtai=1)
        qianyuestudent = QianyueStudent()
        student = StudentInfo.objects.get(u_id=student_id)
        qianyuestudent.u_name = student.u_name
        qianyuestudent.u_id = student.u_id
        qianyuestudent.u_xueli = student.u_xueli
        qianyuestudent.u_nianji = student.u_nianji
        qianyuestudent.u_zhuanye = student.u_zhuanye
        qianyuestudent.u_xueyuan = student.u_xueyuan
        qianyuestudent.u_identyid = student.u_identyid
        qianyuestudent.u_status = student.u_status
        qianyuestudent.u_company_id = c_id
        qianyuestudent.save()
        return HttpResponse('chenggong！')
        #return render(request, 'student/student_jieshouyaoyue.html')
    else:
        return redirect('/student/login/')


def student_qianyuexinxi(request):
    student_id = request.session.get('student_id')
    if student_id:

        qianyue = QianyueInfo.objects.get(q_student_id=student_id, q_qianyuezhuangtai=1)
        student = QianyueStudent.objects.get(u_id=student_id)
        context = {'qianyue': qianyue, 'student': student}
        return render(request, 'student/student_qianyuexinxi.html', context)
    else:
        return redirect('/student/login/')