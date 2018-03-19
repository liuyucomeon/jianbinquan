#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/15 下午2:17
# @Author  : liuyu
from django.conf.urls import url

from wechat_auth.views import wechat_web_auth, wechatVerify, \
    validation_code, bind_phone, login

urlpatterns = [
    # 授权认证时获取openid
    url(r'^web_auth$', wechat_web_auth),
    # 微信回调地址认证
    url(r'^url_auth$', wechatVerify),
    # 发送绑定手机号的验证码
    url(r'^validation_code', validation_code),
    # 验证并绑定手机号
    url(r'^phone_binding$', bind_phone),


    # 登陆（调试用的）
    url(r'^login', login),


]