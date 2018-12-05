from django.urls import re_path, path

from web.views import *

urlpatterns = [
    path('view', view),
    path('feats', feats),
    path('equipment', equipment),
    path('spells', spells),
    path('races', races),
    path('classes', classes),
    path('characters', characters),
    path('create', create),
    path('create_feat', create_feat),
    path('create_equipment', create_equipment),
    path('create_spells', create_spells),
    path('create_races', create_races),
    path('create_classes', create_classes),
    path('create_characters', create_characters),
    path('logout', user_logout),
    path('login', user_login),
    path('register', register),
    re_path('', index),
]
