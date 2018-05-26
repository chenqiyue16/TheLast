from django.shortcuts import render,redirect
from .models import *
from student.models import LinshiInfo, StudentInfo, QianyueStudent
from django.core.paginator import Paginator
from hashlib import sha1
from django.http import HttpResponse, HttpResponseRedirect
import json
import pdfkit
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
import importlib
import urllib
import urllib.request
import base64
import hashlib
import urllib.parse
from django.db.models.aggregates import Count
# Create your views here.

APP_id = "1266271"
APP_key = "7526a46e-3a2a-4f5b-8659-d72f361e3386"


def company_login(request):

    return render(request, 'company/company_login.html')


def company_tuichu(request):
    request.session.clear()
    return redirect('/company/login/')


def login_handle(request):
    u_name = request.POST.get('username')
    u_pwd = request.POST.get('password')
    u_check = request.POST.get('checkout', 0)
    print("uname::"+u_name)
    s1 = sha1()
    s1.update(u_pwd.encode("utf8"))
    upwd_hash = s1.hexdigest()
    name = CompanyInfo.objects.filter(c_username=u_name)
    pwd = CompanyInfo.objects.filter(c_username=u_name, c_password=upwd_hash)
    if name.exists():
        if pwd.exists():
            # url = request.COOKIES.get('url', '/')
            u_shenhe = name[0].c_shenhe
            if u_shenhe == 1:
                red = HttpResponseRedirect('/company/index/')
            else:
                red = HttpResponseRedirect('/company/weishenhe/')
            if u_check == 1:
                red.set_cookie('username', u_name)
            else:
                red.set_cookie('username', '', max_age=-1)

            request.session['username'] = u_name
            request.session['danweimingcheng'] = name[0].c_danweimingcheng
            request.session['shenhe'] = name[0].c_shenhe
            request.session['u_id'] = name[0].id
            return red
        else:
            context = {'error_name': 0, 'error_password': 1}
            return render(request, 'company/company_login.html', context)
    else:
        context = {'error_name': 1, 'error_password': 0}
        return render(request, 'company/company_login.html', context)


def company_xiugaimima(request):
    return render(request, 'company/company_xiugaimima.html')


def company_xiugaimima_handle(request):
    yuanmima = request.POST.get('yuanmima')
    u_id = request.session.get('u_id')
    company = CompanyInfo.objects.filter(id=u_id)[0]
    s1 = sha1()
    s1.update(yuanmima.encode("utf8"))
    upwd_hash = s1.hexdigest()
    #print(student)
    if upwd_hash == company.c_password:
        #print('密码正确')
        return HttpResponse(json.dumps({"msg": '密码正确'}))
    else:
        #print('密码错误')
        return HttpResponse(json.dumps({"msg": '密码错误'}))


def company_xiugaimima_check(request):
    company_id = request.session.get('u_id')
    mima1 = request.POST.get('xinmima')
    mima2 = request.POST.get('xinmimaqueren')
    if company_id:
        if mima1 == mima2:
            company = CompanyInfo.objects.filter(id=company_id)[0]
            s1 = sha1()
            s1.update(mima1.encode("utf8"))
            upwd_hash = s1.hexdigest()
            company.c_password = upwd_hash
            company.save()
            return HttpResponse(
                '<script type="text/javascript">alert("修改成功！");parent.location.href="/company/login/";</script>')
    else:
        return HttpResponse('<script type="text/javascript">alert("没有登录，请先登录！");parent.location.href="/student/login/";</script>')


def company_index(request):
    id = request.session.get('u_id')
    if id:
        company = CompanyInfo.objects.get(id=id)
        if company.c_shenhe == 1:
            name = request.session.get('username')
            danweimingcheng = request.session.get('danweimingcheng')
            id = request.session.get('u_id')
            context = {'name': name, 'danweimingcheng': danweimingcheng, 'id': id}
            return render(request, 'company/index.html', context)
        else:
            return redirect('/company/weishenhe')
    else:
        return redirect('/company/login/')


def company_welcome(request):
    return render(request, 'company/welcome.html')


