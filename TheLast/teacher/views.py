from django.shortcuts import render, redirect
from .models import TeacherInfo
from student.models import LinshiInfo, StudentInfo, QianyueStudent
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from company.models import CompanyInfo
from student.models import QianyueStudent
from django.db.models.aggregates import Count
from django.core.paginator import Paginator
import json
import urllib
import urllib.request
import base64
import hashlib
import urllib.parse
from company.models import CompanyInfo,QianyueInfo
from django.conf import settings
import csv


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
    #print("uname::"+username)

    teacher = TeacherInfo.objects.filter(t_username=username)
    pwd = TeacherInfo.objects.filter(t_username=username, t_pwd=pwd)
    #print(pwd)
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


def teacher_shenhe(request, pIndex):
    company = CompanyInfo.objects.filter(c_shenhe=0)
    p = Paginator(company, 5)
    if pIndex == '':
        pIndex = 1
    pIndex = int(pIndex)
    list2 = p.page(pIndex)
    plist = p.page_range
    context = {'plist': plist, 'companys': list2, 'p': pIndex}
    return render(request, 'teacher/teacher_shenhe.html', context)


def teacher_shenhe_handle(request):
    url = 'http://v.juhe.cn/sms/send'
    # 准备一下头
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    company_list = request.POST.getlist('company_list')
    shenhechenggong = 0
    if company_list:
        for id in company_list:
            company = CompanyInfo.objects.get(id=id)
            company.c_shenhe = 1
            company.save()
            shenhechenggong = 1
            values = {
                'mobile': company.c_lianxidianhua,
                'tpl_id': 68786,
                'key': '0e9b1c796985a4c51cd563b0077fb8f0',
            }
            # 将字典格式化成能用的形式
            data = urllib.parse.urlencode(values).encode('utf-8')
            # 创建一个request,放入我们的地址、数据、头
            rt = urllib.request.Request(url, data, headers)
            html = urllib.request.urlopen(rt).read().decode('utf-8')
            print(json.loads(html)['result'])
            print(json.loads(html)['error_code'])
    company = CompanyInfo.objects.filter(c_shenhe=0)
    context = {'companys': company, 'shenhechenggong': shenhechenggong}
    return render(request, 'teacher/teacher_shenhe.html', context)


def teacher_refuse_handle(request):
    company_list = request.POST.get('company_list')
    dianhua = request.POST.get('dianhua')
    url = 'http://v.juhe.cn/sms/send'
    # 准备一下头
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    values = {
        'mobile': dianhua,
        'tpl_id': 68787,
        'key': '0e9b1c796985a4c51cd563b0077fb8f0',
    }
    # 将字典格式化成能用的形式
    data = urllib.parse.urlencode(values).encode('utf-8')
    # 创建一个request,放入我们的地址、数据、头
    rt = urllib.request.Request(url, data, headers)
    html = urllib.request.urlopen(rt).read().decode('utf-8')
    print(json.loads(html)['result'])
    print(json.loads(html)['error_code'])

    if company_list:
        CompanyInfo.objects.filter(id=company_list).update(c_shenhe=-1)
    return HttpResponse(json.dumps({"msg": '拒绝成功'}))


def teacher_chaxun_sousuo(request, pIndex):

    queryset = {}
    kwargs = {}

    #print(id)
    page = request.GET.get('page', None)
    queryset['u_name'] = request.GET.get('u_name', None)
    queryset['u_id'] = request.GET.get('u_id', None)
    queryset['u_identyid'] = request.GET.get('u_identyid', None)
    queryset['u_sex'] = request.GET.get('u_sex', None)
    queryset['u_xueyuan'] = request.GET.get('u_xueyuan', None)
    queryset['u_zhuanye'] = request.GET.get('u_zhuanye', None)
    queryset['u_xueli'] = request.GET.get('u_xueli', None)
    queryset['u_status'] = request.GET.get('u_qianyuezhuangtai', None)
    for (k, v) in queryset.items():
        if v != '':
            kwargs[k] = v
    #print(kwargs)
    filepath = settings.MEDIA_ROOT + '/' + 'writer.csv'
    students = StudentInfo.objects.filter(**kwargs).values('u_name', 'u_id', 'u_identyid', 'u_sex', 'u_xueyuan', 'u_zhuanye','u_nianji'
                                                          , 'u_xueli', 'u_status')
    if students:

        file = open(filepath, 'w', encoding='utf-8', newline='')
        writer = csv.writer(file)
        writer.writerow(['姓名', '学号', '身份证号', '性别', '学院', '专业', '年级', '学历', '签约状态'])
        for s in students:
            writer.writerow([s['u_name'], s['u_id'], s['u_identyid'], s['u_sex'], s['u_xueyuan'], s['u_zhuanye'], s['u_nianji'], s['u_xueli'], s['u_status']])

        p1 = Paginator(students, 5)
        if page:
            page = int(page)
        else:
            page = 1
        list1 = p1.page(page)
        plist = p1.page_range
        context = {'plist': plist, 'tests': list1, 'pIndex': page}
        return render(request, 'teacher/teacher_chaxun_sousuo.html', context)

    else:
        nostudents = 1
        context = {'nostudents': nostudents}
        return render(request, 'teacher/teacher_chaxun_sousuo.html', context)


def teacher_chaxun(request, pIndex):

    students = QianyueInfo.objects.filter().values('q_student_id', 'q_student_id__u_name',
                                                                      'q_student_id__u_identyid'
                                                                      , 'q_student_id__u_xueyuan', 'q_student_id__u_zhuanye'
                                                                      , 'q_student_id__u_nianji', 'q_student_id__u_xueli'
                                                                      , 'q_student_id__u_status', 'q_student_id__u_sex')
    p = Paginator(students, 5)
    if pIndex == '':
        pIndex = 1
    pIndex = int(pIndex)
    list2 = p.page(pIndex)
    plist = p.page_range
    context = {'plist': plist, 'students': list2, 'pIndex': pIndex}
    return render(request, 'teacher/teacher_chaxun.html', context)



class DateTimeTest(object):
    def __init__(self, year, month , day, c):
        self.year = year
        self.month = month
        self.day = day
        self.count = c


def teacher_chartstest(request):
    students = QianyueStudent.objects.all()

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

    zhuanyeset1 = QianyueStudent.objects.values_list('u_zhuanye').annotate(Count('u_zhuanye')).filter(u_xueli='大学本科')
    zhuanyeset2 = QianyueStudent.objects.values_list('u_zhuanye').annotate(Count('u_zhuanye')).filter(u_xueli='硕士研究生')
    #print(zhuanyeset1)
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
    #print(zhuanyeset1_dict)
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