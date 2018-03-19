#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/3 上午12:38
# @Author  : liuyu

from django.db import models

# Create your models here.
class Information(models.Model):
    """
    信息与经验分享
    """
    user = models.ForeignKey('user.User', models.CASCADE, help_text="发布者")
    content = models.CharField(max_length=5000, help_text="信息与经验")
    pictures = models.CharField(max_length=1000, help_text="图片地址")
    collection_count = models.IntegerField(default=0, help_text="收藏数")
    comments_num = models.IntegerField(default=0, help_text="评论数")
    like_num = models.IntegerField(default=0, help_text="点赞数")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, help_text="修改时间")


class InfoComment(models.Model):
    """
    信息与经验评论
    """
    main_info = models.ForeignKey('Information', models.CASCADE, help_text="发布的信息")
    content = models.CharField(max_length=200, help_text="回复内容")
    pictures =  models.CharField(max_length=1000, help_text="图片地址（只有一级回复允许带图片）")
    respondents = models.ForeignKey('user.User', models.CASCADE, related_name= 'res_comments',
                                    help_text="被回复者")
    replayer = models.ForeignKey('user.User', models.CASCADE,  related_name='rep_comments',
                                 help_text="回复者")
    like_num = models.IntegerField(default=0, help_text="点赞数")
    comments_num = models.IntegerField(default=0, help_text="评论数")
    create_time = models.DateTimeField(auto_now_add=True, help_text="回复时间")
    replay_type = models.IntegerField(default=1, help_text="回复类型（1：一级回复，2：二级回复）")


class InformationLike(models.Model):
    """
    信息与经验点赞
    """
    information = models.ForeignKey('Information', models.CASCADE, help_text="发布的信息")
    part_id = models.IntegerField(help_text="1000个id为一组")
    user_ids = models.CharField(max_length=21000, help_text="用户id列表")


class CommentLike(models.Model):
    """
    评论点赞
    """
    comment = models.ForeignKey('InfoComment', models.CASCADE, help_text="评论")
    part_id = models.IntegerField(help_text="1000个id为一组")
    user_ids = models.CharField(max_length=21000, help_text="用户id列表")