def company_yaoyue(request):
    students = LinshiInfo.objects.all()
    id = request.session.get('u_id')
    if id != '':
        companys = CompanyInfo.objects.filter(id=id)
        company = companys[0]
        context = {'students': students, 'company': company}
        return render(request, 'company/company_yaoyue.html', context)
    else:
        redirect('/company/login/')


def company_yaoyue_handle(request):
    url = 'http://v.juhe.cn/sms/send'
    # 准备一下头
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }


    qianyuegangwei = request.POST.get('qianyuegangwei')
    youxiaotianshu = request.POST.get('qianyuetianshu')
    gongzuodidian = request.POST.get('gongzuodidian')
    baodaodizhi = request.POST.get('baodaodizhi')
    baodaoshijian = request.POST.get('baodaoshijian')
    shiyongqixian = request.POST.get('shiyongqixian')
    zhuanzhengxinshui = request.POST.get('zhuanzhengxinshui')
    qita = request.POST.get('qita')
    zhiweileibie = request.POST.get('zhiweileibie')
    danganjieshou = request.POST.get('selectDangan', None)
    print(danganjieshou)
    print('???')
    students = LinshiInfo.objects.filter(u_company_id=request.session.get('u_id'))
    for student in students:
        qianyue = QianyueInfo()
        qianyue.q_youxiaotianshu = youxiaotianshu
        qianyue.q_gongzuodidian = gongzuodidian
        qianyue.q_baodaodizhi = baodaodizhi
        qianyue.q_baodaoshijian = baodaoshijian
        qianyue.q_shiyongqixian = shiyongqixian
        qianyue.q_zhuanzhengxinshui = zhuanzhengxinshui
        qianyue.q_qita = qita
        qianyue.q_gangwei = qianyuegangwei
        qianyue.q_zhiweileibie = zhiweileibie
        qianyue.q_danganjieshou = int(danganjieshou)

        if danganjieshou != None:
            jieshoubumen = request.POST.get('jieshoubumen')
            jieshoudanwei = request.POST.get('jieshoudanwei')
            jieshoudizhi = request.POST.get('jieshoudizhi')
            jieshouyoubian = request.POST.get('jieshouyoubian')
            jieshouren = request.POST.get('jieshouren')
            jieshoudianhua = request.POST.get('jieshoudianhua')
            qianyue.q_jieshoubumen = jieshoubumen
            qianyue.q_jieshoudanweimingcheng = jieshoudanwei
            qianyue.q_jieshouxiangxidizhi = jieshoudizhi
            qianyue.q_jieshouyoubian = jieshouyoubian
            qianyue.q_jieshouren = jieshouren
            qianyue.q_jieshoudianhua = jieshoudianhua
        qianyue.q_student_id = student.u_id
        qianyue.q_company_id = request.session.get('u_id')
        qianyue.save()

        values = {
            'mobile': student.u_shouji,
            'tpl_id': 68783,
            'key': '0e9b1c796985a4c51cd563b0077fb8f0',
        }
        # 将字典格式化成能用的形式
        data = urllib.parse.urlencode(values).encode('utf-8')
        # 创建一个request,放入我们的地址、数据、头
        rt = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(rt).read().decode('utf-8')
        print(json.loads(html)['result'])
        print(json.loads(html)['error_code'])
    LinshiInfo.objects.filter(u_company_id=request.session.get('u_id')).delete()
    return HttpResponse('邀约成功！')


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


def test(request):
    # 此处为快递鸟官网申请的帐号和密码
    code = '813164737871'
    res = Express100.get_express_info(str(code).strip())
    messagelist = []
    #res1 = json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4)
    for test in res["data"]:
        messagelist.append(test['ftime'] + '  :  ' + test['context'])
    print(messagelist)
    context = {'messagelist': messagelist}
    return render(request, 'company/test.html', context)


def testpdf(request):
    print("test")
    pdfkit.from_url('https://www.liuxue86.com/a/2545752.html', 'out1.pdf')
    return redirect('/company/test/')


def company_shanchustudent(request):
    student_list = request.REQUEST.getlist('student_list')
    print(student_list)
    for ls in student_list:
        student = LinshiInfo.objects.get(u_id=ls)
        student.delete()

    return redirect('/company/yaoyue/')


