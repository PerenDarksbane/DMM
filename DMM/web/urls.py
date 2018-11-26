from django.urls import re_path

from web.views import index

urlpatterns = [
    re_path('', index),
]
