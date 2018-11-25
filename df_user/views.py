# coding = utf-8
from django.shortcuts import render, redirect
from .islogin import islogin
# Create your views here.


def register(requset):
    return render(requset, 'df_user/register.html')

from .models import *
from hashlib import sha1
def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断两次密码
    if upwd != upwd2:
        # 重定向
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf-8"))
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    # 注册成功，转到登录界面
    return redirect('/user/login/')

# 判断用户是否存在
from django.http import JsonResponse
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count': count})

# 登录界面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html', context)
    # s1.update(upwd.encode("utf-8"))

# 登录处理
'''
HttpRessponseRedirect对象：
    服务器接收到http协议的请求后，会根据报文创建HttpRequset对象
    视图函数的第一个参数是HttpRequset对象
'''
from django.shortcuts import HttpResponseRedirect
def login_handle(request):
    # 接收请求信息
    get = request.POST
    uname = get.get('username')
    upwd = get.get('pwd')
    jizhu = get.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    # print uname
    # 判断如果未查到则用户名错，查到再判断密码是否正确，正确则转到用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf-8"))
        #登录带cookie值   必须 red = HttpResponseRedirect    red.set_cookie  renturn red
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info')
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            # 判断用户有没有登录
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname }
        return render(request, 'df_user/login.html', context)

# 用户中心
from df_goods.models import GoodsInfo
@islogin
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail

    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    goods_list = []
    if len(goods_ids):
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name': 1, 'info': 1,
               'goods_list': goods_list}
    return render(request, 'df_user/user_center_info.html', context)

# 订单
@islogin
def order(request):
    context = {'title':'用户中心'}
    return render(request, 'df_user/user_center_order.html', context)

# 收货地址
@islogin
def site(requset):
    user = UserInfo.objects.get(id = requset.session['user_id'])
    if requset.method == 'POST':
        post = requset.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'用户中心', 'user':user, 'page_name':1,}
    return render(requset, 'df_user/user_center_site.html', context)

# 退出
def logout(request):
    request.session.flush()
    return redirect('/')

from df_order.models import OrderInfo
from django.core.paginator import Paginator
@islogin
def user_center_order(request, pageid):
    """
    此页面用户展示用户提交的订单，由购物车页面下单后转调过来，也可以从个人信息页面查看
    根据用户订单是否支付、下单顺序进行排序
    """

    uid = request.session.get('user_id')
    # 订单信息，根据是否支付、下单顺序进行排序
    orderinfos = OrderInfo.objects.filter(
        user_id=uid).order_by('zhifu', '-oid')

    # 分页
    #获取orderinfos list  以两个为一页的 list
    paginator = Paginator(orderinfos, 2)
    # 获取 上面集合的第 pageid 个 值
    orderlist = paginator.page(int(pageid))
    #获取一共多少 页
    plist = paginator.page_range
    #3页分页显示
    qian1 = 0
    hou = 0
    hou2 = 0
    qian2 = 0
    # dd = dangqian ye
    dd = int(pageid)
    lenn = len(plist)
    if dd>1:
        qian1 = dd-1
    if dd>=3:
        qian2 = dd-2
    if dd<lenn:
        hou = dd+1
    if dd+2<=lenn:
        hou2 = dd+2

    # 构造上下文
    context = {'page_name': 1,
               'title': '全部订单',
               'pageid': int(pageid),
               'order': 1,
               'orderlist': orderlist,
               'plist': plist,
               'pre': qian1,
               'next': hou,
               'pree': qian2,
               'lenn': lenn,
               'nextt': hou2}

    return render(request, 'df_user/user_center_order.html', context)


