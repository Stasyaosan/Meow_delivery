from django.db import models


class Role(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название роли')

    def __str__(self):
        return self.title


class User(models.Model):
    email = models.EmailField(verbose_name='Email: ')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    login = models.CharField(max_length=100, verbose_name='Логин', null=True, default='')
    phone = models.CharField(max_length=100, verbose_name='Телефон', null=True)
    level = models.IntegerField(default=0)
    token = models.TextField(null=True, blank=True)
    suc = models.IntegerField(default=0)


class Order(models.Model):
    description = models.TextField(verbose_name='Описание заказа')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client', null=True)
    courier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courier', null=True, blank=True)
    datetime = models.DateTimeField()
    lon = models.CharField(max_length=100, null=True, blank=True)
    lat = models.CharField(max_length=100, null=True, blank=True)
    date_create = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200, verbose_name='Адрес')
    status = models.CharField(max_length=200, default='Ожидает курьера:)')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length='200')
    score = models.IntegerField()
