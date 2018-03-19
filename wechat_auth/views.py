import hashlib
import json

import binascii
import os
import pickle

import requests

# Create your views here.
import time
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import response, status
from rest_framework.decorators import api_view, authentication_classes

from common.auth import TokenAuthentication
from common.sms_platform import send_mesg_jtd
from common.util import upt_model_by_json, getRandomChar, convertByteFromMap
from jianbinquan.settings import appid, secret, logger
from user.models import User

access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s" \
            "&secret=%s&code=%s&grant_type=authorization_code"
user_info_url = "https://api.weixin.qq.com/sns/userinfo?access_token" \
                "=%s&openid=%s&lang=zh_CN"



@api_view(['GET','POST'])
def wechatVerify(request):
    """
    微信接口配置信息回调接口
    :param request: 
    :return: 
    """
    # 验证微信公众号回调地址
    if request.method == "GET":
        echostr = _verifyCallUrl(request)
        return HttpResponse(echostr)


@api_view(['GET'])
def wechat_web_auth(request):
    """
    网页授权获取微信用户信息(网页授权)
        :param
            code:重定向url的code
            state:重定向url的state
    """
    data = request.query_params
    # 获取access_token
    result = requests.get(access_token_url.format(appid,
                    secret, data["code"])).text
    if "errcode" in result:
        return response.Response(data=result, status=status.HTTP_400_BAD_REQUEST)
    result = json.loads(result)
    access_token = result["access_token"]
    openid = result["openid"]

    # 获取基本信息
    user_info_result = requests.get(user_info_url.format(access_token,
                            openid)).text
    if "errcode" in result:
        return response.Response(data=result, status=status.HTTP_400_BAD_REQUEST)
    uir = json.loads(user_info_result)

    # 如果新用户则创建
    try:
        user = User.objects.get(openid=uir['openid'])
    except ObjectDoesNotExist:
        bbid = _generate_bbid()
        user = User.objects.create(openid=uir['openid'], w_nickname=uir['nicknam'],
                                   w_sex=uir['sex'], w_province=uir['province'],
                                   w_city=uir['w_city'], w_country=uir['country'],
                                   bbid=bbid)
    else:
        # 更新用户信息
        upt_model_by_json(user, uir)

    # 清除以前的token
    _del_token(user.id)

    # 生成自己的token,客户端请求接口需要
    token = _get_token(user)
    uir["token"] = token

    return response.Response(data=uir)


def _del_token(userid):
    """
    清除以前的token
    :return: 
    """
    redisDB = get_redis_connection('default')
    keys = redisDB.keys("token:*:" + str(userid))
    if len(keys) != 0:
        redisDB.delete(keys[0].decode())


def _get_token(user):
    """
    获取并保存token
    :return: 
    """
    user_pick = pickle.dumps(user)
    token = binascii.b2a_base64(os.urandom(24))[:-1].decode()
    redisDB = get_redis_connection('default')
    redisDB.setex("token:"+token, user_pick, 24*60*60)
    return token


def _verifyCallUrl(request):
    data = request.query_params
    if len(data) == 0:
        logger.info("未接收到微信验证参数")
    logger.info("微信服务器请求参数为：" + str(data))

    signature = data['signature']
    timestamp = data['timestamp']
    nonce = data['nonce']
    echostr = data['echostr']
    token = "TcZHbjlQQqGTelkrk0phenaigaoke"  # 请按照公众平台官网\基本配置中信息填写

    parmList = [token, timestamp, nonce]
    parmList.sort()
    paramStr = ''.join(parmList)

    hashcode = hashlib.sha1(paramStr.encode()).hexdigest()
    if hashcode == signature:
        logger.info("相等")
        return echostr
    else:
        logger.info("不相等")

def _generate_bbid():
    """
    生成宾宾id(先用时间戳)
    :return: 
    """
    return str(int(time.time()))


@api_view(['GET'])
def validation_code(request):
    """
    获取手机绑定的验证码
    :param phone: 
    :param request: 
    :return: 
    """
    phone = request.query_params['phone']
    redisDB = get_redis_connection('default')
    key = "register:" + phone
    VerificationCode = getRandomChar(4)
    # 查看key是否存在
    telInfo = redisDB.hgetall(key)
    if telInfo:
        telInfo = convertByteFromMap(redisDB.hgetall(key))
        # 连续操作三次，需等待半小时
        if int(telInfo["count"]) >= 3:
            return response.Response({"code": 10001, "msg": "操作频繁，请稍后再试"},
                                     status=status.HTTP_403_FORBIDDEN)
        # 设置过期时间30分钟
        redisDB.expire(key, 15 * 60)
        redisDB.hincrby(key, "count", 1)
        redisDB.hset(key, "code", VerificationCode)
    else:
        redisDB.hmset(key, {"count": 1, "code": VerificationCode})
    # 发送短信
    content = "【宾宾圈】验证码"+VerificationCode + "，请用于手机号验证（如非本人操作，请忽略此短信）"
    send_mesg_jtd(phone, content)
    return response.Response({"code": 0, "msg": "success"},
                             status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def bind_phone(request):
    """
    绑定手机号
    :param request: 
    :return: 
    """
    user = request.user
    params = request.data
    phone = params['phone']
    redisDB = get_redis_connection('default')
    code_info = convertByteFromMap(redisDB.hgetall("register:"+phone))
    if params['code'] ==code_info['code']:
        # 绑定手机号
        user.phone = params['phone']
        user.save()
        return response.Response({"code": 0, "msg": "success"},
                             status=status.HTTP_200_OK)
    else:
        return response.Response({"code": 10002, "msg": "验证码错误"},
                             status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def login(request):
    """
    测试接口
    :param request: 
    :return: 
    """
    redisDB = get_redis_connection('default')
    user = User.objects.get(id=1)

    keys = redisDB.keys("token:*:" + str(1))
    if len(keys)!=0:
        redisDB.delete(keys[0].decode())

    user_pick = pickle.dumps(user)
    token = binascii.b2a_base64(os.urandom(24))[:-1].decode()
    redisDB.setex("token:"+token+":"+str(user.id), 24*60*60, user_pick)
    redisDB.keys()
    return response.Response({"code": 0, "msg": "success"},
                             status=status.HTTP_200_OK)
