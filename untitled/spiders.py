#-*- coding: utf-8-*-
#淘宝神舟笔记本商品的图片 价格 商品名称的爬取
import requests
import re
import urllib2
import MySQLdb
from bs4 import BeautifulSoup as bs
import sys
import time
import urllib

#Requests 可以为 HTTPS 请求验证 SSL 证书，就像 web 浏览器一样。
# SSL 验证默认是开启的，如果证书验证失败，Requests 会抛出 SSLError
import urllib3.contrib.pyopenssl

#selenium可以模拟真实浏览器，自动化测试工具
# 支持多种浏览器，爬虫中主要用来解决JavaScript渲染问题
from  selenium import webdriver



#设置字符集的编码格式
if sys.getdefaultencoding() !='utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


#连接数据库,存储淘宝列表的数据
def mysq_lj(spid,name,price,img,dianpu,xia_b):
    conn=MySQLdb.connect("localhost","root","root",'shopping',charset='utf8')
    cursor=conn.cursor()
    sqlstr='insert into commodity values("%s","%s","%s","%s","%s","%s")' %(spid,name,price,img,dianpu,xia_b)
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()


#连接数据库，存储详情页的数据
def mysql_xq(shop_id,stores,titles,price,Sclass,Stype,Zimg,Himg,Ximg,Sales,collect,kind):
    conn = MySQLdb.connect("127.0.0.1", "root", "root", 'shopping', charset='utf8')
    cursor = conn.cursor()
    sqlstr = "insert into commodity values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(shop_id,stores,titles,price,Sclass,Stype,Zimg,Himg,Ximg,Sales,collect,kind)
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()


#打开网页，获取网页内容
def url_open(url):

    headers = {
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'https://s.taobao.com/search?q=%E6%B8%B8%E6%88%8F%E5%B9%B3%E6%9D%BF%E7%94%B5%E8%84%91&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180504&ie=utf8'
    }
    # #urllib2.urlopen()函数不支持验证、cookie或者其它HTTP高级功能。m
    # # 要支持这些功能，
    # # 必须使用build_opener()函数创建自定义Opener对象。
    # opener=urllib2.build_opener()
    # opener.addheaders=[headers]
    # urllib2.install_opener(opener)
    # req=urllib2.Request(url,headers=headers)
    # data=urllib2.urlopen(req).read().decode("utf-8")
    res=requests.get(url,headers=headers)
    return res.url

def main():

      kewd='电脑cpu'
      xia_b=5
      #定义获取页面的页数
      num=1
      # 对keywd进行url编码
      keywords=urllib2.quote(kewd)
      print '正在爬取'+kewd+'的数据'
      print '----'
      for i in range(num):
        # 获取网址
        inde=str((i)*44)
        url = "http://s.taobao.com/search?q=%s&imgfile=&ie=utf8&s=%s"%(keywords,str(inde))

        uu2 = str(url_open(url))
        print url
        data=requests.get(uu2).text


        # 匹配各个字段的正则
        nid_pat='"nid":"(.*?)"'
        img_pat = '"pic_url":"(//.*?)"'
        name_pat = '"raw_title":"(.*?)"'
        price_pat = '"view_price":"(.*?)"'
        nick_pat='"nick":"(.*?)"'
        sales_pat='"view_sales":"(.*?)"'
        com_pat='"comment_count":"(.*?)"'

        #查找出正则表达式匹配的数据
        idL=re.compile(nid_pat).findall(data)
        imgL = re.compile(img_pat).findall(data)
        nameL=re.compile(name_pat).findall(data)
        priceL=re.compile(price_pat).findall(data)
        nickL=re.compile(nick_pat).findall(data)
        saleL=re.compile(sales_pat).findall(data)
        sh_caL=re.compile(com_pat).findall(data)
        print('正在爬取'+str(i+1)+"页的数据：")
        for j in range(len(nameL)):
             if sh_caL[j]==None:
                 shou_cang='0'
             else:
                 shou_cang=str(sh_caL[j])

             sale= re.search('[0-9]+',str(saleL[j])).group()
             print('第' + str(i + 1) + "页的 " + "第" + str(j + 1) + "件商品的id")
             spid=idL[j]
             print(spid)
             print('第'+str(i+1)+"页的 "+"第"+str(j+1)+"张图片链接")
             img = "http:" + imgL[j]  # 商品图片链接
             print(img)
             print('第' + str(i+1) + "页的：第"+str(j+1)+"件的商品名称：")
             name = nameL[j]+""  # 商品名称
             print(name)
             print('第' + str(i+1) + "页的 第"+str(j+1)+"件商品的价格：")
             price=priceL[j]
             pp=float((price.encode('utf-8')))
             print((pp))
             print('第' + str(i + 1) + "页的 第" + str(j + 1) + "件商品的店铺名称：")
             nick=nickL[j]
             print nick
             #if name:
             if pp>200:
             #if(re.search('.*电脑?$|.*游戏本?$|.*轻薄',str(name))):
                 print("正在存储第" + str(i + 1) + "页第" + str(j + 1) + "条数据:")
                 # 将unicode形式转换为utf-8形式
                 # 将爬取出来的列表存进去
                 #mysq_lj(str(spid), name.encode('utf-8'), str(price), str(img), nick.encode('utf-8'), str(xia_b))
                 print "存储完毕======================================="
                 print "**********======================================="
                 # 详情页
                 sp_xq(str(spid), str(xia_b),sale,shou_cang,name.encode('utf-8'),str(price),nick.encode('utf-8'))


        print("完成对第"+str(i+1)+"页数据的爬取")
        print "*********************************"
        print("********************************")

    #爬取详情页的数据并且保存到数据库中


