from django.shortcuts import render, redirect
from .models import TeacherInfo
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from company.models import CompanyInfo
from student.models import QianyueStudent
from django.db.models.aggregates import Count

def index(request):
    user = request.session.get('teachername')
    if user:
        return render(request, 'teacher/index.html', {'name': user})
    else:
        return redirect('/teacher/login/')


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
            request.session['teachername'] = username
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


class DateTimeTest(object):
    def __init__(self, year, month , day, c):
        self.year = year
        self.month = month
        self.day = day
        self.count = c


def teacher_chartstest(request):
    students = QianyueStudent.objects.all()
    for student in students:
        print(student.u_date.month)
    benkeset = QianyueStudent.objects.values_list('u_date').annotate(Count('u_date')).filter(u_xueli='大学本科').order_by('u_date')
    shuoshiset = QianyueStudent.objects.values_list('u_date').annotate(Count('u_date')).filter(u_xueli='硕士研究生').order_by('u_date')
    datelist1 = []
    datelist2 = []
    for s in benkeset:
        date = DateTimeTest(s[0].year, s[0].month, s[0].day, s[1])
        datelist1.append(date)
    for s in shuoshiset:
        date = DateTimeTest(s[0].year, s[0].month, s[0].day, s[1])
        datelist2.append(date)
    for d in datelist1:
        print(d.year, d.month, d.day, d.count)
    zhuanyeset1 = QianyueStudent.objects.values_list('u_zhuanye').annotate(Count('u_zhuanye')).filter(u_xueli='大学本科')
    zhuanyeset2 = QianyueStudent.objects.values_list('u_zhuanye').annotate(Count('u_zhuanye')).filter(u_xueli='硕士研究生')
    print(zhuanyeset1)
    zhuanyeset1_dict = {}
    zhuanyeset2_dict = {}
    sum = 0
    for set1 in zhuanyeset1:
        sum += set1[1]
    for set1 in zhuanyeset1:
        zhuanyeset1_dict[set1[0]] = (set1[1]*100)/sum
    sum = 0
    for set2 in zhuanyeset2:
        sum += set2[1]
    for set2 in zhuanyeset2:
        zhuanyeset2_dict[set2[0]] = (set2[1]*100)/sum
    print(zhuanyeset1_dict)
    context = {'datelist1': datelist1, 'datelist2': datelist2, 'zhuanyeset1_dict': zhuanyeset1_dict, 'zhuanyeset2_dict': zhuanyeset2_dict}

    return render(request, 'teacher/teacher_chartstest.html', context)

    # u_id = request.session.get('u_id')
    # set = QianyueStudent.objects.values_list('u_nianji').annotate(Count('u_nianji')).filter(u_xueli='大学本科', u_company_id=u_id).order_by('u_nianji')
    # set1 = QianyueStudent.objects.values_list('u_nianji').annotate(Count('u_nianji')).filter(u_xueli='硕士研究生', u_company_id=u_id).order_by('u_nianji')
    # set2 = QianyueStudent.objects.distinct().values('u_nianji').order_by('u_nianji')
    #

    # benkelist = []
    # benkenianjilist={}
    # shuoshilist = []
    # shuoshinianjilist={}
    # nianjilist = []
    # for s2 in set2:
    #     nianjilist.append(s2['u_nianji'])
    #
    # for s1 in set1:
    #     shuoshinianjilist[s1[0]] = s1[1]
    # for s in set:
    #     benkenianjilist[s[0]] = s[1]
    # for nianji in nianjilist:
    #     if nianji in shuoshinianjilist:
    #         shuoshilist.append(shuoshinianjilist[nianji])
    #     else:
    #         shuoshilist.append(0)
    # for nianji in nianjilist:
    #     if nianji in nianjilist:
    #         benkelist.append(benkenianjilist[nianji])
    #     else:
    #         benkelist.append(0)
    #

    # context = {'nianjilist': nianjilist, 'benkelist': benkelist, 'shuoshilist': shuoshilist,'zhuanyeset1_dict': zhuanyeset1_dict, 'zhuanyeset2_dict': zhuanyeset2_dict}
    # return render(request, 'company/company_chartstest.html', context)