def company_chaxunstudent(request):
    return render(request, 'company/company_chaxun.html')


def company_register1(request):
    return render(request, 'company/company_register1.html')

@csrf_exempt
def company_checkUname(request):
    username = request.POST.get('username', None)
    danweimingcheng = request.POST.get('danweimingcheng', None)
    zuzhijigoudaima = request.POST.get('zuzhijigoudaima', None)
    print(username)
    rtxt=""
    danweimingcheng2 = CompanyInfo.objects.filter(c_danweimingcheng=danweimingcheng)
    name2 = CompanyInfo.objects.filter(c_username=username)
    zuzhijigoudaima2 = CompanyInfo.objects.filter(c_zuzhijigoudaima=zuzhijigoudaima)
    if username != None:
        if name2.exists():
            rtxt = "用户名已存在！"
            return HttpResponse(json.dumps({"msg": rtxt}))
        else:
            return HttpResponse(json.dumps({"msg": rtxt}))
    if danweimingcheng != None:
        if danweimingcheng2.exists():
            rtxt = "单位名称已存在！"
            return HttpResponse(json.dumps({"msg": rtxt}))
        else:
            return HttpResponse(json.dumps({"msg": rtxt}))
    if zuzhijigoudaima != None:
        if zuzhijigoudaima2.exists():
            rtxt = "组织机构代码已存在！"
            return HttpResponse(json.dumps({"msg": rtxt}))
        else:
            return HttpResponse(json.dumps({"msg": rtxt}))


def company_register2(request):
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if password == password2 and password != None:
        s1 = sha1()
        s1.update(password.encode("utf8"))
        upwd_hash = s1.hexdigest()
        username = request.POST.get('username')
        danweimingcheng = request.POST.get('danweimingcheng')
        zuzhijigoudaima = request.POST.get('zuzhijigoudaima')
        request.session['username'] = username
        request.session['password'] = upwd_hash
        request.session['danweimingcheng'] = danweimingcheng
        request.session['zuzhijigoudaima'] = zuzhijigoudaima

        return render(request, 'company/company_register2.html')
    else:
        return redirect('/company/register1/')


def company_registerhandle(request):
    username = request.session.get('username')
    print(username)
    if username != "":
        company = CompanyInfo.objects.filter(c_username=username)
        if company:
            return HttpResponse('<script type="text/javascript" > alert("用户名已存在！请不要重复注册！")</script>')
        else:
            password = request.session.get('password')
            danweimingcheng = request.session.get('danweimingcheng')
            zuzhijigoudaima = request.session.get('zuzhijigoudaima')
            danweilishu = request.POST.get('danweilishu')
            danweihangye = request.POST.get('danweihangye')
            danweixingzhi = request.POST.get('danweixingzhi')
            lianxiren = request.POST.get('lianxiren')
            lianxidianhua = request.POST.get('lianxidianhua')
            tongxindizhi = request.POST.get('tongxindizhi')
            zhizhao = request.FILES.get('zhizhao')
            email = request.POST.get('email')
            print(zhizhao)
            fname = '%s/zhizhao/%s.jpg' % (settings.MEDIA_ROOT, zuzhijigoudaima)
            with open(fname, 'wb') as pic:
                for c in zhizhao.chunks():
                    pic.write(c)
            company = CompanyInfo()
            company.c_username = username
            company.c_password = password
            company.c_danweimingcheng = danweimingcheng
            company.c_zuzhijigoudaima = zuzhijigoudaima
            company.c_danweilishu = danweilishu
            company.c_lianxiren = lianxiren
            company.c_lianxidianhua = lianxidianhua
            company.c_danweihangye = danweihangye
            company.c_danweixingzhi = danweixingzhi
            company.c_tongxindizhi = tongxindizhi
            company.c_pic = fname
            company.c_youxiang = email

            company.save()
            return redirect('/company/login/')
    else:
        return redirect('/company/register1/')


def company_weishenhe(request):
    id = request.session.get('u_id')
    company = CompanyInfo.objects.get(id=id)
    if company.c_shenhe != 1:
        id = request.session.get('u_id')
        companys = CompanyInfo.objects.filter(id=id)
        company = companys[0]
        context = {'company': company}
        return render(request, 'company/company_weishenhe.html', context)
    else:
        return HttpResponse('<script type="text/javascript">alert("审核成功，即将跳转页面！");parent.location.href="/company/index/";</script>')


