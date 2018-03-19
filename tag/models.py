#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/3 下午13:20
# @Author  : liuyu

from django.db import models

# Create your models here.
class UserTagType(models.Model):
    """
    用户标签分类
    """
    user = models.ForeignKey('user.User', models.CASCADE, help_text="标签类型拥有者")
    name = models.CharField(max_length=50, help_text="标签类型名字")
    create_time = models.DateTimeField(auto_now_add=True, help_text="标签创建时间")
    update_time = models.DateTimeField(auto_now=True, help_text="修改时间")


class UserTag(models.Model):
    """
    用户标签
    """
    user = models.ForeignKey('user.User', models.CASCADE, help_text="被标注人id")
    user_name = models.CharField(max_length=50, help_text="备注人脉名字")
    remarks = models.CharField(max_length=200, null=True, blank=True,
                               help_text="备注")
    tag_type = models.ForeignKey('UserTagType', models.CASCADE, null=True, blank=True,
                                 help_text="标签类型")
    tag_content = models.CharField(max_length=200, null=True, blank=True,
                                   help_text="标签内容")
    specialty = models.CharField(max_length=200, null=True, blank=True,
                                 help_text="特长")
    is_anonymous = models.BooleanField(default=False, help_text="是否匿名")
    create_time = models.DateTimeField(auto_now_add=True, help_text="标签创建时间")
    update_time = models.DateTimeField(auto_now=True, help_text="修改时间")


