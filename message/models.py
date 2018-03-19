#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/3 下午13:38
# @Author  : liuyu

from django.db import models

# Create your models here.
class ContactPushMsg(models.Model):
    """
    人脉推送消息
    """
    requester = models.ForeignKey('user.User', models.CASCADE, related_name= 'r_push_msgs',
                                  help_text="请求者")
    mediator = models.ForeignKey('user.User', models.CASCADE, related_name= 'm_push_msgs',
                                 help_text="中间人")
    target_friend = models.ForeignKey('user.User', models.CASCADE, related_name= 't_push_msgs',
                                      help_text="目标好友")
    state = models.IntegerField(default=0, help_text="0:求推荐,1:已推荐,2已忽略")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")


class SystemMsg(models.Model):
    """
    系统消息
    """
    receiver = models.ForeignKey('user.User', models.CASCADE, related_name= 'sys_msgs',
                                  help_text="接收者")
    content = models.CharField(max_length=100, help_text="消息内容")
    has_deleted = models.BooleanField(default=False, help_text="是否已被删除")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")
