#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import uuid
from django.shortcuts import render
from django.shortcuts import HttpResponse

from ..forms.article import ArticleForm


def index(request):
    return render(request, 'backend_index.html')


def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    return render(request, 'backend_base_info.html')


def upload_avatar(request):
    ret = {'status': False, 'data': None, 'message': None}
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        print(file_obj)
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join('static/imgs/avatar', file_name)
            f = open(file_path, 'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            ret['status'] = True
            ret['data'] = file_path

    return HttpResponse(json.dumps(ret))


def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    return render(request, 'backend_tag.html')


def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    return render(request, 'backend_category.html')


def article(request):
    """
    博主个人文章管理
    :param request:
    :return:
    """

    return render(request, 'backend_article.html')


def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    form = ArticleForm(request=request)
    return render(request, 'backend_add_article.html', {'form': form})


def edit_article(request):
    """
    编辑文章
    :param request:
    :return:
    """
    return render(request, 'backend_edit_article.html')