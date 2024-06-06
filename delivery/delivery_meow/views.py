import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .dadata import gDadata


def index(request):
    orders = []
    if 'user' in request.session:
        current_user = User.objects.filter(email=request.session['user']).first()
        if request.session['role'] == 'Клиент':
            orders = Order.objects.filter(client=current_user)

    else:
        current_user = ''
    # geo = get_geo('москва')

    return render(request, 'index.html', {'current_user': current_user, 'orders': orders})


def reg(request):
    if 'user' in request.session:
        current_user = User.objects.filter(email=request.session['user']).first()
    else:
        current_user = ''
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
                return render(request, 'suc.html', {'suc': suc, 'current_user': current_user})
            else:
                error += 'Такой пользователь уже есть'

                return render(request, 'suc.html', {'error': error, 'current_user': current_user})

        elif 'auth' in request.POST:
            error = ''
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                if user.suc != 0:
                    if check_password(password, user.password):
                        request.session['user'] = email
                        request.session['role'] = user.role.title
                        return redirect('/')
                    else:
                        error += 'Пароль введен не корректно!'
                else:
                    error += 'Учетная запись не активирована!'
            else:
                error += 'Такого пользователя не существует!'
            return render(request, 'suc.html', {'error': error, 'current_user': current_user})


def suc_user(request, token):
    if User.objects.filter(token=token).exists():
        User.objects.filter(token=token).update(suc=1, token='')
        return HttpResponse('Вы успешно активировали свою учетную запись! <a href="/">Перейти на сайт</a>')
    else:
        return HttpResponse('Token не верный!')


def generate_Token():
    s = 'asdfklewjtwogkassdkGGUYGUYGUYTFlgfnmsdklgnhythbGUYHJERIGVKGIfdfsdf564643wjklegnweklfgfgerygfyegydfgYYYGY656565rfyrgye'
    return ''.join([s[random.randint(0, len(s) - 1)] for i in range(32)])


def logout(request):
    if request.method == 'POST' and 'user' in request.session:
        del request.session['user']
    if 'role' in request.session:
        del request.session['role']
    return redirect('/')


def update(request):
    if 'user' in request.session and request.method == 'POST':
        login = request.POST['login']
        email = request.POST['email']
        User.objects.filter(email=request.session['user']).update(login=login, email=email)
        return redirect('/')


def ajax_load_address(request):
    if request.method == 'POST':
        d = gDadata()
        query = request.POST['address']
        address = d.get_address(query)
        res = '<div class="bl_location" style="width: 100%!important;padding: 10px;">'
        for i in address:
            res += f'<div data-lon="{i['data']['geo_lon']}" data-let="{i['data']['geo_lat']}" style="width: 100%!important; margin: 10px">{i['value']}</div>'
        res += '</div>'

        return HttpResponse(res)


def add_order(request):
    if 'user' in request.session and request.method == 'POST':
        current_user = User.objects.filter(email=request.session['user']).first()
        address = request.POST['address']
        description = request.POST['description']
        datetime = request.POST['datetime']
        lon = request.POST['lon']
        lat = request.POST['lat']
        client = current_user

        order = Order(description=description, client=client, address=address, datetime=datetime, lon=lon, lat=lat)
        order.save()

        return redirect('/')


def get_json_order(request):
    orders = Order.objects.filter(status='Ожидает курьера:)')
    if 'user' in request.session:
        if request.session['role'] == 'Клиент':
            orders = Order.objects.filter(client=User.objects.filter(email=request.session['user']).first())
    res = {}
    res['type'] = 'FeatureCollection'
    res['features'] = []
    for order in orders:
        if 'user' in request.session:
            if request.session['role'] == 'Клиент':
                res['features'].append(
                    {
                        'type': 'Feature',
                        'id': order.id,
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [
                                order.lat,
                                order.lon

                            ]
                        },
                        'properties': {
                            "balloonContentBody": '<p><form action="/otmena" method="post"><input type="hidden" name="id_order" value="' + str(
                                order.id) + '"><button>Отменить заказ</button></form></p>',
                        }

                    }
                )
            else:
                res['features'].append(
                    {
                        'type': 'Feature',
                        'id': order.id,
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [
                                order.lat,
                                order.lon

                            ]
                        },
                        'properties': {
                            "balloonContentBody": '<p><form action="/take_order" method="post"><input type="hidden" name="id_order" value="' + str(
                                order.id) + '"><button>Взять заказ</button></form></p>',
                        }

                    }
                )
    return JsonResponse(res)


@csrf_exempt
def take_order(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.session['role'] == 'Курьер':
                current_user = User.objects.filter(email=request.session['user']).first()
                id_order = request.POST['id_order']
                Order.objects.filter(id=id_order).update(courier=current_user, status='Заказ принят')

    return redirect('/')


@csrf_exempt
def otmena_order(request):
    if 'user' in request.session:
        if request.method == 'POST':
            if request.session['role'] == 'Клиент':
                id_order = request.POST['id_order']
                Order.objects.filter(id=id_order).delete()

    return redirect('/')
