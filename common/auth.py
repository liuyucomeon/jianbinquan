#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 下午3:34
# @Author  : liuyu
import pickle

from django_redis import get_redis_connection
from rest_framework import authentication, exceptions


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise exceptions.AuthenticationFailed('No token')
        redisDB = get_redis_connection('default')
        key = redisDB.keys("token:"+token+":*")
        user_byte = redisDB.get(key[0].decode())
        if not user_byte:
            raise exceptions.AuthenticationFailed('token错误')
        user =  pickle.loads(user_byte)
        return user, None