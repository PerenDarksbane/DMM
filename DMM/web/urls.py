from django.urls import re_path, path

from web.views import *

urlpatterns = [
    path('login', user_login),
    path('register', register),
    path('posts', posts),
    re_path('', index),
]
