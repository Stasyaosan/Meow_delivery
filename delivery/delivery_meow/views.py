import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *


def index(request):
    return render(request, 'index.html')


def reg(request):
    if request.method == 'POST':
        suc = ''
        error = ''
        if 'reg' in request.POST:
            email = request.POST['email']
            phone = request.POST['phone']
            role = request.POST['role']
            token = generate_Token()
            password = make_password(request.POST['password'])
            if not User.objects.filter(email=email).exists():
                user = User()
                user.password = password
                user.email = email
                user.phone = phone
                user.role = Role.objects.filter(title=role).first()
                user.token = token
                user.save()

                url = f'http://127.0.0.1:8000/suc/{token}'
                send_mail(subject='Активация учётной записи', message=url, from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[email])

                suc += 'Подтревдите акаунт в Email письме'
                return render(request, 'suc.html', {'suc': suc})
            else:
                error += 'Такой пользователь уже есть'

                return render(request, 'suc.html', {'error': error})

        elif 'auth' in request.POST:
            error = ''
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                if check_password(password, user.password):
                    request.session['user'] = email
                else:
                    error = 'Неправильный пароль!'
            else:
                error = 'Такого пользователя нет!'
            return render(request, 'suc.html', {'error': error})


def suc_user(request, token):
    if User.objects.filter(token=token).exists:
        User.objects.filter(token=token).update(suc=1, token='')
        return HttpResponse('Вы успешно активировали учётную запись <a href="/">Перейти на сайт</a>')
    else:
        return HttpResponse('Токен неверный!!')


def generate_Token():
    s = 'asdfklewjtw;ogkassdk@#$%$$$#GGUYGUYGUYTFlgfnmsdklgnhythbGUYHJERIGVKGIfdfsdf564643!!!!@@@@#wjklegnweklfgfgerygfyegydfgYYYGY656565rfyrgye'
    return ''.join([s[random.randint(0, len(s) - 1)] for i in range(32)])
