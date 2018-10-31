# -*- encoding:utf8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from src import Userdata,send_email,send_phone
from random import randint
from django.views.decorators.csrf import csrf_exempt
import json

# 首页的控制器，如果直接进入首页，没有携带数据如何显示
def index(request):
    name = request.session.get("name")
    # 首页上方的购物车信息显示
    cart = Userdata.shop_cart(name)
    # 获取数据库中不同种类的商品
    result = Userdata.get_kind(1)
    result1 = Userdata.get_kind(3)
    result2 = Userdata.get_kind(5)
    result3 = Userdata.get_kind(4)
    result4 = Userdata.get_kind(2)
    data = {
        "shuju": result[0:8],
        "name": name, "cart":cart[0:5],
        "shuju1":result1[0:8],"shuju2":result2[0:8],"shuju3":result3[0:8],"shuju4":result4[0:8],"shuju5":result[10:15],"shuju6":result4[10:15]
    }
    # 值为0则表示关闭浏览器session直接过期，如果值是int类型，则表示在多少秒后过期
    # request.session.set_expiry(600)
    return render(request, "index.html", data)


# 退出登录的函数,bug刷新会再执行，然而session中没有用户信息了
def log_out(request):
    # 从数据库中获取数据放到网页中去
    result = Userdata.get_kind(1)
    result1 = Userdata.get_kind(3)
    result2 = Userdata.get_kind(5)
    result3 = Userdata.get_kind(4)
    result4 = Userdata.get_kind(2)
    data = {"shuju": result[0:8],"shuju1": result1[0:8], "shuju2": result2[0:8], "shuju3": result3[0:8],"shuju4":result4[0:8],"shuju5":result[10:15],"shuju6":result4[10:15]}
    # 退出登录则删除session保存用户信息
    if request.session.get("name")!=None:
        del request.session["name"]
    return render(request,"index.html",data)
# 判断用户登录，获取登录的信息保存到session中,,,要用到session需要到 cmd 中 运行 python manage.py migrate


# 判断数据库中是否存在用户
def islogin(request):
    # 获取用户名和密码
    name = request.POST["name"]
    pwd = request.POST["pwd"]
    print name,"-----",pwd
    # 从数据库中查询是否存在用户
    result = Userdata.islogin(name,pwd)
    print result
    s = ''
    if len(result)>0:
        print "存在用户"
        # 不能出现result[0][1]
        s = '{"sex":"nan"}'
        request.session["name"] = result[0][1]
        request.session["pwd"] = result[0][2]
        request.session["phone"] = result[0][4]
    else:
        print "不存在用户"
        s = '{}'
    return HttpResponse(s)


# 详情页面
def Xiang_q(request):
    # 获取商品id
    id = request.GET["id"]
    # 获取用户名,从session中获取
    name = request.session.get("name")
    # 点击时获取商品的id，传入到数据库中查询商品
    result = Userdata.get_Allshop(id)
    # 获取店铺名，在详情页面的店家推荐中显示数据
    result1 = Userdata.details(result[0][2])
    # 从收藏表中获取数据，判断用户是否收藏过该商品
    result2 = Userdata.jugde_cang(name,id)
    # 详情页图片数据，和高清大图
    imgs = result[0][9].split(",")
    himg = result[0][8].split(",")
    # 详情页右边的瞧了又瞧，首先获取当前商品的种类，对应种类的商品上去
    kind = result[0][12]
    result3 = Userdata.look(kind)
    data = {"shuju": result, "name": name, "shuju1":result1[0:6],"shuju2":result2,"imgs":imgs,"himg":himg[0:5],"look":result3[0:6]}
    return render(request, "xiangqingye.html", data)


# 登录视图
def login(request):
    return render(request, "login.html")


# 注册视图
def sign(request):
    return render(request, "sign_in.html")


# 判断注册的账号信息是否存在
def is_sign(request):
    mail = request.POST["mail"]
    phone = request.POST["phone"]
    name = request.POST["name"]
    pwd = request.POST["pwd"]
    # 查询获得返回的数据
    result = Userdata.judge_sign(mail, phone,name)
    # 把返回的数据拼接为json的数据形式
    # jsonstr = json.dumps(result, ensure_ascii=False)
    print result
    print mail,phone,name,pwd
    r = ''
    if len(result)>0:
        print "注册信息存在，进入到了这里"
        r = '{"name":"zx","sex":"nan"}'
    else:
        # 如果电话和邮箱不重复则注册成功，把新用户信息插入到数据库中去
        print "79864524563986454564513145665132456"
        Userdata.add_user(name, pwd, mail, phone)
        request.session["name"] = name
        request.session["phone"] = phone
        request.session["pwd"] = pwd
        print "79864524563986454564513145665132456"
        r = '{}'
    return HttpResponse(r)


