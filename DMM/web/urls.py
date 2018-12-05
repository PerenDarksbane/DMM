from django.urls import re_path, path

from web.views import *

# This ensures that redirects go to the right view in views.py
urlpatterns = [
    path('view', view),
    path('feats', feats),
    path('equipment', equipment),
    path('spells', spells),
    path('races', races),
    path('classes', classes),
    path('characters', characters),
    path('viewer', viewer),
    path('create', create),
    path('create_feats', create_feats),
    path('create_equipment', create_equipment),
    path('create_spells', create_spells),
    path('create_races', create_races),
    path('create_classes', create_classes),
    path('create_characters', create_characters),
    path('logout', user_logout),
    path('login', user_login),
    path('register', register),
    # When not given a valid url, the program will redirect them to the main page
    re_path('', index),
]
