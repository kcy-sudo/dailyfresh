from django.shortcuts import render, redirect, reverse, HttpResponse
import re
from apps.user.models import User
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,  SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


# user/register/
def register(request):
    """显示注册页面"""
    if request.method == 'GET':
        # 显示注册页面
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 进行注册处理
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据处理

        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不匹配'})

        # 检验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoseNotExist:
            # 用户名不存在
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 进行业务处理 ： 进行用户注册
        # user = User()
        # user.username = username
        # user.password = password
        # user.save()
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))



# user/register_handld
def register_handle(request):
    """进行注册处理"""
    pass

class RegisterView(View):
    """注册"""
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 进行注册处理
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据处理

        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不匹配'})

        # 检验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})


        # 进行业务处理 ： 进行用户注册
        # user = User()
        # user.username = username
        # user.password = password
        # user.save()
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户身份信息，并且要把身份信息加密

        # 加密用户身份信息,生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        # 发邮件


        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''激活'''
    def get(self, request, token):
        # 展示激活页面
        try:
            serializer = Serializer(settings.SECRET_KEY, 3600)
            # print(type(token))
            token = token.encode()
            info = serializer.loads(token)
            # 获取激活用户的id
            user_id = info['confirm']

            # 通过id获取用户
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            # 链接失效
            return HttpResponse('激活链接已失效')


#user/login
class LoginView(View):
    '''登录'''
    def get(self, request):
        '''显示登录页面'''
        return render(request, 'login.html')