# 个人中心页面,显示的是用户的购物数据，商品的收藏信息，店铺的收藏信息
def Vipcenter(request):
    # 获取用户名从数据库中查询
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    # 如果用户长时间没有操作，session失效，则进入到登录页面
    if name==None:
        return render(request,"login.html")
    # 从数据库中查找该用户对应的购物车列表，商品收藏的列表，收藏的店铺列表
    result = Userdata.shop_cart(name)
    # 通过用户名查询该用户收藏的商品，店铺，以及购物车商品
    result1 = Userdata.shop_cang(name)
    result2 = Userdata.store_cang(name)
    data = {"name": name, "pwd":len(pwd), "shuju":result[0:5], "shuju1":result1[0:5], "shuju2":result2[0:8]}
    return render(request, "vipcenter.html",data)


# 添加商品到购物车表
def add_cart(request):
    # shop_id,username,img,title,storep,time,price,number,state
    shop_id = request.GET["shop_id"]
    username = request.GET["username"]
    img = request.GET["img"]
    time = request.GET["time"]
    title = request.GET["title"]
    store = request.GET["store"]
    price = request.GET["price"]
    number = request.GET["number"]
    state = request.GET["state"]
    # 把购物车数据插入到数据库
    Userdata.add_cart(shop_id, username, img, title, store, time, int(price), int(number), state)
    return HttpResponse('{}')


# 添加商品到收藏表中
def add_shop(request):
    # 获取链接值，插入到数据库收藏表
    name = request.GET["name"]
    id = request.GET["id"]
    img = request.GET["img"]
    title = request.GET["title"]
    store = request.GET["store"]
    price = request.GET["price"]
    Userdata.add_shop(name,id,img,store,title,price)
    # 更新商品的收藏次数
    Userdata.update_shop_collect(id)
    return HttpResponse('{}')


# 添加店铺收藏
def add_store(request):
    name = request.session.get("name")
    store = request.GET["store"]
    time = request.GET["time"]
    Userdata.add_store(name, store, time)
    return HttpResponse('{}')

# 进入到搜索页面，传入搜索的关键字到数据库进行模糊查询
def search(request):
    # 获取搜索关键字
    shop_name = request.GET["shop_name"]
    name = request.session.get("name")
    # 从数据库中查找数据
    result = Userdata.check(shop_name)
    i = result[0][12]
    # 从数据库中查找对应的销量最高的5条商品数据
    result1 = Userdata.guess(shop_name,i)
    data = {"data": result, "name":name,"shop_name":shop_name,"data1":result1[0:5]}
    return render(request,"liebiaoye.html",data)
# -------------------------------------------------------------------------------------------------


# 搜索后分类的实现,点击后，把kind放到字典中，然后在网页中获取，如果存在则表示被分类，反则没有被分类
def search_kind(request):
    # 获取搜索关键字
    shop_name = request.GET["shop_name"]
    # 获取种类
    kind = request.GET["kind"]
    name = request.session.get("name")
    # 从数据库中查找对应种类的数据
    result = Userdata.get_kind(kind)
    # 从数据库中查找对应的销量最高的5条商品数据
    result1 = Userdata.guess(shop_name,kind)
    data = {"data": result, "name":name,"shop_name":shop_name,"data1":result1[0:5],"kind":kind}
    return render(request,"liebiaoye.html",data)


# 按照销量降序排列
def sales(request):
    # 获取搜索关键字
    shop_name = request.GET["shop_name"]
    name = request.session.get("name")
    # 从数据库中查找数据
    if request.GET["kind"]=="":
        kind = ""
        result = Userdata.sales_desc(shop_name)
    else:
        kind = request.GET["kind"]
        result = Userdata.sales_desc_kind(shop_name,request.GET["kind"])
    # 这里i是对应的分类
    i = result[0][12]
    # 从数据库中查找对应的销量最高的5条商品数据
    result1 = Userdata.guess(shop_name, i)
    data = {"data": result, "name":name,"shop_name":shop_name,"data1":result1[0:5],"kind":kind}
    return render(request,"liebiaoye.html",data)


# 按照价格降序排列
def prices(request):
    # 获取搜索关键字
    shop_name = request.GET["shop_name"]
    name = request.session.get("name")
    # 从数据库中查找数据
    if request.GET["kind"]=="":
        kind = ""
        print shop_name,"4563"
        result = Userdata.price_desc(shop_name)
        print result,"-----"
    else:
        kind = request.GET["kind"]
        result = Userdata.price_desc_kind(shop_name,request.GET["kind"])
    # 这里i是对应的分类
    i = result[0][12]
    # 从数据库中查找对应的销量最高的5条商品数据
    result1 = Userdata.guess(shop_name, i)
    data = {"data": result, "name":name,"shop_name":shop_name,"data1":result1[0:5],"kind":kind}
    return render(request,"liebiaoye.html",data)
