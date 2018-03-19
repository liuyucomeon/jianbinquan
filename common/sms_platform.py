#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 下午2:34
# @Author  : liuyu
import base64
import hashlib
import urllib.parse
import urllib.request


def getmd5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()


def send_mesg_jtd(mobile, content):
    """
    聚通达短信接口
    :return: 
    """
    url = "http://119.90.36.56:8090/jtdsms/sendData.do"
    # 用户名
    uid = "202472"
    # 密码
    pwdStr = "944759"
    pwd = getmd5(pwdStr)
    pwd = pwd.upper()
    contentStr = base64.b64encode(content.encode(encoding='utf-8', errors='strict'))
    encodeType = 'base64'
    encode = 'utf8'
    data = {'uid': uid, 'password': pwd,
            'mobile': mobile, 'encode': encode,
            'content': contentStr,
            'encodeType': encodeType}
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.urlopen(url, post_data)
    return req.read()