def company_weishenhe_xiugai(request):
    id = request.session.get('u_id')
    companys = CompanyInfo.objects.filter(id=id)
    company = companys[0]
    context = {'company': company}
    return render(request, 'company/company_weishenhe_xiugai.html', context)


def company_xiugaihandle(request):
    id = request.session.get('u_id')
    if id:
        danweimingcheng = request.POST.get('danweimingcheng')
        danweilishu = request.POST.get('danweilishu')
        lianxiren = request.POST.get('lianxiren')
        lianxidianhua = request.POST.get('lianxidianhua')
        youxiang = request.POST.get('email')
        tongxindizhi =request.POST.get('tongxindizhi')
        danweixingzhi = request.POST.get('danweixingzhi')
        danweihangye = request.POST.get('danweihangye')

        CompanyInfo.objects.filter(id=id).update(c_danweimingcheng=danweimingcheng, c_danweilishu=danweilishu,
                                                 c_lianxiren=lianxiren, c_lianxidianhua=lianxidianhua,
                                                 c_youxiang=youxiang, c_tongxindizhi=tongxindizhi,
                                                 c_danweixingzhi=danweixingzhi, c_danweihangye=danweihangye,
                                                 c_shenhe=0)
        request.session['shenhe'] = 0
        return HttpResponse('修改成功！请耐心等待审核')
    else:
        return redirect('/company/login/')

def company_info(request):
    id = request.session.get('u_id')
    companys = CompanyInfo.objects.filter(id=id)
    company = companys[0]
    context = {'company': company}
    return render(request, 'company/company_info.html', context)


@csrf_exempt
def company_addstudent(request):
    studentid = request.POST.get('studentid', None)
    print(studentid)
    id =request.session.get('u_id', None)
    if studentid != None and id != None:

        stlinshi = LinshiInfo.objects.filter(u_identyid=studentid)
        if stlinshi.exists():
            return HttpResponse(json.dumps({"msg": '此人您已发出邀约！'}))
        else:
            stlinshi = QianyueInfo.objects.filter(q_student_id__u_identyid=studentid, q_company_id=id)
            if stlinshi.exists():
                return HttpResponse(json.dumps({"msg": '此人您已发出邀约！'}))
            else:
                students = StudentInfo.objects.filter(u_identyid=studentid)

                print(students)
                if students:
                    if students[0].u_status == '未签约':
                        student = LinshiInfo()
                        student.u_id = students[0].u_id
                        student.u_name = students[0].u_name
                        student.u_xueyuan = students[0].u_xueyuan
                        student.u_nianji = students[0].u_nianji
                        student.u_xueli = students[0].u_xueli
                        student.u_zhuanye = students[0].u_zhuanye
                        student.u_status = students[0].u_status
                        student.u_identyid = students[0].u_identyid
                        student.u_shouji = students[0].u_shouji
                        student.u_minzu = students[0].u_minzu
                        student.u_sex = students[0].u_sex
                        student.u_company_id = str(id)
                        student.save()
                        return HttpResponse(json.dumps({"msg": '添加成功'}))
                    else:
                        return HttpResponse(json.dumps({"msg": '添加失败，此人已完成签约！'}))
                else:
                    return HttpResponse(json.dumps({"msg": '添加失败,无效的身份证号'}))
    else:
        return redirect('/company/login/')


def company_chaxun(request, pIndex):

    id = request.session.get('u_id', None)
    if id != None:
        students = QianyueInfo.objects.filter(q_company_id=id).values('q_student_id', 'q_student_id__u_name',
                                                                      'q_student_id__u_identyid'
                                                                      , 'q_student_id__u_xueyuan', 'q_student_id__u_zhuanye'
                                                                      , 'q_student_id__u_nianji', 'q_student_id__u_xueli'
                                                                      , 'q_qianyuezhuangtai')

        p = Paginator(students, 1)
        if pIndex == '':
            pIndex = 1
        pIndex = int(pIndex)
        list2 = p.page(pIndex)
        plist = p.page_range
        context = {'plist': plist, 'students': list2, 'pIndex': pIndex}

        return render(request, 'company/company_chaxun.html', context)
    else:
        return redirect('/company/login/')


