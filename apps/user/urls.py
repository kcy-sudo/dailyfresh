from django.urls import path, re_path
from apps.user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView

app_name = 'user'

urlpatterns = [
    # path('register/', views.register, name='register'),  # 注册
    # path('register_handle/', views.register_handle, name='register_handle'),  # 注册处理
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    path('order/', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    path('address/', AddressView.as_view(), name='address'),  # 用户中心-地址页
    re_path('active/(?P<token>.*)/', ActiveView.as_view(), name='active'),  # 用户激活
    path('login/', LoginView.as_view(), name='login'),  # 登录

]
