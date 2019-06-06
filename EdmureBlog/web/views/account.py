#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render
from utils.check_code import create_validate_code

from ..forms.account import LoginForm

from repository import models


def editor(request):
    content = request.POST.get('content')
    print(content)
    return render(request,'editor.html')


def upload_file(request):
    import os
    import json
    dir = request.GET.get('dir')
    if dir == 'image':
        pass
    obj = request.FILES.get('fafafa')
    file_path = os.path.join('static/imgs',obj.name)
    with open(file_path,'wb') as f:
        for chunk in obj.chunks():
            f.write(chunk)
    ret = {
        'error': 0,
        'url': 'http://127.0.0.1:8000/'+file_path,
        'message': '错误了...'
    }
    return HttpResponse(json.dumps(ret))

def manager_file(request):
    import os
    import time
    import json
    from EdmureBlog.settings import BASE_DIR

    dic = {}
    root_path = os.path.join(BASE_DIR,'static/')

    static_root_path = '/static/'

    # 要访问的路径
    request_path = request.GET.get('path')

    if request_path:
        abs_current_dir_path = os.path.join(root_path, request_path)
        # request_path=css/    ""
        # move_up_dir_path=css
        #
        move_up_dir_path = os.path.dirname(request_path.rstrip('/'))
        dic['moveup_dir_path'] = move_up_dir_path + '/' if move_up_dir_path else move_up_dir_path

    else:
        # 根目录无上一级
        abs_current_dir_path = root_path
        dic['moveup_dir_path'] = ''

    dic['current_dir_path'] = request_path
    dic['current_url'] = os.path.join(static_root_path, request_path)

    file_list = []
    for item in os.listdir(abs_current_dir_path):
        # item每一个文件名
        abs_item_path = os.path.join(abs_current_dir_path, item)
        a, exts = os.path.splitext(item)
        is_dir = os.path.isdir(abs_item_path)
        if is_dir:
            temp = {
                'is_dir': True,
                'has_file': True,
                'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }
        else:
            temp = {
                'is_dir': False,
                'has_file': False,
                'filesize': os.stat(abs_item_path).st_size,
                'dir_path': '',
                'is_photo': True if exts.lower() in ['.jpg', '.png', '.jpeg'] else False,
                'filetype': exts.lower().strip('.'),
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }

        file_list.append(temp)
    dic['file_list'] = file_list
    return HttpResponse(json.dumps(dic))


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects.filter(username=username, password=password).values('nid', 'nickname',
                                                                                                    'username', 'email',
                                                                                                    'avatar',
                                                                                                    'blog__nid',
                                                                                                    'blog__site').first()
            if not user_info:
                # result['message'] = {'__all__': '用户名或密码错误'}
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            print(form.errors)
            # result['message'] = form.errors
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))


def register(request):
    """
    注册
    :param request:
    :return:
    """

    return render(request, 'register.html')


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    pass