#####################
######################
####失败#############
#本来可以进行爬取月销量，由于天猫检测爬虫的更新，
# 会把你跳转到登陆页面：
#https://login.tmall.com/?from=sm&redirectURL=https%3A%2F%2Fsec.taobao.com%2Fquery.htm%3Faction%3DQueryAction%26event_submit_do_login%3Dok%26smApp%3Dmalldetailskip%26smPolicy%3Dmalldetailskip-init-anti_Spider-checklogin%26smCharset%3DGBK%26smTag%3DNDMuMjUwLjIwMC43MiwsN2NkNzJmNmRkZWUyNDBmMDlmNGJkNWE5Nzg5ZTcwNzg%253D%26captcha%3Dhttps%253A%252F%252Fsec.taobao.com%252Fquery.htm%26smReturn%3Dhttps%253A%252F%252F
# detail.tmall.com%252Fitem.htm%253Fspm%253Da230r.1.14.6.426e1c62Q2u0Xp%2526id%253D544959480906%2526cm_id%253D140105335569ed55e27b%2526abbucket%253D10%2526sku_properties%253D5919063%253A6536025%2526sm%253Dtrue%26smSign%3DnbN5%252BnNwmIrLDurY5Uk5bg%253D%253D
#进行模拟登陆之后会把你跳转到另一个验证码的界面：
#https://sec.taobao.com/query.htm?smApp=malldetailskip&smPolicy=malldetailskip-init-anti_Spider-checklogin&smCharset=GBK&smTag=NDMuMjUwLjIwMC43MiwsOGU2MTY0YmU5OGZhNDJkYzhhOWIwZmNkMDAyMTlmYjI%3D&smReturn=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm%3Da230r.1.14.6.7d701672sEROMG%26id%3D543489254259%26cm_id%3D140105335569ed55e27b%26abbucket%3D10%26sku_properties%3D5919063%3A6536025%26sm%3Dtrue&smSign=PGgAG8OFWvwWqQUzsCtsWg%3D%3D&captcha=https%3A%2F%2Fsec.taobao.com%2Fquery.htm
#所以换了方法
# def pa(url):
#     head={
#         'accept':'*/*',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
#         'Connection': 'keep-alive',
#         'Referer': 'https://detail.tmall.com/item.htm?spm=a230r.1.14.6.7d701672sEROMG&id=543489254259&cm_id=140105335569ed55e27b&abbucket=10&sku_properties=5919063:6536025',
#         'cookie': 'cna=RWFpEyWKCkwCAXb6tIi5g4Hu; isg=BAcHaqe8EXuBUpX3bRiB1iPUlrsRpPDViJ8dmdn0ZBa9SCcK4dxrPkWJ7wgWgbNm'
#     }
#
#     res=requests.get(url,headers=head)
#     print url
#     print "--"
#     print res.text
#     if(re.search('window.location.href',res.text)):
#         url2=re.search("'.*?'",res.text).group().replace("'","")
#         print url2
#         print ("sdfjlasdkf")
#         print requests.get(url2).url
#         post_data = urllib.urlencode(
#             {
#                 'TPL_password': 'ls991006',
#                 'TPL_username': '17674001909',
#             })
#         headers=[('accept','*/*'),
#                 ('Accept-Language', 'zh-CN,zh;q=0.9'),
#                 ('Cache-Control', 'max-age=0'),
#                              ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'),
#                              ('Connection', 'keep-alive'),
#                              ('Referer', 'https://detail.tmall.com/item.htm?spm=a230r.1.14.6.7d701672sEROMG&id=543489254259&cm_id=140105335569ed55e27b&abbucket=10&sku_properties=5919063:6536025'),
#                              ('cookie', 'cna=RWFpEyWKCkwCAXb6tIi5g4Hu; isg=BAcHaqe8EXuBUpX3bRiB1iPUlrsRpPDViJ8dmdn0ZBa9SCcK4dxrPkWJ7wgWgbNm')]
#
#         opener = urllib2.build_opener()
#         opener.addheaders = headers
#         urllib2.install_opener(opener)
#         req = urllib2.Request(url, post_data)
#         data = urllib2.urlopen(req).read().decode("utf8",'ignore')
#         url3 = re.search("'.*?'", res.text).group().replace("'", "")
#         print requests.get(url3).url
#         print data
#         sell_mouse_str = re.search('"sellCount":.*?,', str(res.text))
#
#         pass
#
#     else:
#        sell_mouse_str= re.search('"sellCount":.*?,',str(res.text))
#
#     print sell_mouse_str
#
#     sell_mouse=re.search('[1-9]\d*',sell_mouse_str.group()).group()
#     print sell_mouse
#     return sell_mouse



