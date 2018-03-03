from django.shortcuts import render,redirect
from .models import *
from student.models import LinshiInfo, StudentInfo
from django.core.paginator import Paginator
from hashlib import sha1
from django.http import HttpResponse, HttpResponseRedirect
import json
import pdfkit
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def company_login(request):

    return render(request, 'company/company_login.html')


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


def company_index(request):
    if request.session.get('shenhe') == 1:
        name = request.session.get('username')
        danweimingcheng = request.session.get('danweimingcheng')
        id = request.session.get('u_id')
        context = {'name': name, 'danweimingcheng': danweimingcheng, 'id': id}
        return render(request, 'company/index.html', context)
    else:
        return redirect('/company/weishenhe')




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

    qianyuegangwei = request.POST.get('qianyuegangwei')
    youxiaotianshu = request.POST.get('qianyuetianshu')
    gongzuodidian = request.POST.get('gongzuodidian')
    baodaodizhi = request.POST.get('baodaodizhi')
    baodaoshijian = request.POST.get('baodaoshijian')
    shiyongqixian = request.POST.get('shiyongqixian')
    zhuanzhengxinshui = request.POST.get('zhuanzhengxinshui')
    qita = request.POST.get('qita')
    zhiweileibie = request.POST.get('zhiweileibie')
    danganjieshou = request.POST.get('danganjieshou', None)

    students = LinshiInfo.objects.all()
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
        qianyue.q_danganjieshou = danganjieshou

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
    LinshiInfo.objects.filter(u_company_id=request.session.get('u_id')).delete()
    return redirect('/company/chakan/')




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
        fname = '%s/zhizhao/%s' % (settings.MEDIA_ROOT, zhizhao.name)
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
        return HttpResponse('helloword!')
    else:
        return redirect('/company/register1/')


def company_weishenhe(request):
    if request.session.get('shenhe') != 1:
        id = request.session.get('u_id')
        companys = CompanyInfo.objects.filter(id=id)
        company = companys[0]
        context = {'company': company}
        return render(request, 'company/company_weishenhe.html', context)
    else:
        return redirect('/company/index/')


def company_weishenhe_xiugai(request):
    id = request.session.get('u_id')
    companys = CompanyInfo.objects.filter(id=id)
    company = companys[0]
    context = {'company': company}
    return render(request, 'company/company_weishenhe_xiugai.html', context)


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
            students = StudentInfo.objects.filter(u_identyid=str(studentid))
            student = LinshiInfo()
            student.u_id = students[0].u_id
            student.u_name = students[0].u_name
            student.u_xueyuan = students[0].u_xueyuan
            student.u_nianji = students[0].u_nianji
            student.u_xueli = students[0].u_xueli
            student.u_zhuanye = students[0].u_zhuanye
            student.u_status = students[0].u_status
            student.u_identyid = students[0].u_identyid
            student.u_company_id = str(id)
            student.save()
            print('u_name')
            print(student.u_name)
            print(student)
            return HttpResponse(json.dumps({"msg": '添加成功'}))
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
        context = {'plist': plist, 'students': list2, 'pindex': pIndex}

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


def company_chaxun_sousuo(request):
    queryset = {}
    kwargs = {}
    id = request.session.get('u_id')
    print(id)
    queryset['u_name'] = request.POST.get('u_name', None)
    queryset['u_id'] = request.POST.get('u_id', None)
    queryset['u_identyid'] = request.POST.get('u_identyid', None)
    queryset['u_xueyuan'] = request.POST.get('u_xueyuan', None)
    queryset['u_zhuanye'] = request.POST.get('u_zhuanye', None)
    queryset['u_xueli'] = request.POST.get('u_xueli', None)
    queryset['FAN1__q_qianyuezhuangtai'] = request.POST.get('u_qianyuezhuangtai', None)
    queryset['FAN1__q_danganjieshou'] = request.POST.get('u_danganjieshou', None)
    queryset['FAN1__q_company_id'] = id
    for (k, v) in queryset.items():
        if v != '':
            kwargs[k] = v
    print(kwargs)
    try:
        students = StudentInfo.objects.filter(**kwargs)
    except StudentInfo.DoesNotExist:
        print('Does Not Exist')
    for student in students:
        print(student)

    qianyues = QianyueInfo.objects.filter(q_student_id=student.u_id)
    tests = zip(students, qianyues)
    context = {'tests': tests}
    return render(request, 'company/company_chaxun_sousuo.html', context)
    # if u_name != None
    #     if u_id != None:
    #         if u_identyid != None:
    #             if u_xueyuan != None:
    #                 if u_zhuanye != None:
    #                     if u_xueli != None:
    #                         if u_qianyuezhuangtai !=None:
    #                             if u_danganjieshou != None:
    #                                 pass #全不为None
    #                             elif u_danganjieshou ==None:
    #                                 pass #档案接收不为None
    #                         elif u_qianyuezhuangtai ==None:
    #                     elif u_xueli ==None:
    #                 elif u_zhuanye ==None:
    #             elif u_xueyuan == None:
    #         elif u_identyid == None:
    #     elif u_id == None:
    # elif u_name == None:

