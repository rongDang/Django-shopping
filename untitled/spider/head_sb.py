#-*- coding: utf-8-*-
import urllib2,sys,urllib
import ssl
import base64
import re

def access_to():
  # client_id 为官网获取的AK， client_secret 为官网获取的SK
  host='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=W9Q2cn7nZUt8STUaxaBa2K2i&client_secret=oFWYEfv35U0XbmHQyrhZaPEtEACumOHZ'
  request=urllib2.Request(host)
  request.add_header('Content-Type','application/json;charset=UTF-8')
  response=urllib2.urlopen(request)
  content=response.read()
  if(content):
     print content
     #运用正则提取到access_token的值
     ac= re.search('"access_token":".*?"',str(content)).group()
     ac1=re.search(':".*?"',ac)
     ac2=re.search('".*?"',ac1.group())
     access_token=ac2.group().replace('"','')
     return access_token

  else:
      print "00000"

def tt_sb(img_local):
    #二进制方式打开图片文件
    request_url='https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/user_defined'

    f=open(img_local,'rb')

    img=base64.b64encode(f.read())
    params={'image':img}
    params=urllib.urlencode(params)

    #调用获取的token
    access_token=access_to()


    request_url = request_url + '?access_token=' +access_token

    request=urllib2.Request(url=request_url,data=params)

    request.add_header('Content-Type','application/x-www-form-urlencoded')

    response=urllib2.urlopen(request)
    content=response.read()
    if content:
        print content

tt_sb('E:/timg.jpg')
#access_to()