import os
import logging
import warnings
import datetime
import win32api
import win32print

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from user.models import UserPrintRecord

logger = logging.getLogger(__name__)
User = get_user_model()


def print_pdf_sumatra(pdf_file_name, print_settings=None):
    if print_settings:
        os.system(f"{settings.SUMATRAPDF_PATH} -print-to \"{settings.PRINTER_NAME}\" -print-settings \"{print_settings}\" \"{pdf_file_name}\" ")
    else:
        os.system(f"{settings.SUMATRAPDF_PATH} -print-to \"{settings.PRINTER_NAME}\" \"{pdf_file_name}\" ")


def index(request):
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id', '')
        password = request.POST.get('password', '')
        if stu_id and password:
            user = authenticate(request, username=stu_id, password=password)
            if user is not None:
                login(request, user)
                # print('login')
                return redirect('panel')
            else:
                return render(request, 'index.html', {'instruction': "用户名或密码不对"})
        else:
            return render(request, 'index.html', {'instruction': "用户名或密码不能为空"})
    else:
        if request.user.is_authenticated:
            return redirect('panel')
    return render(request, 'index.html', {'instruction': "请登录"})


def user_logout(request):
    logout(request)
    return redirect('index')


def user_register(request):
    context = {
        'user': request.user,
        'instruction': '',
    }
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        name = request.POST.get('name', '李大嘴')
        if stu_id and password1 and password2:
            if password1 != password2:
                context['instruction'] = '密码输入不一致'
            else:
                if User.objects.filter(username=stu_id).count() >= 1:
                    context['instruction'] = '该学号的账户已被注册'
                else:
                    user = User.objects.create_user(username=stu_id, password=password1, name=name)
                    user.save()
                    context['instruction'] = '注册成功'
        else:
            context['instruction'] = '请把仨框填满'

    return render(request, 'user_register.html', context=context)


def change_password(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'instruction': '',
        }
        if request.method == 'POST':
            old_password = request.POST.get('old_password', '')
            new_password1 = request.POST.get('new_password1', '')
            new_password2 = request.POST.get('new_password2', '')
            if old_password and new_password1 and new_password2:
                if request.user.check_password(old_password):
                    if new_password1 == new_password2:
                        request.user.set_password(new_password1)
                        logout(request)
                        return redirect('index')
                    else:
                        context['instruction'] = '两次输入的新密码必须保持一致'
                else:
                    context['instruction'] = '旧密码输入错误'
            else:
                context['instruction'] = '请把三个密码框填满'

        return render(request, 'user_change_password.html', context=context)
    else:
        return redirect('index')


def under_construction(request):
    return render(request, 'under_construction.html')


def panel(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        print_num = UserPrintRecord.objects.filter(user=request.user).count()
        context['print_num'] = print_num
        if request.method == "POST":
            print_file = request.FILES.get('print_file', None)
            if print_file:
                file_path_name = os.path.join(settings.UPLOAD_DIR,
                                              '{}-{}-{}'.format(request.user.username,
                                                                  datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                                                                  print_file.name))
                with open(file_path_name, 'wb') as f:
                    for chunk in print_file.chunks():
                        f.write(chunk)
                record = UserPrintRecord(user=request.user, file_path=file_path_name)
                record.save()

                action = request.POST.get('action', '')
                print_settings = request.POST.get('print_settings', None)

                if action == 'upload':
                    context['instruction'] = '上传成功'
                else:
                    if print_file.name.split('.')[-1].lower() != 'pdf':
                        context['instruction'] = '文件已上传，但不支持非PDF文件的打印'
                        return render(request, 'print.html', context=context)
                    context['instruction'] = '上传成功，准备打印'
                    print_num = UserPrintRecord.objects.filter(user=request.user).count()
                    context['print_num'] = print_num
                    print_pdf_sumatra(file_path_name, print_settings)
                return render(request, 'print.html', context=context)
            else:
                context['instruction'] = '嘿，你没有上传文件哦'
                return render(request, 'print.html', context=context)
        else:
            return render(request, 'print.html', context=context)
    else:
        return redirect('index')
