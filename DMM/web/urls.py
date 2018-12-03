from django.urls import re_path, path

from web.views import *

urlpatterns = [
    path('view', view),
    path('feats', feats),
    path('equipment', equipment),
    path('create', create),
    path('create_feat', create_feat),
    path('create_equipment', create_equipment),
    path('logout', user_logout),
    path('login', user_login),
    path('register', register),
    re_path('', index),
]