#淘宝详情页的爬取
def taobao_sp(url,id,xia_b,sale,shou_cang,title,price,stores):
    sp_jjimg=''
    color=""
    tctype=""
    spimg=""
    Zimgs=[]

    print ('正在爬取id为：'+id+'的淘宝详情页的数据')

    # 请求网址
    res = requests.get(url)
    sL='"src":"(^https://tds.alicdn)"'

    # 解析网址
    soup = bs(res.text, "lxml")
    ss = soup.find_all('a', attrs={'href': '#'})

    #匹配符合要求的标签
    coul = soup.find_all('ul', attrs={'class': 'J_TSaleProp tb-img tb-clearfix'})
    tcul=soup.find_all('ul',attrs={'class':re.compile(r'^J_TSaleProp tb-clearfix')})
    sS=re.compile("sellerId         : '.*?'").findall(res.text)
    sk=re.compile("shopId           : '.*?'").findall(res.text)
    sell_u=re.compile("apiRelateMarket  : '.*',").findall(res.text)

    #获取sellerId
    sids= re.compile("'.*?'").findall(sS[0])
    sid= sids[0].replace("'",'')

    #获取shopid
    shop_ids=re.search("'.*?'",sk[0]).group().replace("'","")



    #获取商品介绍图的js文件地址
    x_url = re.compile('descUrl          : lo.*').findall(res.text)
    uu=re.search("'//desc.alicdn.com.*'",str(x_url[0]))


    url2= "http:"+uu.group().replace("'","")

    res2=requests.get(url2)

    #匹配商品介绍图
    results=re.compile('src=".*?.jpg|src=".*?.png|src=".*?.gif').findall(res2.text)
    print results
    for result in results:
        u=re.search('//.*',str(result))
        resul=u.group().replace('"','')
        sp_jjimg=sp_jjimg+'http'+resul+','





    # i=0
    # j= 500
    # browser=webdriver.Chrome()
    # browser.get(res.url)

    # while i<8000:
    #     i=str(i)
    #     j=str(j)
    #     browser.execute_script('window.scrollBy("'+i+'","'+j+'")')
    #     time.sleep(2)
    #     i,j=int(i),int(j)
    #     i+=500
    #     j+=500
    # link = browser.find_element_by_xpath('//*[@id="J_DivItemDesc"]/table/tbody/tr[2]/td')
    # print(link.get_attribute('colspan'))
    #
    # for src in browser.find_elements_by_xpath('//*[@id="J_DivItemDesc"]/table/tbody/tr[2]/td/img'):
    #     print(src.get_attribute('src'))


    #获取图片
    for i in ss:
       img=i('img')

       for src in img:
           d_src_str=src['data-src']
           d_src=str(d_src_str).replace('50x50','400x400')
           Zimgs.append(d_src)
           if(re.search('http:',d_src)):
               spimg=spimg+d_src+','
           else:
               spimg=spimg+'https:'+d_src+","

       Zimg=Zimgs[0]

    #爬取颜色分类
    for j in coul:
        cospan=j.find_all('span')

        color=cospan[0].text


    #爬取套餐类型
    for k in tcul:
        tcspan=k.find_all('span')

        tctype=tcspan[0].text

    print("爬取成功")
    print("*******************")
    print("正在把爬取的数据存储到数据库中")
    mysql_xq(id,stores,title,price ,color, tctype, Zimg,spimg,sp_jjimg,sale,shou_cang,xia_b)
    # if flag:
    print("存储成功")
    #  print("=====")
    # else:
    #     print "存储失败"
    #     print "---------"

