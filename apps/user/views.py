from django.shortcuts import render, redirect, reverse
import re
from user.models import User
# Create your views here.


# /user/register
def register(requset):
    '''注册'''
    if requset.method == 'GET':
        # 显示注册页面
        return render(requset, 'register.html')
    else:
        # 进行注册处理
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all(username, password, email):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 邮箱不合法
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})

        # 校验用户名是否重复
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', 'errmsg')

        # 校验用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请确认协议'})

        # 进行业务处理，进行用户注册
        # user = User()
        # user.username = username
        # user.password = password
        # user.email = email
        # user.save()
        user = User.objects.creat_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答，跳转到首页
        return redirect(reverse('goods.index'))  # 反向解析namesapce.name



# def register_handle(request):
#     '''进行注册处理'''