def company_chaxun_xiangxixinxi(request, id):
    qianyue = QianyueInfo.objects.filter(q_student_id=id)
    students = StudentInfo.objects.filter(u_id=id)
    identyid = students[0].u_identyid
    name = students[0].u_name
    context = {'qianyue': qianyue[0], 'name': name, 'identyid': identyid}
    return render(request, 'company/company_chaxun_xiangxixinxi.html', context)


def company_chaxun_sousuo(request, pIndex):

    queryset = {}
    kwargs = {}
    id = request.session.get('u_id')
    #print(id)
    page = request.GET.get('page', None)
    queryset['u_name'] = request.GET.get('u_name', None)
    queryset['u_id'] = request.GET.get('u_id', None)
    queryset['u_identyid'] = request.GET.get('u_identyid', None)
    queryset['u_xueyuan'] = request.GET.get('u_xueyuan', None)
    queryset['u_zhuanye'] = request.GET.get('u_zhuanye', None)
    queryset['u_xueli'] = request.GET.get('u_xueli', None)
    queryset['FAN1__q_qianyuezhuangtai'] = request.GET.get('u_qianyuezhuangtai', None)
    queryset['FAN1__q_danganjieshou'] = request.GET.get('u_danganjieshou', None)
    queryset['FAN1__q_company_id'] = id
    for (k, v) in queryset.items():
        if v != '':
            kwargs[k] = v
    #print(kwargs)

    students = StudentInfo.objects.filter(**kwargs).values('u_name', 'u_id', 'u_identyid', 'u_xueyuan', 'u_zhuanye','u_nianji'
                                                           , 'u_xueli', 'FAN1__q_qianyuezhuangtai', 'FAN1__q_danganjieshou'
                                                           , 'FAN1__q_company_id')
    if students:
        p1 = Paginator(students, 2)
        if page:
            page = int(page)
        else:
            page = 1
        list1 = p1.page(page)
        plist = p1.page_range
        context = {'plist': plist, 'tests': list1, 'pIndex': page}
        return render(request, 'company/company_chaxun_sousuo.html', context)

    else:
        nostudents = 1
        context = {'nostudents': nostudents}
        return render(request, 'company/company_chaxun_sousuo.html', context)


def company_quxiaoyaoyue(request):
    id = request.session.get('u_id')
    if id:
        student_list = request.REQUEST.getlist('student_list')
        if student_list:
            for ls in student_list:
                student = QianyueInfo.objects.get(q_student_id=ls, q_company_id=id)
                student.delete()
            return render(request, 'company/company_chaxun_sousuo.html', {'quxiaochenggong': 1, "nostudenbs": 0})
        else:
            return render(request, 'company/company_chaxun_sousuo.html', {'quxiaochenggong': 0, "nostudents": 0})
    else:
        return redirect('/company/login/')


def company_qianyueinfo(request, page):
    company_id = request.session.get('u_id')
    if company_id:
        qianyuestudent = QianyueStudent.objects.filter(u_company_id=company_id)
        if page:
            page = int(page)
        else:
            page = 1
        p1 = Paginator(qianyuestudent, 2)
        list1 = p1.page(page)
        plist = p1.page_range

        context = {'list1': list1, 'plist': plist, 'pIndex': page}
        return render(request, 'company/company_qianyueinfo.html', context)


def company_sanfangxieyi(request, student_id):

    company_id = request.GET.get('test')
    t = str(company_id)
    print('t:'+t)
    print('student_id:'+ student_id)
    if t:
        qianyuestudent = QianyueStudent.objects.filter(u_id=student_id)[0]
        qianyue = QianyueInfo.objects.filter(q_company_id=t, q_student_id=student_id)[0]
        company = CompanyInfo.objects.filter(id=t)[0]
        context = {'student': qianyuestudent, 'qianyue': qianyue, 'company': company}

        return render(request, 'company/company_sanfangxieyi.html', context)
    else:
        return redirect('/company/login/')



