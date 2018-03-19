#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 下午4:17
# @Author  : liuyu
import random
import string


def upt_model_by_json(model, map_data):
    """
    根据json数据更新model
    :param json_data: 
    :return: 
    """
    for k,v in map_data:
        if hasattr(model, k):
            setattr(model, k, v)
    model.save()


def getRandomChar(num):
    """
    获取随机字符
    :param num: 
    :return: 
    """
    return ''.join(random.sample(string.ascii_letters+string.digits, num))


def convertByteFromMap(map):
    """
    map中的字节转字符
    :param map: 
    :return: 
    """
    result = {}
    for k, v in map.items():
        k = k.decode()
        v = v.decode()
        result[k] = v
    return result

