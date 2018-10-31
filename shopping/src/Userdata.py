# -*- encoding:utf8 -*-
import MySQLdb


# 验证用户登录
def islogin(name, pwd):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # 准备sql语句,用户可以用手机号，用户名或邮箱登录
    # SELECT * FROM shopping.`test` WHERE (NAME='小白鸽' OR phone='1' OR email='1515@qq.com')AND pwd='123456'
    sqlstr = "select * from test where(name='%s' or phone='%s' or email='%s') and pwd='%s'"%(name, name, name, pwd)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的多个数据元组
    result = cursor.fetchall()
    # 关闭数据库连接
    conn.close()
    return result
# print islogin("小白鸽","123456")


# 用户的注册, 用户名，密码，邮箱，手机号码
def add_user(name, pwd, E_mail, phone):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句
    sqlstr = "insert into test(name,pwd,email,phone) values ('%s','%s','%s','%s') "%(name,pwd,E_mail,phone)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()


# 判断注册时的邮箱和手机号码是否存在，如果已经注册则不能再注册。
def judge_sign(E_mail, phone,name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句查询数据库表中是否存在已有的数据
    sqlstr = "select * from test where email='%s' or pwd='%s' or name='%s'"%(E_mail,phone,name)
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print judge_sign("111111@qq.com","1180250")


# # 连接数据库，查询商品表返回商品的数据到首页
# def get_shop():
#     # 连接数据库
#     conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
#     # 获取游标操作数据库
#     cursor = conn.cursor()
#     # sql语句,首页的电子产品模板应该放8条数据
#     sqlstr = "select * from commodity"
#     # 执行sql语句
#     cursor.execute(sqlstr)
#     # 获取查询的数据
#     result = cursor.fetchall()
#     # 关闭连接
#     conn.close()
#     return result


# 获取不同种类的商品
def get_kind(kind):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,首页的电子产品模板应该放8条数据
    sqlstr = "select * from commodity where kind='%d'"%int(kind)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


def get_imgs():
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,首页的电子产品模板应该放8条数据
    sqlstr = "select Himg,Ximg from commodity"
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# for i in  get_imgs()[0:8]:
#     print i


# 通过商品id来获取对应id商品的所有信息
def get_Allshop(shop_id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句
    sqlstr = "select * from commodity where shop_id=%s"%(shop_id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print get_Allshop("11")


# 用户中心的查询，查找该用户是否存在
def get_user(name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句
    sqlstr = "select * from test where(name='%s' or phone='%s' or email='%s')"%(name,name,name)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


# 商品的搜索
# pyhton中存在转义机制%s，sql的模糊查询需要用到%，所以可以把需要进行模糊查询的字符串从sql中单独拎出来进行拼接就好
def check(shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,模糊查询 SELECT * FROM commodity WHERE (titles LIKE '%99%') OR (shop_id = '11')
    args = '%'+shop_name+'%'
    sqlstr = "select * from commodity where (titles like '%s') or (shop_id='%s')"%(args,shop_name)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print check("笔记本")


# 进入店铺，返回数据库中该店铺存在的商品信息
def details(store_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,查找数据库中的店铺,SELECT * FROM commodity WHERE stores = '神舟电脑'
    sqlstr = "select * from commodity where stores = '%s'"%store_name
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print details("神舟电脑")


# 查找指定店铺里面的商品
def find(store_name, shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    args = '%' + shop_name + '%'
    # sql语句,SELECT * FROM commodity WHERE stores = '神舟电脑' AND titles LIKE '%战神%'
    sqlstr = "select * from commodity where stores = '%s' and titles like '%s'" % (store_name,args)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print find("神舟电脑","笔记本")


# 从数据库中获取用户的购物车信息
def shop_cart(username):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,查找数据库中的购物车表，SELECT * FROM cart WHERE cart.`u_name`='小白鸽'
    sqlstr = "select * from cart where u_name = '%s'" % username
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    # 返回前几条数据的代码修改：result[0:2]，实现购物车和后再统改=======
    return result
# print shop_cart2("小白鸽")


# 商品收藏页面，展示所有的收藏商品
def shop_cang(username):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,查找数据库中的购物车表，SELECT * FROM cart WHERE cart.`u_name`='小白鸽'
    sqlstr = "select * from shoucan where user_name = '%s'" % username
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print shop_cang1("小白鸽")


# 从数据的店铺收藏表中获取数据
def store_cang(username):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,查找数据库中的购物车表，SELECT * FROM cart WHERE cart.`u_name`='小白鸽'
    sqlstr = "select * from collection where username = '%s'" % username
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


# 进入店铺时候从店铺收藏表中查看用户是否收藏该店铺
def judge_store(username,store):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,查找数据库中的购物车表，SELECT * FROM cart WHERE cart.`u_name`='小白鸽'
    sqlstr = "select * from collection where username='%s' and store='%s'" % (username,store)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


# 查询用户是否有收藏某商品
def jugde_cang(username,id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,查找数据库中的购物车表，SELECT * FROM cart WHERE cart.`u_name`='小白鸽'
    sqlstr = "select * from shoucan where user_name = '%s' and shop_id='%s'" % (username, id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


# 加入购物车的操作，往数据库中插入数据
def add_cart(shop_id, username, img, title, stores, time, prices, number, state):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1","root","root","shopping",charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句，INSERT INTO cart(shop_id,u_name,img,title,stores,DATE,prices,number,state) VALUES('12','小白鸽','http://','微软 Surface Laptop','微软小店','2018-04-26',6800,1,'0');
    sqlstr = "insert into cart(shop_id,u_name,img,title,stores,DATE,prices,number,state) VALUES('%s','%s','%s','%s','%s','%s','%d',%d,'%s')"%(shop_id,username,img,title,stores,time,prices,number,state)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# add_cart("14","小黑","56315312","97845631","炉石笔记本","2018-4-24",6800,1,"0")


# 添加商品到收藏表中
def add_shop(user_name,shop_id,img,store,title,price):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句，INSERT INTO cart(shop_id,u_name,img,title,stores,DATE,prices,number,state) VALUES('12','小白鸽','http://','微软 Surface Laptop','微软小店','2018-04-26',6800,1,'0');
    sqlstr = "insert into shoucan(user_name,shop_id,img,store,title,price) VALUES('%s','%s','%s','%s','%s','%d')" % (user_name,shop_id,img,store,title,int(price))
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()


# 添加店铺收藏
def add_store(username,store,time):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句，插入到
    sqlstr = "insert into collection(username,store,time) VALUES('%s','%s','%s')" % (username, store, time)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()


# 删除指定的数据，收藏的店铺里的数据
def del_store(username, store):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,
    sqlstr = "delete from collection where username='%s' AND store='%s'"%(username, store)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# del_store("小白鸽", "测试")


# 删除所有的店铺收藏
def D_allstore(username):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,
    sqlstr = "delete from collection where username='%s'" % username
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# D_allstore("小白鸽")


# 删除订单信息
def D_cart(username, shop_id, id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,
    sqlstr = "delete from cart where u_name='%s' and shop_id='%s' and id='%d'" % (username, shop_id, id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# D_cart("小白鸽","1111",21)


# 删除收藏的商品
def D_shop(username, id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,
    sqlstr = "delete from shoucan where user_name='%s' and shop_id='%s'" % (username, id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# D_shop("小白鸽","19")


# 用户查询后按照销量高低查询
def sales_desc(shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    args = '%'+shop_name+'%'
    sqlstr = "select * from commodity where titles like '%s' order by Sales desc"%args
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print sales_desc("")


def sales_desc_kind(shop_name,kind):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    args = '%'+shop_name+'%'
    sqlstr = "select * from commodity where titles like '%s' and kind='%d' order by Sales desc"%(args,int(kind))
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


# 按照价格降序
def price_desc(shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    args = '%'+shop_name+'%'
    sqlstr = "select * from commodity where titles like '%s' order by prices desc"%args
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print price_desc("笔记本")


def price_desc_kind(shop_name,kind):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    args = '%'+shop_name+'%'
    sqlstr = "select * from commodity where titles like '%s' and kind='%d' order by prices desc"%(args,int(kind))
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result


# 店铺内的价格降序
def S_price_desc(store,shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    args = '%' + shop_name + '%'
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    sqlstr = "select * from commodity where stores='%s'and titles like '%s' order by prices desc"%(store,args)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print S_price_desc("神舟电脑","1050")


# 店铺内的销量降序
def S_sales_desc(store,shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    args = '%' + shop_name + '%'
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    sqlstr = "select * from commodity where stores='%s'and titles like '%s' order by Sales desc"%(store,args)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print S_sales_desc("神舟电脑","笔记本")


# 店铺内的商品收藏次数降序
def S_collect_desc(store,shop_name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    args = '%' + shop_name + '%'
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    sqlstr = "select * from commodity where stores='%s'and titles like '%s' order by collect desc"%(store,args)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print S_collect_desc("神舟电脑","笔记本")


# 用户的信息更新
def update_user(real_name,address,birthday,sex,name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE test SET real_name='小白',address='湖南省长沙市麓谷信息港A栋',birthday='1995-12-12',sex='男' WHERE NAME='小白鸽'
    sqlstr = "update test set real_name='%s',address='%s',birthday='%s',sex='%s' where name='%s' " % (real_name,address,birthday,sex,name)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# update_user("小白","湖南省长沙市岳麓区麓谷大道","1994-12-12","男","小白鸽")


# 个人资料修改,查询该用户的资料放到页面中
def personal(pwd,phone):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    sqlstr = "select * from test where pwd='%s'and phone='%s'" % (pwd, phone)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print personal("12345678910","18807395853")


# 每有一件商品被收藏则更新表中的收藏次数
def update_shop_collect(shop_id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE commodity SET collect=collect+1 WHERE shop_id='11'
    sqlstr = "update commodity set collect=collect+1 where shop_id='%s'" % (shop_id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# update_shop_collect("11")


# 在搜索的列表页中所展示的热销商品
def guess(shop_name,i):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    args = '%' + shop_name + '%'
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    sqlstr = "select * from commodity where titles like '%s' and kind='%d' order by Sales desc" % (args,int(i))
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print guess("笔记本")


# 在商品详情页中显示瞧了又瞧，这里显示的是同种类商品被收藏最多的
def look(kind):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC
    sqlstr = "select * from commodity where kind='%d' order by collect desc" % int(kind)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 获取查询的数据
    result = cursor.fetchall()
    # 关闭连接
    conn.close()
    return result
# print look(1)


# 更新用户表中的邮箱
def update_mail(mail,name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE commodity SET collect=collect+1 WHERE shop_id='11'
    sqlstr = "update test set email='%s' where name='%s'" % (mail,name)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()


# 更新用户表中的邮箱
def update_phone(phone,name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE commodity SET collect=collect+1 WHERE shop_id='11'
    sqlstr = "update test set phone='%s' where name='%s'" % (phone,name)
    #` 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()


# 更新用户表中的邮箱
def update_pwd(pwd,name):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE commodity SET collect=collect+1 WHERE shop_id='11'
    sqlstr = "update test set pwd='%s' where name='%s'" % (pwd,name)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()


# 更新数据中的购物车表订单状态
def update_cart(name,id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE commodity SET collect=collect+1 WHERE shop_id='11'
    sqlstr = "update cart set state=-1 where u_name='%s' and shop_id='%s'" % (name,id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()
# update_cart("小白鸽","10")


# 付款后更新状态
def update_cart1(name,id):
    # 连接数据库
    conn = MySQLdb.connect("127.0.0.1", "root", "root", "shopping", charset="utf8")
    # 获取游标操作数据库
    cursor = conn.cursor()
    # sql语句,UPDATE commodity SET collect=collect+1 WHERE shop_id='11'
    sqlstr = "update cart set state=1 where u_name='%s' and shop_id='%s'" % (name,id)
    # 执行sql语句
    cursor.execute(sqlstr)
    # 提交数据
    conn.commit()
    # 关闭数据库连接
    conn.close()

