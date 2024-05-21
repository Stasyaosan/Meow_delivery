from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('reg', reg),
    path('suc/<str:token>', suc_user),
    path('logout', logout),
]