#----------------------------------------------------------------------------------------

# 进入到店铺详情页面
def store(request):
    # 获取到店铺的名字，商品表中查找该店铺，和店铺对应的商品信息
    store_name = request.GET["store_name"]
    #  在数据库中查找对应店铺的商品
    result = Userdata.details(store_name)
    # 获取用户名
    name = request.session.get("name")
    # 到店铺收藏表中查询，判断用户是否收藏过该店铺
    result1 = Userdata.judge_store(name,store_name)
    data = {"details": result, "store_name": store_name, "name": name, "details1": result1}
    return render(request,"jinrudianpuxiangqing.html",data)


# 店铺内的搜索，返回的页面还是店铺详情页
def search_store(request):
    # 获取店铺名字和搜索关键字
    store_name = request.GET["store_name"]
    shop_name = request.GET["shop_name"]
    print store_name,"----",shop_name
    name = request.session.get("name")
    # 从数据库中查找指定店铺所查询的商品信息
    result = Userdata.find(store_name,shop_name)
    data = {"details": result,"name":name,"shop_name":shop_name}
    return render(request,"jinrudianpuxiangqing.html",data)


# 店铺内的商品价格降序，
def store_price(request):
    # 获取店铺名字和搜索关键字
    store_name = request.GET["store_name"]
    shop_name = request.GET["shop_name"]
    print store_name,"----",shop_name
    name = request.session.get("name")
    # 从数据库中查找指定店铺所查询的商品信息
    result = Userdata.S_price_desc(store_name,shop_name)
    data = {"details": result,"name":name,"store_name":store_name,"shop_name":shop_name}
    return render(request,"jinrudianpuxiangqing.html",data)


# 店铺内的商品销量降序
def store_sales(request):
    # 获取店铺名字和搜索关键字
    store_name = request.GET["store_name"]
    shop_name = request.GET["shop_name"]
    print store_name,"----",shop_name
    name = request.session.get("name")
    # 从数据库中查找指定店铺所查询的商品信息
    result = Userdata.S_sales_desc(store_name,shop_name)
    data = {"details": result,"name":name,"store_name":store_name,"shop_name":shop_name}
    return render(request,"jinrudianpuxiangqing.html",data)


# 店铺里面的商品收藏降序
def store_collect(request):
    # 获取店铺名字和搜索关键字
    store_name = request.GET["store_name"]
    shop_name = request.GET["shop_name"]
    print store_name,"----",shop_name
    name = request.session.get("name")
    # 从数据库中查找指定店铺所查询的商品信息
    result = Userdata.S_collect_desc(store_name,shop_name)
    data = {"details": result,"name":name,"store_name":store_name,"shop_name":shop_name}
    return render(request,"jinrudianpuxiangqing.html",data)


# 进入到我的购物车详情页面,
def my_cart(request):
    # 获取用户名从数据库中查询
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    result = Userdata.shop_cart(name)
    data = {"shuju":result, "pwd":len(pwd),"name":name}
    return render(request, "wodegouwuche.html", data)


# 进入到我的商品收藏页面
def shop_cang(request):
    # 获取用户名从数据库中查询
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    result = Userdata.shop_cang(name)
    data = {"shuju":result, "pwd":len(pwd),"name":name}
    return render(request, "wodeshoucang.html", data)


# 进入我的店铺收藏页面
def store_cang(request):
    # 获取用户名从数据库中查询
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    result = Userdata.store_cang(name)
    data = {"shuju":result, "pwd":len(pwd) , "name":name}
    return render(request,"woshoucangdedianpu.html",data)


# 进入到修改资料页面,更新用户的一些资料
def vip_amend(request):
    # 获取用户密码,电话
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    phone = request.session.get("phone")
    # 查找指定用户的信息
    result = Userdata.personal(pwd,phone)
    data = {"pwd":len(pwd),"personal":result,"name":name}
    return render(request,"xiugaiziliao.html",data)


# 用户修改资料页面
def amend_user(request):
    name = request.session.get("name")
    # 获取要更新的用户资料
    real_name = request.GET["real_name"]
    sex = request.GET["sex"]
    birthday = request.GET["birthday"]
    address = request.GET["adderss"]
    Userdata.update_user(real_name,address,birthday,sex,name)
    return HttpResponse('{}')


