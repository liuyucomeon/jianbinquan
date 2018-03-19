#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/3 上午11:38
# @Author  : liuyu

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, help_text="名字")
    bbid = models.CharField(max_length=30, null=True, blank=True, unique=True, help_text="宾宾id")
    can_modify_bbid = models.BooleanField(default=True, help_text="是否可以修改宾宾id")
    openid = models.CharField(max_length=100, null=True, blank=True, help_text="公众号下唯一标识")
    head_portrait = models.CharField(max_length=100, null=True, blank=True, help_text="头像")
    phone = models.CharField(max_length=11, null=True, blank=True, help_text="电话号码")
    tag = models.CharField(max_length=20, null=True, blank=True, help_text="标签")
    friend_tag = models.CharField(max_length=2000, null=True, blank=True, help_text="好友标签")
    influence = models.IntegerField(default=0, help_text="影响力指数")
    friends_num = models.IntegerField(default=0, help_text="好友数")
    comments_num = models.IntegerField(default=0, help_text="评论数")
    like_num = models.IntegerField(default=0, help_text="点赞数")
    scan_num = models.IntegerField(default=0, help_text="浏览数")
    forward_num = models.IntegerField(default=0, help_text="转发数")
    look_forward_know = models.CharField(max_length=50, null=True,
                                         blank=True, help_text="期待结识")
    honor_desc = models.CharField(max_length=500, null=True, blank=True, help_text="荣誉")
    honor_pics = models.CharField(max_length=1000, null=True, blank=True,
                                  help_text="荣誉照片")
    interest = models.CharField(max_length=100, null=True, blank=True,
                                help_text="兴趣爱好")
    hometown = models.CharField(max_length=100, null=True, blank=True,
                                help_text="家乡")
    university = models.CharField(max_length=100, null=True, blank=True,
                                help_text="毕业院校")
    living_city = models.CharField(max_length=100, null=True, blank=True,
                                help_text="来往城市")
    company = models.CharField(max_length=100, null=True, blank=True,
                                help_text="公司")
    position = models.CharField(max_length=100, null=True, blank=True,
                                help_text="职务")
    company_intr = models.CharField(max_length=500, null=True, blank=True,
                                help_text="公司简介")
    financing_stage = models.CharField(max_length=20, null=True, blank=True,
                                help_text="融资阶段")
    company_city = models.CharField(max_length=100, null=True, blank=True,
                                help_text="公司坐落城市")
    company_site = models.CharField(max_length=200, null=True, blank=True,
                                help_text="公司官网")
    recommend_all_friends = models.BooleanField(default=False,
                                                help_text="相当于所有好友都被金荐（是否关闭二度人脉）")
    can_be_search = models.BooleanField(default=False, help_text="允许被搜索")
    can_be_mediator = models.BooleanField(default=False, help_text="允许荐人脉")
    is_active = models.IntegerField(default=1, help_text="是否激活")
    create_time =models.DateTimeField(auto_now_add=True, help_text="创建时间")

    w_nickname = models.CharField(max_length=100, null=True, blank=True,
                                help_text="微信昵称")
    w_sex = models.IntegerField(default=0, help_text="1时是男性，值为2时是女性，值为0时是未知")
    w_province = models.CharField(max_length=100, null=True, blank=True,
                                help_text="微信省份")
    w_city = models.CharField(max_length=100, null=True, blank=True,
                                help_text="微信城市")
    w_country = models.CharField(max_length=100, null=True, blank=True,
                                help_text="微信国家")


class UserFriendRela(models.Model):
    """
    用户好友关系
    """
    requester = models.ForeignKey('User', models.CASCADE,related_name= 'rrelas',
                                  help_text="请求者")
    mediator = models.ForeignKey('User', models.CASCADE, related_name= 'mrelas',
                                 help_text="中间人")
    target_friend = models.ForeignKey('User', models.CASCADE, related_name= 'trelas',
                                      help_text="目标好友")
    is_niubi = models.BooleanField(default=False, help_text="是否金荐")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")


class UserCollectRela(models.Model):
    """
    用户收藏用户
    """
    owner = models.ForeignKey('User', models.CASCADE, related_name= 'o_collect_relas',
                              help_text="收藏者")
    mediator = models.ForeignKey('User', models.CASCADE, related_name='m_collect_relas',
                                 help_text="中间人")
    target_friend = models.ForeignKey('User', models.CASCADE, related_name= 't_collect_relas',
                                      help_text="被收藏的用户")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")


class UserCollectInfo(models.Model):
    """
    用户收藏的信息
    """
    owner = models.ForeignKey('User', models.CASCADE, help_text="收藏者")
    target_info = models.ForeignKey('info.Information', models.CASCADE,
                                    help_text="被收藏的信息与经验")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")


class UserInvite(models.Model):
    """
    用户邀请
    """
    owner = models.ForeignKey('User', models.CASCADE, related_name= 'oinvites',
                              help_text="邀请者")
    target_friend = models.ForeignKey('User', models.CASCADE,related_name= 'tinvites',
                                      help_text="被邀请的用户")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")


