from django.urls import path, re_path

# from apps.goods.views import IndexView
from apps.goods.views import IndexView

app_name = 'goods'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='index2'),
]
