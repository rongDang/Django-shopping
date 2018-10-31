# -*- coding:utf8 -*-
from django.conf.urls import url
from django.contrib import admin
from . import View
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    #首页的链接
    url(r'^index$', View.index),
    #登录和注册的链接
    url(r'^login$', View.login),
    url(r'^sign$', View.sign),
    # 判断注册信息
    url(r'^is_sign$', View.is_sign),
    # 判断登录信息
    url(r'^is_login$', View.islogin),
    # 商品详细页面
    url(r'^Xiangq$', View.Xiang_q),
    # 用户的个人中心
    url(r'^vip$', View.Vipcenter),
    # 退出登录
    url(r'^log_out$', View.log_out),
    # 搜索展示的列表
    url(r'^search$',View.search),
    # 显示不同种类的东西
    url(r'^search_kind',View.search_kind),
    # 列表页中按照销量，价格排序
    url(r'^sales$',View.sales),
    url(r'^prices$',View.prices),
    # 店铺详情页面的信息
    url(r'^store$', View.store),
    # 在店铺内查找商品
    url(r'^find$', View.search_store),
    # 店铺内商品价格的降序
    url(r'^store_price',View.store_price),
    # 店铺内商品销量的降序
    url(r'^store_sales',View.store_sales),
    # 店铺内商品收藏的降序
    url(r'^store_collect',View.store_collect),
    # 添加商品到购物车
    url(r'^add_cart$', View.add_cart),
    # 添加商品收藏
    url(r'^add_shop$',View.add_shop),
    url(r'^add_store$',View.add_store),
    # 我的购物车页面
    url(r'^cart$', View.my_cart),
    # 我的商品收藏页面
    url(r'^shop_cang$', View.shop_cang),
    # 我的店铺收藏
    url(r'^store_cang$', View.store_cang),
    # 删除收藏的店铺
    url(r'^Dstore$', View.del_store),
    # 删除所有收藏的店铺
    url(r'^Del_all_store$',View.D_allstore),
    # 删除购物车信息
    url(r'^Dcart$',View.D_cart),
    # 删除收藏的商品
    url(r'^Dshop$',View.D_shop),
    # 用户资料修改页面
    url(r'^vip_amend$',View.vip_amend),
    url(r'^amend_vip',View.amend_user),
    # 立刻购买页面
    url(r'^buy$',View.buy),
    # 账号安全
    url(r'^secure$',View.secure),
    # 修改绑定邮箱页面
    url(r'^amend_mail',View.amend_mail),
    # 随机产生验证码
    url(r'^send$',View.send),
    url(r'^send1$',View.send1),
    # 进入到修改手机页面
    url(r'^amend_phone$',View.amend_phone),
    url(r'^send_phone$',View.send_p),
    url(r'^send2$',View.send2),
    # 修改密码页面
    url(r'^amend_pwd',View.amend_pwd),
    url(r'^send3$',View.send3),
    # 取消订单操所
    url(r'^update_cart$',View.update_cart),
    url(r'^update_cart1$',View.update_cart1)
    # url(r'^aaa',View.aaaa)
]