# 进入立即购买页面,没有完成
def buy(request):
    # 获取对应的数据
    name = request.session.get("name")
    # 获取商品信息
    id = request.GET["id"]
    store = request.GET["store"]
    title = request.GET["title"]
    price = request.GET["price"]
    number = request.GET["number"]
    img = request.GET["img"]
    prices = int(price)*int(number)
    data = {"name": name,"id":id,"store":store,"title":title,"price":price,"number":number,"img":img,"prices":prices}
    return render(request,"tianxieheduigouwuxinxi.html",data)


# 进入账户安全页面,没有完成
def secure(request):
    # 获取对应的数据
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    data = {"name":name,"pwd":len(pwd)}
    return render(request,"zhanghuanquan.html",data)


# 修改绑定邮箱，进行验证
def amend_mail(request):
    # 获取对应的数据
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    result = Userdata.get_user(name)
    data = {"name": name, "pwd": len(pwd),"data":result[0]}
    return render(request,"xiugaibangding.html",data)


@csrf_exempt
def send(request):
    mail = request.POST["mail"]
    rand = randint(100000, 999999)
    content = "你的验证码是："+str(rand)+"\n,请不要告诉他人。"
    # 调用发送验证码的方法
    send_email.send(content,mail)
    return HttpResponse(json.dumps({"rand":rand}))


# 到数据库中更新邮箱
def send1(request):
    # 获取对应的数据
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    mail = request.GET["mail"]
    # 更改数据库中的邮箱
    Userdata.update_mail(mail,name)
    data = {"name": name, "pwd": len(pwd)}
    return render(request,"zhanghuanquan.html",data)


# 修改绑定电话，进行验证
def amend_phone(request):
    # 获取对应的数据
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    result = Userdata.get_user(name)
    data = {"name": name, "pwd": len(pwd),"data":result[0]}
    return render(request,"xiugaibangding1.html",data)


@csrf_exempt
def send_p(request):
    phone = request.POST["phone"]
    print phone
    rand = randint(100000, 999999)
    # 您的验证码是：【变量】。请不要把验证码泄露给其他人。
    content = "您的验证码是："+str(rand)+"。请不要把验证码泄露给其他人。"
    # 调用发送验证码的方法,参数是内容和电话号码
    send_phone.send_sms(content, phone)
    return HttpResponse(json.dumps({"rand":rand}))


# 进入到修改密码的页面
def amend_pwd(request):
    # 获取对应的数据
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    data = {"name": name, "pwd": len(pwd)}
    return render(request,"xiugaibangding2.html",data)


# 到数据库中更新电话
def send2(request):
    # 获取对应的数据
    name = request.session.get("name")
    pwd = request.session.get("pwd")
    mail = request.GET["phone"]
    # 更改数据库中的邮箱
    Userdata.update_phone(mail,name)
    data = {"name": name, "pwd": len(pwd)}
    return render(request,"zhanghuanquan.html",data)


# 到数据库中更新密码
@csrf_exempt
def send3(request):
    # 获取对应的数据
    new_pwd = request.POST["new_pwd"]
    name = request.session.get("name")
    request.session["pwd"] = new_pwd
    Userdata.update_pwd(new_pwd,name)
    return HttpResponse('{}')


# 删除店铺指定收藏
def del_store(request):
    # 获取用户名和要删除的店铺名
    name = request.session.get("name")
    store_name = request.GET["store"]
    Userdata.del_store(name, store_name)
    return HttpResponse('{}')


# 删除所有的店铺收藏
def D_allstore(request):
    # 获取用户名
    name = request.session.get("name")
    Userdata.D_allstore(name)
    return HttpResponse('{}')


# 删除购物车信息
def D_cart(request):
    # 获取用户名
    name = request.session.get("name")
    shop_id = request.GET["shop_id"]
    id = request.GET["id"]
    Userdata.D_cart(name, shop_id, int(id))
    return HttpResponse('{}')


# 删除收藏的商品
def D_shop(request):
    # 获取用户名
    name = request.session.get("name")
    id = request.GET["id"]
    Userdata.D_shop(name, id)
    return HttpResponse('{}')


# 进入到我的购物车详情页面,支付后到购物车表中更新状态
def update_cart(request):
    # 获取用户名从数据库中查询
    name = request.session.get("name")
    # 更新数据库中购物车表的状态
    id = request.GET["id"]
    Userdata.update_cart(name,id)
    return HttpResponse('{}')


# 进入到我的购物车详情页面,支付后到购物车表中更新状态
def update_cart1(request):
    # 获取用户名从数据库中查询
    name = request.session.get("name")
    # 更新数据库中购物车表的状态
    id = request.GET["id"]
    Userdata.update_cart1(name,id)
    return HttpResponse('{}')



# def aaaa(request):
#     data = {"aa":[1,2,3,4,5,6,7,8,9]}
#     return render(request,"aaa.html",data)