def company_getsanfangxieyi(request, student_id):
    print("test")
    company_id = request.session.get('u_id')
    if company_id:
        url1 = 'http://127.0.0.1:8000/company/sanfangxieyi_' + str(student_id)+'/?test='+str(company_id)
    #url1 = 'http://127.0.0.1:8000/company/sanfangxieyi_235373/'
        url2 = 'static/sanfangxieyi/sanfangxieyi_'+str(student_id)+'.pdf'
        print(url1)
        print(url2)
        pdfkit.from_url(url1, url2)
        url3 = '/static/sanfangxieyi/sanfangxieyi_' + str(student_id)+'.pdf'
        return redirect(url3)
    else:
        redirect('/company/login/')


def company_wuliuxinxiluru(request):
    return render(request, 'company/company_wuliuxinxiluru.html')


def company_wuliuxinxi_check(request):
    identyid = request.POST.get('identyid')
    company_id = request.session.get('u_id')
    qianyuestudents = QianyueStudent.objects.filter(u_identyid=identyid, u_company_id=company_id)
    if qianyuestudents:
        rtxt = qianyuestudents[0].u_name
        return HttpResponse(json.dumps({"msg": "成功", "u_name": rtxt}))
    else:
        rtxt = '未查找到该学生'
        return HttpResponse(json.dumps({"msg": rtxt}))


def company_wuliuxinxi_baocun(request):
    u_id = request.session.get('u_id')
    if u_id:
        print(u_id)
        identyid = request.POST.get('identyid')
        kuaidi = request.POST.get('kuaidi1')
        QianyueInfo.objects.filter(q_student_id__u_identyid=identyid, q_company_id=u_id).update(q_com_kuaidi=kuaidi)
        return redirect('/company/wuliuxinxichakan/')
    else:
        return redirect('/company/login/')


def company_wuliuxinxi_chakan(request, page):
    print('why')
    u_id = request.session.get('u_id')
    students = StudentInfo.objects.filter(FAN1__q_company_id=u_id, FAN1__q_qianyuezhuangtai=1).values('u_name', 'u_id', 'u_identyid', 'u_xueyuan', 'u_nianji', 'FAN1__q_gangwei', 'FAN1__q_com_kuaidi', 'FAN1__q_stu_kuaidi', 'FAN1__q_company_id')
    p1 = Paginator(students, 1)
    if page:
        page = int(page)
    else:
        page = 1
    list1 = p1.page(page)
    plist = p1.page_range
    context = {'plist': plist, 'tests': list1, 'pIndex': page}
    return render(request, 'company/company_wuliuxinxichakan.html', context)


def company_wuliuxinxi_chakan_sousuo(request):
    queryset = {}
    kwargs = {}
    id = request.session.get('u_id')
    #print(id)
    page = request.GET.get('page', None)
    queryset['u_name'] = request.GET.get('u_name', None)
    queryset['u_id'] = request.GET.get('u_id', None)
    queryset['u_identyid'] = request.GET.get('u_identyid', None)
    queryset['u_xueyuan'] = request.GET.get('u_xueyuan', None)
    queryset['u_nianji'] = request.GET.get('u_nianji', None)
    queryset['FAN1__q_gangwei'] = request.GET.get('u_gangwei', None)
    queryset['FAN1__q_company_id'] = id
    queryset['FAN1__q_qianyuezhuangtai'] = 1
    for (k, v) in queryset.items():
        if v != '':
            kwargs[k] = v
    print(kwargs)

    students = StudentInfo.objects.filter(**kwargs).values('u_name', 'u_id', 'u_identyid', 'u_xueyuan', 'u_nianji'
                                                           , 'FAN1__q_gangwei', 'FAN1__q_com_kuaidi'
                                                           , 'FAN1__q_stu_kuaidi'
                                                           , 'FAN1__q_company_id')
    if students:
        p1 = Paginator(students, 1)
        if page:
            page = int(page)
        else:
            page = 1
        list1 = p1.page(page)
        plist = p1.page_range
        context = {'plist': plist, 'tests': list1, 'pIndex': page}
        return render(request, 'company/company_wuliuxinxichakan_sousuo.html', context)

    else:
        nostudents = 1
        context = {'nostudents': nostudents}
        return render(request, 'company/company_wuliuxinxichakan_sousuo.html', context)


