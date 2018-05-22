from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import *
from company.models import CompanyInfo,QianyueInfo
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
import requests
import importlib
import urllib
import urllib.request
import base64
import hashlib
import urllib.parse
import json

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
                red = HttpResponseRedirect('/student/index/')
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
                p = Paginator(yaoyues, 5)
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
    url = 'http://v.juhe.cn/sms/send'
    # 准备一下头
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
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
        company = CompanyInfo.objects.get(id=c_id)
        values = {
            'mobile': company.c_lianxidianhua,
            'tpl_id': 68784,
            'key': '0e9b1c796985a4c51cd563b0077fb8f0',
        }
        #print(qianyuestudent.u_company_id__c_lianxidianhua)
        # 将字典格式化成能用的形式
        data = urllib.parse.urlencode(values).encode('utf-8')
        # 创建一个request,放入我们的地址、数据、头
        rt = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(rt).read().decode('utf-8')
        print(json.loads(html)['result'])
        print(json.loads(html)['error_code'])

        return HttpResponse('接收邀约成功')
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


def student_wuliuxinxiluru(request):
    student_id = request.session.get('student_id')
    if student_id:
        status = QianyueStudent.objects.filter(u_id=student_id)[0].u_status
        if status == '已签约':
            qianyuestudents = QianyueStudent.objects.filter(u_id=student_id).values('u_company_id__c_danweimingcheng')
            qianyuestudent = qianyuestudents[0]
            context = {'qianyuestudent': qianyuestudent}
            return render(request, 'student/student_wuliuxinxiluru.html', context)
    else:
        return redirect('/student/login/')


def student_wuliuxinxibaocun(request):
    student_id = request.session.get('student_id')
    if student_id:
        print(student_id)
        company_name = request.POST.get('identyid')
        kuaidi = request.POST.get('kuaidi1')
        print(company_name)
        QianyueInfo.objects.filter(q_company_id__c_danweimingcheng=company_name, q_student_id=student_id).update(q_stu_kuaidi=kuaidi)
        return HttpResponse('录入成功！')
    else:
        return redirect('/student/login/')


class Express100(object):
    company_url = "http://www.kuaidi100.com/autonumber/autoComNum"
    trace_url = "http://www.kuaidi100.com/query"

    @classmethod
    def get_json_data(cls, url, payload):
        r = requests.get(url=url, params=payload)
        return r.json()

    @classmethod
    def get_company_info(cls, express_code):
        payload = {'text': express_code}
        data = cls.get_json_data(cls.company_url, payload)
        return data

    @classmethod
    def get_express_info(cls, express_code):
        company_info = cls.get_company_info(express_code)
        company_code = ""
        if company_info.get("auto", ""):
            company_code = company_info.get("auto", "")[0].get("comCode", "")
        payload = {'type': company_code, 'postid': express_code, 'id': 1}
        data = cls.get_json_data(cls.trace_url, payload)
        data.update(company_info)
        return data


def student_wuliuxinxichakan(request):
    student_id = request.session.get('student_id')
    if student_id:
        qianyue = QianyueInfo.objects.filter(q_student_id=student_id)[0]
        code1 = qianyue.q_com_kuaidi
        code2 = qianyue.q_stu_kuaidi
        res1 = Express100.get_express_info(str(code1).strip())
        res2 = Express100.get_express_info(str(code2).strip())
        messagelist1 = []
        messagelist2 = []
        #res1 = json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4)
        for test1 in res1["data"]:
            messagelist1.append(test1['ftime'] + '  :  ' + test1['context'])
        for test2 in res2["data"]:
            messagelist2.append(test2['ftime'] + '  :  ' + test2['context'])
        if messagelist1 and messagelist2:
            context = {'messagelist1': messagelist1, 'messagelist2': messagelist2}
            return render(request, 'student/student_chakanwuliuxinxi.html', context)
        elif messagelist1 and not messagelist2:
            context = {'messagelist1': messagelist1, 'nowuliuxinxi2': '暂无物流信息呢！'}
            return render(request, 'student/student_chakanwuliuxinxi.html', context)
        elif messagelist2 and not messagelist1:
            context = {'messagelist2': messagelist2, 'nowuliuxinxi1': '暂无物流信息呢！'}
            return render(request, 'student/student_chakanwuliuxinxi.html', context)
        else:
            context = {'nowuliuxinxi1': '暂无物流信息呢！', 'nowuliuxinxi2': '暂无物流信息呢！'}
            return render(request, 'student/student_chakanwuliuxinxi.html', context)
    else:
        return redirect('/student/login/')


def student_shujutongji(request):
    u_id = request.session.get('student_id')
    diquset1 = QianyueStudent.objects.values_list('u_company_id__c_danweilishu').annotate(Count('u_company_id__c_danweilishu')).filter(u_xueli='大学本科')
    diquset2 = QianyueStudent.objects.values_list('u_company_id__c_danweilishu').annotate(Count('u_company_id__c_danweilishu')).filter(u_xueli='硕士研究生')
    student = QianyueStudent.objects.get(u_id=u_id)
    zhuanye = student.u_zhuanye
    name = student.u_name
    print(zhuanye)
    zhiweiset = QianyueInfo.objects.values_list('q_gangwei').annotate(Count('q_gangwei')).filter(q_student_id__u_zhuanye=zhuanye)
    print(zhiweiset)
    diquset1_dict = {}
    diquset2_dict = {}
    zhiwei_dict={}
    sum = 0
    for set1 in diquset1:
        sum += set1[1]
    for set1 in diquset1:
        diquset1_dict[set1[0]] = (set1[1]*100)/sum
    sum = 0
    for set2 in diquset2:
        sum += set2[1]
    for set2 in diquset2:
        diquset2_dict[set2[0]] = (set2[1]*100)/sum
    sum = 0
    for set3 in zhiweiset:
        sum += set3[1]
    for set3 in zhiweiset:
        zhiwei_dict[set3[0]] = (set3[1]*100)/sum
    print(diquset1_dict)
    print(diquset2_dict)
    context = {'diquset1_dict': diquset1_dict, 'diquset2_dict': diquset2_dict, 'zhiwei_dict': zhiwei_dict, 'name': name}
    return render(request, 'student/student_shujutongji.html', context)