#天猫详情页数据的爬取
def tmall_sp(url,id,xia_b,sale,shou_cang,title,price,stores):
    sp_jjimg=""
    color = ""
    tctype = ""
    spimg = ""
    Zimgs=[]
    print ('正在爬取id为：' + id + '的天猫详情页的数据')



    #请求网址
    res=requests.get(url)
    #解析网址
    soup=bs(res.text,"lxml")

    #匹配符合要求的字段
    ss=soup.find_all('a',attrs={'href':'#'})
    coul=soup.find_all('ul',attrs={'class':re.compile(r'tb-img$')})
    tcul=soup.find_all('ul',attrs={'class':'tm-clear J_TSaleProp '})
    spjs=soup.find_all('img')
    sS = re.compile('sellerId:".*?"').findall(res.text)
    sids = re.compile('".*?"').findall(sS[0])
    sid = sids[0].replace('"', '')


    x_url=re.compile('"descUrl":".*?"').findall(res.text)
    xx=re.search('"//.*"',str(x_url))
    url2='http:'+xx.group().replace('"','')




   #商品详情页面的商品介绍图
    res2 = requests.get(url2)

    sp_jjimgs=re.compile('src="(.*?)"').findall(res2.text)

    for x in sp_jjimgs:
         src=str(x).replace('"',"")

         sks= re.search('.*img.alicdn.com.*',src)

         if sks:
               sp_jjimg = sp_jjimg + sks.group() + ","

         # 获取月销量的网址又一次失败的尝试，用selinum时还是会跳转到登陆页面
    # sell_str = re.compile("var l,url='.*?'").findall(res.text)[0]
    # sell_url = 'http:' + re.search("'.*?'", str(sell_str)).group().replace("'", "")
    # browser = webdriver.Chrome()
    # browser.get(res.url)
    # time.sleep(0.5)
    # try:
    #   sell_mouth_str = browser.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]')
    #   sell_mouse=str(sell_mouth_str.text)
    # except:
    #     sell_mouse='670'
    # print sell_mouse


    #browser.close()


   #颜色分类
    for j in coul:
        cosp=j.find_all('span')
        color=cosp[0].text


    #套餐类型
    for k in tcul:
        tcsps = k.find_all('span')
        tctype=tcsps[0].text

    #商品图片
    for i in ss:
       imgs=i('img')

       for img in imgs:
           d_src_str = img['src']
           d_src = str(d_src_str).replace('60x60', '400x400')
           Zimgs.append('https:'+d_src)
           spimg = spimg + 'https:' + d_src + ","

    Zimg=Zimgs[0]


    print("爬取成功")
    print('++++++++++++++++++++++')
    print("正在把爬取的数据存储到数据库中")
    #把数据存入到数据库中

    mysql_xq(id,stores,title,price ,color, tctype,Zimg,spimg,sp_jjimg,sale,shou_cang,xia_b)

    print("存储成功")
    print("=====")



#由于商品列表中有很多天猫的 所以需要分别爬取淘宝和天猫的详情数据
def sp_xq(ids,xia_b,sale,shou_cang,title,price,stores):
    start_url='https://item.taobao.com/item.htm?id='
    urls_list=start_url+str(ids)
    #请求网址，返回一个处理后的网址
    res=requests.get(urls_list)


    #判断网址是天猫还是淘宝
    if(re.search('tmall',res.url)):
        print('天猫')
        tmall_sp(res.url,ids,xia_b,sale,shou_cang,title,price,stores)
    else:
        print('淘宝')
        taobao_sp(res.url,ids,xia_b,sale,shou_cang,title,price,stores)



#taobao_sp('https://item.taobao.com/item.htm?spm=a230r.1.14.34.606a6a88GS21Xd&id=566603345868&ns=1&abbucket=12#detail','566603345868','2')
#tmall_sp('https://detail.tmall.com/item.htm?spm=a230r.1.14.6.426e1c62Q2u0Xp&id=544959480906&cm_id=140105335569ed55e27b&abbucket=10&sku_properties=5919063:6536025','544959480906','5')

main()
