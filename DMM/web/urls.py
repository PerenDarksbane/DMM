from django.urls import re_path, path

from web.views import *

urlpatterns = [
    path('register', register),
    path('posts', posts),
    re_path('', index),
]
