`test`#注册登录时的插入语句
INSERT INTO shopping.`test`(NAME,pwd,email,phone)VALUES('小黑鸽','135791','111111@qq.com','1180250');

#用户可以用用户名,邮箱或者电话号登录
SELECT * FROM shopping.`test` WHERE (NAME='小白鸽' OR phone='1' OR email='1515@qq.com')AND pwd='123456'

#查找用户注册时邮箱和电话号是否已经注册
SELECT * FROM shopping.`test` WHERE email='111111@qq.com' OR phone='1180250'

#查询指定的几条数据
SELECT * FROM shopping.`test` LIMIT 0,5

SELECT shopping.`commodity`.* FROM shopping.`commodity` WHERE shopping.`shoucan`.`shop_id`=shopping.`commodity`.`shop_id`

#模糊查询，搜索商品
SELECT * FROM commodity WHERE (titles LIKE '%99%') OR (shop_id = '11')

#查询店铺
SELECT * FROM commodity WHERE stores = '神舟电脑'

#查找指定店铺对应的商品信息
SELECT * FROM commodity WHERE stores = '神舟电脑' AND titles LIKE '%战神%'`commodity`

#查找店铺的几条数据，放到商品详情的店家推荐中
SELECT * FROM shopping.`commodity` WHERE stores='神舟电脑' LIMIT 2

#用户表和收藏表（购物车表）一起查询，用户收藏的商品id和用户名
SELECT * FROM shoucan,commodity WHERE shoucan.`shop_id`=commodity.`shop_id` AND shoucan.`user_name`='小白鸽'

#商品详情表和购物车表一起查询，查找指定的数据（购物车表中有用户的名字信息）？？？
SELECT * FROM cart,commodity WHERE cart.`shop_id`=commodity.`shop_id` AND cart.`u_name`='小白鸽'

#查询购物车中，指定用户的购物车信息
SELECT * FROM cart WHERE cart.`u_name`='小白鸽' LIMIT 3

#用户往购物车表中添加商品，添加的是用户名，商品id，总价格，个数，
INSERT INTO cart(shop_id,u_name,img,title,stores,DATE,prices,number,state) VALUES('12','小白鸽','jpg','微软 Surface Laptop','微软小店','2018-04-26',6800,1,'0');

#店铺的收藏人气就是店铺在店铺收藏表中的个数，用Count来统计
SELECT COUNT(store) FROM Collection

#删除指定的行
DELETE FROM shoucan WHERE user_name='小黑' AND shop_id='122'

#删除购物车订单
DELETE FROM cart WHERE u_name='小白鸽' AND shop_id='21' AND id=20

#销量的降序
SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY Sales DESC

#价格的降序
SELECT * FROM commodity WHERE titles LIKE '%笔记本%' ORDER BY prices DESC

#每有一个商品被收藏则加1
UPDATE commodity SET collect = collect+1 WHERE shop_id='11'

#店铺内的价格排序
SELECT * FROM commodity WHERE stores='神舟电脑'  ORDER BY prices DESC

#搜索后再排序
SELECT * FROM commodity WHERE stores='神舟电脑' AND titles LIKE '%%' ORDER BY prices DESC


#更新个人信息
UPDATE test SET real_name='小白',address='湖南省长沙市麓谷信息港A栋',birthday='1995-12-12',sex='男' WHERE NAME='小白鸽'

#更新商品的收藏次数，如果有用户收藏则加1
UPDATE commodity SET collect=collect+1 WHERE shop_id='11'

SELECT * FROM commodity WHERE shop_id='559645653449'