def company_wuliuxinxi_chakan_xiangxixinxi(request, id):
    # 此处为快递鸟官网申请的帐号和密码

    qianyue = QianyueInfo.objects.filter(q_student_id=id)[0]
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
        return render(request, 'company/company_wuliuxinxichakan_xiangxixinxi.html', context)
    elif messagelist1 and not messagelist2:
        context = {'messagelist1': messagelist1, 'nowuliuxinxi2': '暂无物流信息呢！'}
        return render(request, 'company/company_wuliuxinxichakan_xiangxixinxi.html', context)
    elif messagelist2 and not messagelist1:
        context = {'messagelist2': messagelist2, 'nowuliuxinxi1': '暂无物流信息呢！'}
        return render(request, 'company/company_wuliuxinxichakan_xiangxixinxi.html', context)
    else:
        context = {'nowuliuxinxi1': '暂无物流信息呢！', 'nowuliuxinxi2': '暂无物流信息呢！'}
        return render(request, 'company/company_wuliuxinxichakan_xiangxixinxi.html', context)


def company_chartstest(request):
    u_id = request.session.get('u_id')
    set = QianyueStudent.objects.values_list('u_nianji').annotate(Count('u_nianji')).filter(u_xueli='大学本科', u_company_id=u_id).order_by('u_nianji')
    set1 = QianyueStudent.objects.values_list('u_nianji').annotate(Count('u_nianji')).filter(u_xueli='硕士研究生', u_company_id=u_id).order_by('u_nianji')
    set2 = QianyueStudent.objects.distinct().values('u_nianji').order_by('u_nianji')
    print('set')
    print(set)
    print('set1')
    print(set1)
    print('set2')
    print(set2)
    benkelist = []
    benkenianjilist={}
    shuoshilist = []
    shuoshinianjilist={}
    nianjilist = []
    for s2 in set2:
        nianjilist.append(s2['u_nianji'])

    for s1 in set1:
        shuoshinianjilist[s1[0]] = s1[1]
    for s in set:
        benkenianjilist[s[0]] = s[1]
    for nianji in nianjilist:
        if nianji in shuoshinianjilist:
            shuoshilist.append(shuoshinianjilist[nianji])
        else:
            shuoshilist.append(0)
    for l in benkenianjilist:
        print(l)
    print(benkenianjilist)
    print(nianjilist)
    for nianji in nianjilist:
        if nianji in benkenianjilist:
            benkelist.append(benkenianjilist[nianji])
        else:
            benkelist.append(0)



    zhuanyeset1 = QianyueStudent.objects.values_list('u_zhuanye').annotate(Count('u_zhuanye')).filter(u_xueli='大学本科', u_company_id=u_id)
    zhuanyeset2 = QianyueStudent.objects.values_list('u_zhuanye').annotate(Count('u_zhuanye')).filter(u_xueli='硕士研究生', u_company_id=u_id)
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
    agentmanlist1 = QianyueStudent.objects.filter(u_company_id=u_id,u_sex='男',u_xueli='大学本科')
    agentmanlist2 = QianyueStudent.objects.filter(u_company_id=u_id, u_sex='男', u_xueli='硕士研究生')
    agentwomanlist1 = QianyueStudent.objects.filter(u_company_id=u_id,u_sex='女',u_xueli='大学本科')
    agentwomanlist2 = QianyueStudent.objects.filter(u_company_id=u_id, u_sex='女', u_xueli='硕士研究生')
    benkeagentlist = [len(agentmanlist1),len(agentmanlist2)]
    yanjiushengagentlist=[len(agentwomanlist1),len(agentwomanlist2)]
    print(yanjiushengagentlist)
    context = {'nianjilist': nianjilist, 'benkelist': benkelist, 'shuoshilist': shuoshilist,
               'zhuanyeset1_dict': zhuanyeset1_dict, 'zhuanyeset2_dict': zhuanyeset2_dict,
               'benkeagentlist': benkeagentlist, 'yanjiushengagentlist': yanjiushengagentlist}
    return render(request, 'company/company_chartstest.html', context)