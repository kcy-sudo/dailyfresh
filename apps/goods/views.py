from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
from django.core.cache import cache
from apps.goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner, GoodsSKU
from apps.order.models import OrderGoods

# Create your views here.


# goods/index
class IndexView(View):
    """首页"""

    def get(self, request):
        """首页"""
        # 获取用户信息
        user = request.user

        # 判断缓存
        try:
            context = cache.get('index_page_data')
        except Exception as e:
            context = None

        if context is None:
            # 没有缓存数据
            # 获取商品种类信息
            types = GoodsType.objects.all()

            # 获取首页轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')

            # 获取首页促销商品信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            # 获取分类商品展示信息
            for type in types:
                image_goods_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
                font_goods_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)
                type.image_goods_banners = image_goods_banners
                type.font_goods_banners = font_goods_banners

            # 组织上下文
            context = {
                'types': types,
                'goods_banners': goods_banners,
                'promotion_banners': promotion_banners,
            }
            # 设置缓存
            cache.set('index_page_data', context, 3600)

        # 获取购物车中商品数量
        cart_count = 0
        if user.is_authenticated:
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_{0}'.format(user.id)
            cart_count = conn.hlen(cart_key)

        context.update(user=user, cart_count=cart_count)

        return render(request, 'index.html', context)



